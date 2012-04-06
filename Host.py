import pygame
from pygame.locals import *
from Packet import Packet
from Device import Device
from copy import copy

class Host(Device):
    def __init__ (self, screen, x, y):
        Device.__init__(self, screen, x, y)

        self.radius = 12
        self.color = (0, 96, 191) 
        self.packetColor = (128, 128, 191)

        #Similar to router
        self.font = pygame.font.Font(None, 28)
        self.IPfont = pygame.font.SysFont(u'couriernew,courier', 18, bold=True)
        self.timer = 0

        self.selectable = False
        self.name = ""
        self.names = {}

    def update(self):
        pass

    def receive(self, packet):
        pass

    def draw(self):
        if self.selected:
            self.drawTable()
            pygame.draw.circle(self.screen, self.selectColor, self.pos, self.radius+3) 
        pygame.draw.circle(self.screen, self.color, self.pos, self.radius) 
        address = self.IPfont.render(self.IP, 1, self.color)
        self.screen.blit(address, (self.pos[0] - 75, self.pos[1] + self.radius + 4)) 
        if self.name:
            name = self.font.render(self.name[0], 1, (0,0,0))
            self.screen.blit(name, (self.pos[0] - 7, self.pos[1] - 10))

    def drawTable(self):
        pass

    def __repr__(self):
        return "Host: "+self.IP
