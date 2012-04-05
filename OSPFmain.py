import pygame
from pygame.locals import *
from main import packets
from Router import Router
from Subnet import Subnet

"""
OSPF

Routers send out packets exchanging distance vector information, building their
routing tables. Note that IP addresses are associated with an interface (one
side of a link).
"""

def OSPFmkDevice(screen, x, y, id):
    if id in '1234567890':
        subnet =  Subnet(screen, x, y)
        subnet.IP = "192.168."+str(ord(list(id)[0]))+".0/24"
        return subnet
    else:
        router = Router(screen, x, y)
        router.IP = str(ord(list(id)[0]))
        router.selected = router.IP == "66"
        return router

def OSPFconfigure(devices, links):
    for device in filter(lambda d: not isinstance(d, Subnet), devices):
        for link in device.links:
            subnet = link.other(device)
            if isinstance(subnet, Subnet):
                IP = subnet.IP[:-4]+device.IP
                device.interfaces[link] = IP
                device.table[IP] = (0, None)
                               #IP -> (distance, link)    
                if len(device.links)==1:
                    device.IP = IP

    for device in filter(lambda d: not isinstance(d, Subnet), devices):
        if len(device.IP) < 4:
            device.IP = "192.168.*."+device.IP
                

packets(topology="OSPFtopology.txt", mkDevice=OSPFmkDevice, configure=OSPFconfigure)
