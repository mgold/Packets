import pygame
from pygame.locals import *
from Packet import Packet
from Device import Device
from copy import copy

class Router(Device):
    def __init__ (self, screen, x, y):
        Device.__init__(self, screen, x, y)
        self.color = (0, 128, 128) 
        self.timer = 0
        
        self.packetColor = (128, 255, 128)

        self.IPfont = pygame.font.SysFont(u'couriernew,courier', 22, bold=True)
        self.font = pygame.font.Font(None, 36)

    def update(self):
        if self.timer == 0:
            packet = Packet(self.screen, self.pos[0], self.pos[1])
            packet.color = self.packetColor
            packet.payload = copy(self.table)
            packet.protocol = "OSPF"
            for link in self.links:
               link.send(copy(packet), self)
            self.timer = 250
        else:
            self.timer -= 1

    def receive(self, packet):
        if packet.protocol == "OSPF":
            pl = packet.payload
            for entry in pl:
                if entry not in self.table or pl[entry][0] + 1 < self.table[entry]:
                        self.table[entry] = (pl[entry][0]+1, pl[entry][1])
    
    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.pos, self.radius) 
        tableSize = self.font.render(str(len(self.table)), 1, (0,0,0))
        if len(self.table) < 10:
            self.screen.blit(tableSize, (self.pos[0] - 7, self.pos[1] - 10))
        else:
            self.screen.blit(tableSize, (self.pos[0] - 15, self.pos[1] - 10))
        address = self.IPfont.render(self.IP, 1, self.color)
        self.screen.blit(address, (self.pos[0] - 60, self.pos[1] + self.radius +10))
