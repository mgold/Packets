import pygame
from pygame.locals import *
from Packet import Packet
from Router import Router
from copy import copy

class Host(Router):
    def __init__ (self, screen, x, y):
        Router.__init__(self, screen, x, y)

        self.color = (0, 96, 191) 
       #self.packetColor = (128, 128, 191)

    def drawIPs(self):
        address = self.IPfont.render(self.IP, 1, self.color)
        self.screen.blit(address, (self.pos[0] - 75, self.pos[1] + self.radius + 4)) 
        
    def __repr__(self):
        return "Host: "+self.IP
