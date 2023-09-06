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
