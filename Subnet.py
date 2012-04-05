import pygame
from pygame.locals import *
from Packet import Packet
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

    def receive(self, packet):
        if packet.protocol == "OSPF":
            pl = packet.payload
            for entry in pl:
                if entry not in self.table or pl[entry][0] + 1 < self.table[entry]:
                        self.table[entry] = (pl[entry][0]+1, pl[entry][1])
            for link in self.links:
                if link is not packet.link:
                    link.send(copy(packet), self)
    
    def draw(self):
        pass
