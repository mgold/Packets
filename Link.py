import pygame
from pygame.locals import *
from math import sin, cos

class Link(pygame.sprite.Sprite):

    def __init__ (self, screen, d1, d2):
        self.screen = screen
        self.d1 = d1
        self.d2 = d2
        self.pos1 = d1.pos
        self.pos2 = d2.pos

        vector1 = (self.pos1[0] - self.pos2[0], self.pos1[1] - self.pos2[1])
        vector2 = (self.pos2[0] - self.pos1[0], self.pos2[1] - self.pos1[1])
        speed = .01
        #self.toPos1 = (speed // vector1[0], speed // vector1[1])
        #self.toPos2 = (speed // vector1[0], speed // vector1[1])
        self.toPos1 = (speed * vector1[0], speed * vector1[1])
        self.toPos2 = (speed * vector2[0], speed * vector2[1])

        self.thickness = 5
        self.color = (128, 128, 128) 

        self.packets = []

    def send(self, packet, sender):
        if sender == self.d1:
            packet.destination = self.d2
            packet.dx = self.toPos2[0]
            packet.dy = self.toPos2[1]
            packet.link = self
            packet.targx = self.pos2[0]
            packet.targy = self.pos2[1]
            self.packets.append(packet)

        elif sender == self.d2:
            packet.destination = self.d1
            packet.dx = self.toPos1[0]
            packet.dy = self.toPos1[1]
            packet.link = self
            packet.targx = self.pos1[0]
            packet.targy = self.pos1[1]
            self.packets.append(packet)

    def remove(self, packet):
        self.packets.remove(packet)

    def update(self):
        for packet in self.packets:
            packet.update()

    def draw(self):
        pygame.draw.line(self.screen, self.color, self.pos1, self.pos2, self.thickness)
        for packet in self.packets:
            packet.draw()
