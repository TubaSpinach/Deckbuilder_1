#TODO
#modules: map.py
#adjust menu.draw to draw to a reasonable size
#determine if I will use a set resolution or if there's an option for resizability in pygame
#add a win / loss screen or menu
#images:
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
deck_list = []
currentView = None
running = True
views = []

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

#initialize the game
def start_up():

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((conf_dict['WIDTH'], conf_dict['HEIGTH']))
    clock = pygame.time.Clock()
    

    #has to come after display initialization
    GameMenu = menu.Menu(load_png("background.png"),screen)
    newGameButton = menu.Button('newGame','New Game',load_png("button.png"),load_png("button_down.png"))
    GameMenu.add(newGameButton)
    GameMenu.arrange()


    #will also be instantiated elsewhere later on
    for i in range(0,6):
        deck_list.append(play.CardFactory(card_dict['strike']))

    for i in range(0,4):
        deck_list.append(play.CardFactory(card_dict['bash']))


    #probably will be instantiated elsewhere later on
    Player = play.Character('Player',load_png("player.png"),50,3,deck_list)
    Enemy = play.Character('Enemy', load_png('enemy.png'),50,3,deck_list)

    BattleScreen = play.BattleView(load_png("battle_background.png"))
    BattleScreen.add(Player)
    BattleScreen.add(Enemy)
    BattleScreen.arrange()

    views = [GameMenu,BattleScreen]
    
    return clock, screen, views[0]

tick, display, currentView = start_up()

def handle_events(event):
    if event.type == pygame.QUIT:
            return False
    elif event.type == pygame.USEREVENT:
        if event.dict['name'] == 'newGame':
            currentView = views[1]
        elif event.dict['name'] == "loss":
            currentView = views[0]
        #elif event.dict['name'] == "win":
        #    currentView = VIEWS[2]
        else:
            currentView.update(event)
    return True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        running = handle_events(event)

    # RENDER YOUR GAME HERE
    currentView.clear(display,currentView.image)
    currentView.draw(display)
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    tick.tick(60)  # limits FPS to 60

pygame.quit()