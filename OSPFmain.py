import pygame
from pygame.locals import *
from main import packets
from Router import Router
from Junction import Junction

"""
OSPF - well, not quite.

Currently it's more a cross between OSPF and ARP, because IPs are associated
with Devices rather than interfaces (sides of Links). I'm working on it.
"""

def OSPFmkDevice(screen, x, y, id):
    if id in '1234567890':
        return Junction(screen, x, y)
    else:
        router = Router(screen, x, y)
        router.IP = "192.168.0."+str(ord(list(id)[0]))
        router.table = {router.IP : (0, None)}
                        #IP -> (distance, link)    
        return router


packets(topology="OSPFtopology.txt", mkDevice=OSPFmkDevice)
