#the view when you're in a battle
# [Player]_______________________[Enemy]
# _______[Card1][Card2]...[Cardn]____ <- (Player's Hand)
# (offscreen:) [Cardn+1]...[Cardj]_____[Cardj+1][Cardi] <- (Player's deck, n+1 - j is draw pile, j+1 - i is discard)

#Player and Enemy have a Deck each, BattleView has a Hand has Player's Deck


import pygame, json, os

import numpy as np

#needs a character name "Player"
class BattleView(pygame.sprite.RenderUpdates):
    def __init__(self, background_image, *sprites):
        pygame.sprite.RenderUpdates.__init__(self)
        self.image, self.rect = background_image
        self.player_slot = self.rect.midleft
        self.enemy_slot = self.rect.midright
        self.card_slots = self.rect.bottomleft
        self.cards = None
        
        
    #call after adding sprites    
    def arrange(self):
        for sprite in self:
            if sprite.name == "Player":
                sprite.rect = self.player_slot
                self.cards = Hand(self.card_slots, sprite.deck)
            else: 
                sprite.rect = self.enemy_slot

    def setBackground(self, loaded_image):
        self.image, self.rect = loaded_image
        return True

    def handle(self, event):
        match event.name:
            case "dropEvent":
                if self.rect.colliderect(event.pos):
                    for effect in event.effects:
                        pygame.event.post(pygame.event.Event(pygame.USEREVENT, { 'name' : effect.name, 'amount' : effect.amount} ))
            case _:
                super(BattleView,self).update(event)

#draw pile starts at 0 cuz why pop
#                   might need to optimize later
class Deck(pygame.sprite.Group):
    def __init__(self, *sprites):
        pygame.sprite.Group.__init__(self)
        self.discard_pile = pygame.sprite.Group()
        self.draw_pile = pygame.sprite.Group()
        for sprite in sprites:
            self.draw_pile.add(sprite)
        self.rng = np.random.default_rng()
        self.shuffle()

    def pullCards(self, amount):
        cards_pulled = self.draw_pile.sprites()[:amount]
        self.draw_pile.remove(cards_pulled)
        return cards_pulled
    
    def shuffle(self):
        self.rng.shuffle(self.draw_pile.sprites())
        return self.draw_pile
    
    def addToDiscardPile(self, *sprites):
        self.discard_pile.add(sprites)
        return self.discard_pile
    
    def addToDrawPile(self, *sprites):
        self.draw_pile.add(sprites)
        return self.draw_pile

#need to post a turnStart event in the loop
#need to post a turnEnd event in the loop
class Hand(pygame.sprite.RenderUpdates):
    def __init__(self, rect, aDeck, *sprites):
        pygame.sprite.RenderUpdates.__init__(self)
        self.rect = rect
        

        #should these be player character attributes instead?
        self.m_deck = aDeck
        self.hand_size = 10
        self.start_size = 5
        
    def add(self, *sprites):
        if len(self.sprites) > self.hand_size:
            print("Can't add more cards")
            return False
        else:
            super(Hand,self).add(sprites)

    def update(self, event):
        match event.name:
            case 'turnStart':
                self.m_deck.pullCards(self.start_size)
            case 'turnEnd':
                self.m_deck.addToDiscardPile(self.sprites)
                self.empty()
            case 'pullCard':
                self.m_deck.pullCards(event['amount'])
            case _:
                super(Hand,self).update(event)
        
    def getRect(self):
        return self.rect
    
    def setRect(self, dim, value):
        def x(num):
            self.rect.x = num
            return self.rect
        def y(num):
            self.rect.y = num
            return self.rect
        def w(num):
            self.rect.w = num
            return self.rect
        def h(num):
            self.rect.h = num
            return self.rect
        def centerx(num):
            self.rect.centerx = num
            return self.rect
        def centery(num):
            self.rect.centery = num
            return self.rect
        
        match dim:
            case 'x':
                return x(value)
            case 'y':
                return y(value)
            case 'w':
                return w(value)
            case 'h':
                return h(value)
            case 'centerx':
                return centerx(value)
            case 'centery':
                return centery(value)
            case _:
                print(f"Unsupported operation {dim}")
                return False
    
    def getHandSize(self):
        return self.hand_size
    
    def setHandSize(self,newSize):
        self.hand_size = newSize
        return self.hand_size
    
    def getStartSize(self):
        return self.start_size
    
    def setStartSize(self, newSize):
        self.start_size = newSize
        return self.start_size

    def addDeck(self, newDeck):
        self.m_deck = newDeck
        return self.m_deck

    def getDeck(self):
        return self.m_deck
    
class Character(pygame.sprite.Sprite):
    def __init__(self, name, loaded_image, health, energy, aDeck):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = loaded_image
        self.name = name
        self.health = health
        self.energy = energy
        self.deck = Deck(aDeck)
    
    def update(self,event):
        match event.name:
            case 'healthEvent':
                self.health += event.amount
            case 'energyEvent':
                self.energy += event.amount
            case _:
                pass

#effect_list = [{'name':[healthEvent,energyEvent], 'amount':int},{'name': , 'amount': }...]
#           should always include an 'energyEvent'
class Card(pygame.sprite.Sprite):
    effects = None
    title = ''
    image_src = ''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.dropEvent = None

    def update(self, cls, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == "button1":
                if self.rect.collidepoint(event.pos):
                    self.rect = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == "button1":
                self.dropEvent = pygame.event.Event(pygame.USEREVENT + 1, {'name': 'dropEvent', 'pos' : self.rect, 'effects':cls.effects})
                pygame.event.post(self.dropEvent)
        else:
            pass

def CardFactory(card):
    class SubCard(Card):
        effects = card['effects']
        title = card['title']
        image_src = card['image_src']
    return SubCard()
        