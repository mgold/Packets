import pygame
from pygame.locals import *
from core.Packet import Packet
from Router import Router
from copy import copy
from IP import DNSIP

class DNS(Router):
    def __init__ (self, screen, x, y):
        Router.__init__(self, screen, x, y)

        self.color = (191, 96, 96) 
        self.packetColor = (191, 128, 128)
        self.font = pygame.font.Font(None, 24)

        self.names = {}

    def update(self):
        if self.timer == 0:
            packet = Packet(self.screen, self.pos[0], self.pos[1])
            packet.color = (128, 255, 128)
            packet.payload = {}
            packet.protocol = "OSPF"
            for link in self.links:
                packetCopy = copy(packet)
                interface = self.interfaces[link]
                packetCopy.source = interface
                packetCopy.destination = interface.broadcast()
                packetCopy.payload[DNSIP()] = (0, link)
                link.send(packetCopy, self)
            self.timer = 250
        else:
            self.timer -= 1

    def receive(self, packet):
        if packet.protocol == "OSPF":
            pass
        elif packet.protocol == "DNS Request":
            respacket = Packet(self.screen, self.pos[0], self.pos[1])
            respacket.protocol = "DNS Response"
            respacket.destination = packet.source
            respacket.color = self.packetColor
            respacket.source = self.IP
            try:
                respacket.response = packet.request, self.names[packet.request]
                respacket.code = 200
            except KeyError: #Yes, I'm using HTTP codes for DNS. Shh.
                respacket.response = None
                respacket.code = 404
            packet.link.send(respacket, self)

    def drawTable(self):
        x = 40
        y = 470
        dy = 19
        header = self.IPfont.render("Name Table for DNS "+str(self.IP), 1, self.selectColor)
        self.screen.blit(header,  (x, y))

        for name, IP in self.names.iteritems():
            label = self.IPfont.render(name.ljust(8)+IP, 1, self.color)
            y += dy
            self.screen.blit(label, (x, y))
            
        footer = self.IPfont.render(str(len(self.names))+" entries", 1, self.selectColor)
        self.screen.blit(footer,  (x, y+dy))
       
    def drawLabel(self):
        self.screen.blit(self.font.render("DNS", 1, (0,0,0)), (self.pos[0] - self.radius + 2, self.pos[1] - 6))

    def __repr__(self):
        return "DNS: "+self.IP
