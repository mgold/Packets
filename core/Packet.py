import pygame
from pygame.locals import *

class Packet(pygame.sprite.Sprite):
    """
    Packet - Core
    
    Visual representation of data transfer, as well as a container for that
    data.  Indeed, the time of arrival of a packet at its destination is not
    precalculated by determined by the onscreen position of the sprite.

    Extention notes:
    Avoid subclassing.
    Custom subclasses of Device should create Packets, configure internal
    variables (color and protocol are of interest), and add additional member
    variables to carry protocol-specific data.
    """

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
            if self.targdev:
                self.targdev.receive(self)

        self.rect = pygame.Rect(self.x, self.y, self.side, self.side)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def __str__(self):
        toreturn = "Packet of protocol "+self.protocol
        if self.destination:
            toreturn += ", destination "+str(self.destination)
        toreturn += "."
        return toreturn
