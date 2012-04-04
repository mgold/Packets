import pygame
from pygame.locals import *

class Device(pygame.sprite.Sprite):

    def __init__ (self, screen, x, y):
        self.screen = screen
        self.pos = (x, y) 
        self.radius = 20
        self.color = (0, 128, 255) 
        
        self.links = [] #connected interfaces

    def update(self):
        pass

    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.pos, self.radius) 
