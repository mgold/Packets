import pygame
from pygame.locals import *
from core.Packet import Packet
from Router import Router
from copy import copy

class Subnet(Router):
    """Subnet

    A dirty hack. Allows many-to-many join of routers, with the hopes of
    assigning IPs to interfaces instead of devices.

    """

    def __init__ (self, screen, x, y):
        Router.__init__(self, screen, x, y)
        self.selectable = False

    def update(self):
        pass

    def sendLocal(self, packet):
        for link in self.links:
            if link.other(self).IP == packet.destination:
                link.send(packet, self)

    def broadcast(self, packet):
        for link in self.links:
            if link is not packet.link:
                link.send(copy(packet), self)

    def draw(self):
        pass
