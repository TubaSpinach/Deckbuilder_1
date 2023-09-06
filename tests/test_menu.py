import pygame, project.menu, os, json
from project.main import load_png

tMenu = project.menu.Menu(load_png('test_background.png'))
tButton1 = project.menu.Button('test_Press',"Test Button",load_png('test_button.png'),load_png('test_button_down.png'))
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