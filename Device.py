import pygame
from pygame.locals import *
from Packet import Packet
from random import randint, choice

class Device(pygame.sprite.Sprite):

    def __init__ (self, screen, x, y):
        self.screen = screen
        self.pos = (x, y) 
        self.radius = 20
        self.color = (0, 128, 255) 
        
        self.links = [] #connected interfaces

    def update(self):
        if randint(0, 20) == 5:
            choice(self.links).send(Packet(self.screen, self.pos[0], self.pos[1]), self)

    def receive(self, packet):
        pass

    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.pos, self.radius) 
