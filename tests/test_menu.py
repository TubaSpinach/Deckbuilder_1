import pygame, project.menu
from project.main import load_png

tMenu = project.menu.Menu(load_png('test_background.png'))

def test_menu():
    assert isinstance(tMenu.image,pygame.surface.Surface)
    assert isinstance(tMenu.rect,pygame.Rect)
