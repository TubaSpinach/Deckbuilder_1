import pygame, os, json
from .. import play

def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join("res", name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except FileNotFoundError:
        print(f"Cannot load image: {fullname}")
        raise SystemExit
    return image, image.get_rect()
def load_json(file):
    try: 
        with open(file) as f:
            target_dict = json.load(f)
        return target_dict
    except FileNotFoundError as err:
        print(f"Couldn't load file {err}")
        return {}

card_dict = load_json("res/card_lib.txt")

pygame.init()
screen = pygame.display.set_mode((1280, 720))

deck_list = []
d2 = []
for i in range(0,10):
    deck_list.append(play.CardFactory(card_dict['strike']))
    d2.append(play.CardFactory(card_dict['bash']))

tDeck = play.Deck(deck_list)
td2 = play.Deck(d2)

tPlayer = play.Character("Player",load_png("player.png"),10,3,tDeck)
tEnemy = play.Character("Enemy",load_png("enemy.png"),10,3,tDeck)
tBView = play.BattleView(load_png("background.png"))
tBView.add(tPlayer)
tBView.add(tEnemy)
tBView.arrange()

tEvents = [pygame.event.Event(pygame.USEREVENT,{'name':'healthEvent','amount': -5 }),
           pygame.event.Event(pygame.USEREVENT,{'name':'energyEvent','amount': -1 }),
           pygame.event.Event(pygame.USEREVENT,{'name':'dropEvent','pos':tBView.rect,
                                                'effects':[{'name':'energyEvent','amount':1}]})]

tCard = play.CardFactory(card_dict['strike'])

def test_card_factory():
    assert isinstance(tCard,play.Card)
    assert tCard.title == card_dict['strike']['title']
    assert tCard.effects == card_dict['strike']['effects']
    assert tCard.image_src == card_dict['strike']['image_src']

def test_deck():
    cards_pulled = tDeck.pullCards(1)
    assert isinstance(cards_pulled[0],play.Card)
    tDeck.addToDiscardPile(cards_pulled)
    assert len(tDeck.discard_pile) == len(cards_pulled)
    tDeck.fromDiscardToDraw()
    assert len(tDeck.discard_pile) == 0

def test_characters():
    tPlayer.setHandSize(3)
    tPlayer.setStartSize(4)
    tPlayer.addDeck(d2)
    assert tPlayer.hand_size == 3
    assert tPlayer.start_size == 4
    assert tPlayer.deck == d2
    pygame.event.post(tEvents[0])
    tPlayer.update(pygame.event.poll())
    assert tPlayer.health == 5
    pygame.event.post(tEvents[1])
    tPlayer.update(pygame.event.poll())
    assert tPlayer.energy == 2

def test_bview():
    tPlayer.setEnergy(3)
    assert tPlayer.rect == tBView.player_slot
    assert tEnemy.rect == tBView.enemy_slot
    pygame.event.post(tEvents[2])
    tBView.handle(pygame.event.poll())
    assert tPlayer.energy == 4

