import pygame, os
from .. import menu

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


pygame.init()
screen = pygame.display.set_mode((1280, 720))


tMenu = menu.Menu(load_png('background.png'))
tButton1 = menu.Button('test_Press',"Test Button",load_png('button.png'),load_png('button_down.png'))
resFolder = os.path.join('project','res')

def test_menu():
    #testing __init__ worked properly
    assert isinstance(tMenu.image,pygame.surface.Surface)
    assert isinstance(tMenu.rect,pygame.Rect)

    #testing add() and draw() member functions work properly
    tMenu.add(tButton1)
    assert len(tMenu.sprites) > 0 
    assert isinstance(tMenu.draw(),list)

def test_button():
    #testing __init__
    assert isinstance(tButton1.image,pygame.surface.Surface)
    assert isinstance(tButton1.image_down,pygame.surface.Surface)
    assert isinstance(tButton1.rect,pygame.Rect)
    assert isinstance(tButton1.action,pygame.event.Event)

    testClick = tButton1.rect.center
    testEvent = pygame.event.Event('MOUSEBUTTONDOWN',{'pos':(testClick), 'button': 1})
    #testing being pressed
    tButton1.update(testEvent)
    assert tButton1.action in pygame.event.get()