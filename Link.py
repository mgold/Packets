import pygame
from pygame.locals import *
from math import sin, cos, atan2, pi

class Link(pygame.sprite.Sprite):
    """
    Link - Moves Packets between Devices

    Subclassing notes
    Implement packet loss in send by only sometimes calling super.
    There is currently no way to change the speed of packet travel.
    You can change self.weight in mkLink.
    """
    
    def __init__ (self, screen, d1, d2):
        self.screen = screen
        self.d1 = d1
        self.d2 = d2
        self.pos1 = d1.pos
        self.pos2 = d2.pos

        #Don't ask unless you like trig
        theta = atan2(self.pos2[0] - self.pos1[0], self.pos1[1] - self.pos2[1])
        alpha = atan2(self.pos1[0] - self.pos2[0], self.pos2[1] - self.pos1[1])
        tau = 2*pi #tauday.com
        for angle in [theta, alpha]:
            if angle < 0:
                angle += tau
        speed = 5
        #Payoff: dx and dy to either end at constant speed
        self.toPos1 = (-speed * sin(theta), speed * cos(theta))
        self.toPos2 = (-speed * sin(alpha), speed * cos(alpha))

        self.thickness = 5
        self.color = (128, 128, 128) 

        self.packets = []
        self.weight = 1

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
