import pygame
from pygame.locals import *
from core.Packet import Packet
from core.Device import Device
from copy import copy

class Computer(Device):
    def __init__ (self, screen, x, y, radius=20):
        Device.__init__(self, screen, x, y)
        self.radius = radius
        self.rect = pygame.Rect(x-self.radius, y-self.radius, 2*self.radius, 2*self.radius)

        self.owner = None
        self.count = 0
        self.color = (96, 96, 96) 

        self.selectColor = (223, 223, 233)
        self.selected = False

        self.font = pygame.font.Font(None, 36)

        self.timeToNewPacket = 0
        self.maxTimeToNewPacket = 1500//radius

        self.timeToSend = 0
        self.maxTimeToSend = 3

        self.forwardOn = None

    def update(self):
        if self.owner:
            if self.timeToNewPacket == 0:
                self.count += 1
                self.timeToNewPacket = self.maxTimeToNewPacket
            else:
                self.timeToNewPacket -= 1

            if self.timeToSend == 0:
                if self.forwardOn:
                    if self.count:
                        self.forwardOn.send(self.packet(), self)
                        self.count -= 1
                self.timeToSend = self.maxTimeToSend
            else:
                self.timeToSend -= 1
            
            if self.owner == "GREEN":
                for link in self.links:
                    if link.other(self).owner != self.owner:
                        self.attack(link.other(self))
                        return


    def receive(self, packet):
        if self.owner and self.owner == packet.owner:
            self.count += 1
        else:
            self.count -= 1
            if self.count < 0:
                self.changeOwner(packet.owner)
                self.forwardOn = None

    def attack(self, target):
        if target == self:
            self.forwardOn = None
            return
        for link in self.links:
            if link.other(self) == target:
                self.forwardOn = link
                if (target.owner == self.owner
                    and target.forwardOn 
                    and target.forwardOn.other(target) == self): 
                    target.forwardOn = None #Prevent forwarding loops

    def packet(self):
        packet = Packet(self.screen, self.pos[0], self.pos[1])
        packet.color = self.color
        packet.owner = self.owner
        return packet

    def changeOwner(self, newOwner, count=0):
        self.count = count
        self.owner = newOwner
        if newOwner == "RED":
            self.color = (255, 0, 0)
            self.maxTimeToSend = 3
        else:
            self.color = (0, 255, 0)
            self.maxTimeToSend = 4

    def draw(self):
        if self.selected:
            pygame.draw.circle(self.screen, self.selectColor, self.pos, self.radius+5) 

        pygame.draw.circle(self.screen, self.color, self.pos, self.radius) 

        counts  = self.font.render(str(self.count), 1, (0,0,0))
        if self.count < 10:
            self.screen.blit(counts, (self.pos[0] - 7, self.pos[1] - 10))
        elif self.count < 100:
            self.screen.blit(counts, (self.pos[0] - 13, self.pos[1] - 10))
        else:
            self.screen.blit(counts, (self.pos[0] - 20, self.pos[1] - 10))

    def __repr__(self):
        return "<%s instance at %s with %s %s packets>" % (self.__class__.__name__, id(self), str(self.count), self.owner)
