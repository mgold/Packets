import pygame
from pygame.locals import *
from core.Device import Device

class Text(Device):
    """
    Text - Virus

    Displays text. Not really a device, just a subclass of it to make things
    easier. 
    """
    def __init__ (self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y

        self.font = pygame.font.SysFont(u'couriernew,courier', 18, bold=True)
        self.color = (0, 128, 255) #Change if you like

    def update(self):
        pass
        #Implement me!

    def draw(self):
        pass
        #Implement me!
