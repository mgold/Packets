import pygame
from pygame.locals import *

def abs(x):
    if x < 0:
        return -x
    return x

class Packet(pygame.sprite.Sprite):

    def __init__ (self, screen, x, y):
        self.side = 12
        self.halfside = self.side//2
        self.color = (255, 128, 128) 
        
        self.screen = screen
        self.x = x - self.halfside
        self.y = y - self.halfside
        self.dx = self.dy = 0
        self.targx = self.targy = 0

        self.link = None
        self.destination = None

        self.rect = pygame.Rect(self.x, self.y, self.side, self.side)
        
        self.protocol = "generic"

    def update(self):
        self.x += self.dx
        self.y += self.dy 
        targetSize = 10
        if abs(self.x - self.targx) < targetSize and (
           abs(self.y - self.targy) < targetSize):
            if self.link:
                self.link.remove(self)
            if self.destination:
                self.destination.receive(self)

        self.rect = pygame.Rect(self.x, self.y, self.side, self.side)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
