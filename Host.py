import pygame
from pygame.locals import *
from Packet import Packet
from Router import Router
from copy import copy

class Host(Router):
    def __init__ (self, screen, x, y):
        Router.__init__(self, screen, x, y)

        self.radius = 12
        self.color = (0, 96, 191) 
       #self.packetColor = (128, 128, 191)

        self.selectable = False

    def receive(self, packet):
        if packet.protocol == "OSPF":
            pass

    def drawIPs(self):
        address = self.IPfont.render(self.IP, 1, self.color)
        self.screen.blit(address, (self.pos[0] - 75, self.pos[1] + self.radius + 4)) 
    
    def drawTable(self):
        x = 40
        y = 470
        header = self.IPfont.render("Forwarding Table for Host "+self.IP, 1, self.selectColor)
        local = self.IPfont.render(self.IP.ljust(16)+"localhost", 1, self.color)
        outside = self.IPfont.render("0.0.0.0/0       "+self.IP, 1, self.color)
        footer = self.IPfont.render("2 entries", 1, self.selectColor)

        self.screen.blit(header,  (x, y))
        self.screen.blit(local,   (x, y+20))
        self.screen.blit(outside, (x, y+40))
        self.screen.blit(footer,  (x, y+60))
       
    def drawTableSize(self):
        pass

    def __repr__(self):
        return "Host: "+self.IP
