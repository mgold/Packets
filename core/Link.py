import pygame
from pygame.locals import *
from math import sin, cos, atan2, pi

class Link(pygame.sprite.Sprite):
    """
    Link - Core
    
    Moves Packets between Devices.

    Extention notes:
    Avoid subclassing if at all possible.
    In your mkLink, use the optional parameter in the constructor to change the speed of packet
    travel. Set self.weight after instatiation. Make changes in topology with self.active.
    """
    
    def __init__ (self, screen, d1, d2, speed=5):
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
        #Payoff: dx and dy to either end at constant speed
        self.toPos1 = (-speed * sin(theta), speed * cos(theta))
        self.toPos2 = (-speed * sin(alpha), speed * cos(alpha))

        #Exact zeroes are better than 3.06161699787e-16
        if abs(self.toPos1[0]) < 0.001:
            self.toPos1 = (0, self.toPos1[1])
        if abs(self.toPos1[1]) < 0.001:
            self.toPos1 = (self.toPos1[0], 0)
        if abs(self.toPos2[0]) < 0.001:
            self.toPos2 = (0, self.toPos2[1])
        if abs(self.toPos2[1]) < 0.001:
            self.toPos2 = (self.toPos2[0], 0)

        self.thickness = 5
        self.color = (128, 128, 128) 

        self.packets = []
        self.weight = 1
        self.active = True

    def send(self, packet, sender):
        if self.active:
            if sender == self.d1:
                packet.targdev = self.d2
                packet.x = self.pos1[0] - packet.halfside
                packet.y = self.pos1[1] - packet.halfside
                packet.dx = self.toPos2[0]
                packet.dy = self.toPos2[1]
                packet.link = self
                packet.targx = self.pos2[0]
                packet.targy = self.pos2[1]
                self.packets.append(packet)

            elif sender == self.d2:
                packet.targdev = self.d1
                packet.x = self.pos2[0] - packet.halfside
                packet.y = self.pos2[1] - packet.halfside
                packet.dx = self.toPos1[0]
                packet.dy = self.toPos1[1]
                packet.link = self
                packet.targx = self.pos1[0]
                packet.targy = self.pos1[1]
                self.packets.append(packet)

    def remove(self, packet):
        self.packets.remove(packet)

    def other(self, device):
        if device == self.d1:
            return self.d2
        elif device == self.d2:
            return self.d1
        else:
            return None

    def update(self):
        if self.active:
            for packet in self.packets:
                packet.update()
        else:
            self.packets = []

    def draw(self):
        if self.active:
            pygame.draw.line(self.screen, self.color, self.pos1, self.pos2, self.thickness)
            for packet in self.packets:
                packet.draw()

    def __repr__(self):
        return "Link between "+self.d1.IP+" and "+self.d2.IP+"\n"
