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
        self.packetColor = (128, 128, 191)

        self.font = pygame.font.Font(None, 28)
        self.selectable = False
        self.name = ""
        self.names = {}


    def update(self):
        if self.name == "Alice" and "Bob" not in self.names:
            if self.timer == 0:
                request = Packet(self.screen, self.pos[0], self.pos[1])
                request.color = (191, 128, 128)
                request.protocol = "DNS Request"
                request.source = self.IP
                request.destination = "DNS"
                request.request = "Bob"
                self.link.send(request, self)
                self.timer = 250
            else:
                self.timer -= 1

    def receive(self, packet):
        if packet.protocol == "OSPF":
            pass
        elif packet.protocol == "DNS Response":
            if packet.code != 404:
                self.names[packet.response[0]] = packet.response[1] 

    def drawIPs(self):
        address = self.IPfont.render(self.IP, 1, self.color)
        self.screen.blit(address, (self.pos[0] - 75, self.pos[1] + self.radius + 4)) 
    
    def drawTable(self):
        x = 40
        y = 470
        dy = 19
        headerText = "Name Table for Host "+self.IP
        if self.name:
            headerText += " ("+self.name+")"
        header = self.IPfont.render(headerText, 1, self.selectColor)
        self.screen.blit(header, (x, y))

        for name, IP in self.names.iteritems():
            label = self.IPfont.render(name.ljust(8)+IP, 1, self.color)
            y += dy
            self.screen.blit(label, (x, y))
            
        footer = self.IPfont.render(str(len(self.names))+" entries", 1, self.selectColor)
        self.screen.blit(footer,  (x, y+dy))
       
    def drawLabel(self):
        if self.name:
            name = self.font.render(self.name[0], 1, (0,0,0))
            self.screen.blit(name, (self.pos[0] - 7, self.pos[1] - 10))

    def __repr__(self):
        return "Host: "+self.IP
