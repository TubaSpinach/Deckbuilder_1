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
for i in range(0,10):
    deck_list.append(play.CardFactory(card_dict['strike']))

tDeck = play.Deck(deck_list)

tPlayer = play.Character("Player",load_png("player.png"),10,3,tDeck)
tEnemy = play.Character("Enemy",load_png("enemy.png"),10,3,tDeck)
tBView = play.BattleView(load_png("background.png"))
tBView.add(tPlayer)
tBView.add(tEnemy)
tBView.arrange()

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