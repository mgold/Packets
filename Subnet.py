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
            weight = packet.link.weight
            for entry in pl:
                if entry not in self.table or pl[entry][0] + weight <= self.table[entry][0]:
                    self.table[entry] = (pl[entry][0]+ weight, packet.link)
            for link in self.links:
                if link is not packet.link:
                    link.send(copy(packet), self)
        elif packet.protocol == "DNS Request":
            if "DNS" in self.table:
                self.table["DNS"][1].send(copy(packet), self)
        elif packet.protocol == "DNS Response":
            destination = packet.destination[:10]
            if self.IP[:10] == destination:
                for link in self.links:
                    if link.other(self).IP == packet.destination:
                        link.send(packet, self)
            elif destination in self.table:
                self.table[destination][1].send(packet, self)


    def draw(self):
        pass
