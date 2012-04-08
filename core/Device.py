import pygame
from pygame.locals import *
from Packet import Packet
from random import randint, choice

class Device(pygame.sprite.Sprite):
    """
    Device - Core
    
    Superclass of hosts, routers, servers, etc.
    
    When no overriden by a subclass, sends packets at random and forwards or
    drops packets at random.

    Subclassing note: treat self.links as read-only. 
    """
    def __init__ (self, screen, x, y):
        self.screen = screen
        self.pos = (x, y) 
        self.radius = 20
        self.rect = pygame.Rect(x-self.radius, y-self.radius, 2*self.radius, 2*self.radius)

        self.color = (0, 128, 255) 

        self.links = [] #connected interfaces

    def update(self):
        if randint(0, 250) == 1:
            choice(self.links).send(Packet(self.screen, self.pos[0], self.pos[1]), self)

    def receive(self, packet):
        if randint(0, 3) != 1:
            choice(filter(lambda l: l != packet.link, self.links)).send(packet, self)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.pos, self.radius) 
