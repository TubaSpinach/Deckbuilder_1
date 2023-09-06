#TODO
#set up virtual environment
#modules: map.py
#add a win / loss screen or menu
#test json uses in conf_dict and card_dict
#add unit tests for play.py, menu.py
#images: background.png, button.png, battle_background.png, player.png, enemy.png, strike.png, bash.png
#alts: button_pressed.png

try:
    import sys, os, pygame, json
    import menu.py, play.py
except ImportError:
    print(f"Couldn't load all modules.")
    sys.exit(2)

settings = 'res/settings.txt'
conf_dict = {}
card_dict = {}
with open(settings) as f:
    conf_dict = json.load(f)

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


GameMenu = menu.Menu(load_png("background.png"))
newGameButton = menu.Button('newGame','New Game',load_png("button.png"),load_png("button_down.png"))
GameMenu.add(newGameButton)

BattleScreen = play.BattleView(load_png("battle_background.png"))

#probably will be instantiated elsewhere later on
Player = play.Character('Player',"player.png",50,3,BattleScreen)
Enemy = play.Character('Enemy','enemy.png',50,3,BattleScreen)

with open(os.path.join('res',card_json)) as f:
    card_dict = json.load(f)

deck_list = []
#will also be instantiated elsewhere later on
for i in range(0,6):
    deck_list.append(play.CardFactory(card_dict['strike']))

for i in range(0,4):
    deck_list.append(play.CardFactory(card_dict['bash']))
Deck = play.Deck(deck_list)

VIEWS = [GameMenu,BattleScreen]
# pygame setup
pygame.init()
screen = pygame.display.set_mode((conf_dict['WIDTH'], conf_dict['HEIGTH']))
clock = pygame.time.Clock()
running = True
currentView = VIEWS[0]

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == "newGame":
            currentView = VIEWS[1]
        elif event.type == "loss":
            currentView = VIEWS[0]
        #elif event.type == "win":
        #    currentView = VIEWS[2]
        else:
            currentView.update()

    # RENDER YOUR GAME HERE
    currentView.clear()
    currentView.draw()
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()