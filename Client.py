import pygame
from pygame.locals import *
from Packet import Packet
from Host import Host
from copy import copy
from IP import DNSIP

class Client(Host):
    def __init__ (self, screen, x, y):
        Host.__init__(self, screen, x, y)
        self.selectable = True        
        self.corespondent = self.name
        self.timer = 0

    def update(self):
        if self.corespondent not in self.names:
            if self.timer == 0:
                request = Packet(self.screen, self.pos[0], self.pos[1])
                request.color = (191, 128, 128)
                request.protocol = "DNS Request"
                request.source = self.IP
                request.destination = DNSIP()
                request.request = self.corespondent
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

    def drawTable(self):
        x = 40
        y = 470
        dy = 19
        headerText = "Name Table for Host "+str(self.IP)[:-3]
        if self.name:
            headerText += " ("+self.name+")"
        header = self.IPfont.render(headerText, 1, self.selectColor)
        self.screen.blit(header, (x, y))

        for name, IP in self.names.iteritems():
            label = self.IPfont.render(name.ljust(8)+str(IP)[:-3], 1, self.color)
            y += dy
            self.screen.blit(label, (x, y))
            
        footer = self.IPfont.render(str(len(self.names))+" entries", 1, self.selectColor)
        self.screen.blit(footer,  (x, y+dy))
       
    def __repr__(self):
        return "<%s instance at %s with IP %s (%s)>" % (self.__class__.__name__, id(self), self.IP, self.name)
