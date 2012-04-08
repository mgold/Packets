import pygame
from pygame.locals import *
from core.Packet import Packet
from Router import Router
from copy import copy

class Subnet(Router):
    """
    Subnet - Web

    Represents many-to-many joins of Links.
    
    Helps assign IP addresses to each interface, rather than each host. For
    this reason, every Link in the Web module connects one Subnet to one
    non-Subnet Device.
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
