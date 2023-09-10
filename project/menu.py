#TODO
#
#modify Menu.add() to position buttons in equal parts of the menu surface
#clean up


import pygame

#a class to hold buttons and take names 8)
class Menu(pygame.sprite.RenderUpdates):
    def __init__(self,loaded_image):
        #make sure to call default class init first
        pygame.sprite.RenderUpdates.__init__(self)
        self.image, self.rect = loaded_image
    
    
    def draw(self, aSurface):
        #draw self first; children go on top
        aSurface.blit(self.image,self.rect)
        return super(Menu, self).draw(aSurface)
        
    def arrange(self):
        if len(self) > 0:
            for i, sprite in enumerate(self.sprites()):
                sprite.rect.centerx = self.rect.centerx
                sprite.rect.y = self.rect.centery - (len(self) - 1)*50*i
    #don't need to define an update method, already in sprite.RenderUpdates

class Button(pygame.sprite.Sprite):
    def __init__(self, action, text, loaded_image_up,loaded_image_down):
        pygame.sprite.Sprite.__init__(self)
        #we'll use the load_png function to load the images
        self.image, self.rect = loaded_image_up
        self.image_down, self.image_down_rect = loaded_image_down

        #set up the button text
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render(text,1,(1,1,1))
        #center it in the button; this doesn't work, and I need to figure out what to do with that
        #self.text.center = self.rect.center
        #the event placed on cue when pressed!
        self.action = pygame.event.Event(pygame.USEREVENT, {'name':'newGame','action': action})
    
    #activate on mouseclick!
    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseClick = event.pos
            if(self.rect.collidepoint(mouseClick)):
                pygame.event.post(self.action)
                return True
        return False
    


