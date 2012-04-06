import pygame
from pygame.locals import *
from Packet import Packet
from Router import Router
from copy import copy

class DNS(Router):
    def __init__ (self, screen, x, y):
        Router.__init__(self, screen, x, y)

        self.color = (191, 96, 96) 
        self.packetColor = (191, 128, 128)

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
                packetCopy.destination = interface[:-2]+"255"
                packetCopy.payload["DNS"] = (0, link)
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

    def drawIPs(self):
        address = self.IPfont.render(self.IP, 1, self.color)
        self.screen.blit(address, (self.pos[0] - 75, self.pos[1] + self.radius + 4)) 
    
    def drawTable(self):
        x = 40
        y = 470
        dy = 19
        header = self.IPfont.render("Name Table for DNS "+self.IP, 1, self.selectColor)
        self.screen.blit(header,  (x, y))

        for name, IP in self.names.iteritems():
            label = self.IPfont.render(name.ljust(8)+IP, 1, self.color)
            y += dy
            self.screen.blit(label, (x, y))
            
        footer = self.IPfont.render(str(len(self.names))+" entries", 1, self.selectColor)
        self.screen.blit(footer,  (x, y+dy))
       
    def drawLabel(self):
        return None

    def __repr__(self):
        return "DNS: "+self.IP
