import pygame
from pygame.locals import *

class Packet(pygame.sprite.Sprite):

    def __init__ (self, screen, x, y):
        self.screen = screen
        self.pos = (x, y) 
        self.side = 10
        self.color = (255, 128, 128) 

    def update(self):
        self.rect = pygame.Rect(self.pos, (self.side, self.side))

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
