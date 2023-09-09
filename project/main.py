#TODO
#set up virtual environment
#modules: map.py
#add a win / loss screen or menu
#test json uses in conf_dict and card_dict
#add unit tests for play.py, menu.py
#images: player.png, enemy.png, strike.png, bash.png
#right now, Enemy.image should be changed for each enemy. Keep?


try:
    import sys, os, pygame, json
    import menu
    import play
except ImportError as err:
    print(f"Couldn't load all modules: {err}.")
    sys.exit(2)

settings = os.path.join('project','res','settings.txt')
card_lib = os.path.join('project','res', 'card_lib.txt')
conf_dict = {}
card_dict = {}

def load_json(file):
    try: 
        with open(file) as f:
            target_dict = json.load(f)
        return target_dict
    except FileNotFoundError as err:
        print(f"Couldn't load file {err}")
        return {}

conf_dict = load_json(settings)
card_dict = load_json(card_lib)

def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join('project',"res", name)
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

# pygame setup
pygame.init()
screen = pygame.display.set_mode((conf_dict['WIDTH'], conf_dict['HEIGTH']))
clock = pygame.time.Clock()
running = True

#has to come after display initialization
GameMenu = menu.Menu(load_png("background.png"))
newGameButton = menu.Button('newGame','New Game',load_png("button.png"),load_png("button_down.png"))
GameMenu.add(newGameButton)

deck_list = []
#will also be instantiated elsewhere later on
for i in range(0,6):
    deck_list.append(play.CardFactory(card_dict['strike']))

for i in range(0,4):
    deck_list.append(play.CardFactory(card_dict['bash']))


#probably will be instantiated elsewhere later on
Player = play.Character('Player',load_png("player.png"),50,3,deck_list)
Enemy = play.Character('Enemy', load_png('enemy.png'),50,3,deck_list)

BattleScreen = play.BattleView(load_png("battle_background.png"),[Player,Enemy])

VIEWS = [GameMenu,BattleScreen]
currentView = VIEWS[0]

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.name == 'newGame':
            currentView = VIEWS[1]
        elif event.name == "loss":
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