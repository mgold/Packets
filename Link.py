import pygame
from pygame.locals import *

class Link(pygame.sprite.Sprite):

    def __init__ (self, screen, d1, d2):
        self.screen = screen
        self.d1 = d1
        self.d2 = d2
        self.pos1 = d1.pos
        self.pos2 = d2.pos
        self.thickness = 5
        self.color = (128, 128, 128) 

        self.packets = []

    def update(self):
        for packet in self.packets:
            packet.update()

    def draw(self):
        pygame.draw.line(self.screen, self.color, self.pos1, self.pos2, self.thickness)
        for packet in self.packets:
            packet.draw()
