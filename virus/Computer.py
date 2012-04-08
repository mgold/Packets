import pygame
from pygame.locals import *
from core.Packet import Packet
from core.Device import Device
from copy import copy

class Computer(Device):
    def __init__ (self, screen, x, y, radius=20):
        Device.__init__(self, screen, x, y)
        self.radius = radius

        self.owner = None
        self.count = 0
        self.color = (96, 96, 96) 

        self.selectColors = [(0,0,0), (64, 64, 64), (128, 128, 128), (223, 223, 233)]
        self.selectLevel = 0

        self.font = pygame.font.Font(None, 36)

        self.timeToNewPacket = 0
        self.maxTimeToNewPacket = 1500//radius

        self.timeToSend = 0
        self.maxTimeToSend = 3

        self.queues = {} #Created by configure
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
                else:
                    for link, count in self.queues.iteritems():
                        if count and self.count:
                            link.send(self.packet(), self)
                            self.queues[link] -= 1
                            self.count -= 1
                self.timeToSend = self.maxTimeToSend
            else:
                self.timeToSend -= 1

    def receive(self, packet):
        if self.owner and self.owner == packet.owner:
            self.count += 1
        else:
            self.count -= 1
            if self.count == 0:
                self.changeOwner(packet.owner)

    def attack(self, target):
        for link in self.links:
            if link.other(self) == target:
                if self.selectLevel == 3:
                    self.forwardOn = link
                else:
                    self.forwardOn = None
                    self.queues[link] += int(self.selectLevel * self.count / 3)

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
        else:
            self.color = (0, 255, 0)

    def draw(self):
        if self.selectLevel:
            pygame.draw.circle(self.screen, self.selectColors[self.selectLevel], self.pos, self.radius+5) 

        pygame.draw.circle(self.screen, self.color, self.pos, self.radius) 

        counts  = self.font.render(str(self.count), 1, (0,0,0))
        if self.count < 10:
            self.screen.blit(counts, (self.pos[0] - 7, self.pos[1] - 10))
        else:
            self.screen.blit(counts, (self.pos[0] - 13, self.pos[1] - 10))

    def __repr__(self):
        return "<%s instance at %s with %s %s packets>" % (self.__class__.__name__, id(self), str(self.count), self.owner)
