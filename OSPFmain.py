import pygame
from pygame.locals import *
from main import packets
from Router import Router
from Subnet import Subnet
from Host import Host
from DNS import DNS

"""
OSPF

Routers send out packets exchanging distance vector information, building their
routing tables. Note that IP addresses are associated with an interface (one
side of a link).
"""

def OSPFmkDevice(screen, x, y, id):
    if id.isdigit():
        subnet = Subnet(screen, x, y)
        subnet.IP = "192.168."+str(ord(list(id)[0]))+".0/24"
        return subnet
    elif id == "N":
        dns = DNS(screen, x, y)
        dns.IP = str(ord(list(id)[0]))
        return dns
    elif id.isupper():
        router = Router(screen, x, y)
        router.IP = str(ord(list(id)[0]))
        router.selected = router.IP == "66"
        return router
    elif id.islower():
        host = Host(screen, x ,y)
        host.IP = str(ord(list(id)[0]))
        if id == "q":
            host.name = "Alice"
            host.selectable = True
        if id == "x":
            host.name = "Bob"
            host.selectable = True
        return host
    else:
        print "Unrecognized unique identifier in sprite map"
        return None

def OSPFconfigure(devices, links):
    names = {}
    for device in filter(lambda d: not isinstance(d, Subnet), devices):
        for link in device.links:
            subnet = link.other(device)
            if isinstance(subnet, Subnet):
                IP = subnet.IP[:-4]+device.IP
                device.interfaces[link] = IP
                device.table[subnet.IP[:-5]] = (1, link)
                               #x.y.z -> (distance, link)    
            if len(device.links)==1:
                device.IP = IP
            if isinstance(device, Host):
                if device.name:
                    names[device.name] = device.IP
                
    for device in filter(lambda d: not isinstance(d, Subnet), devices):
        if len(device.IP) < 4:
            device.IP = "192.168.*."+device.IP
        if isinstance(device, Host):
            host = device
            host.link = host.links[0]
            assert(len(host.links)==1)
        if isinstance(device, DNS):
            device.names = names

packets(topology="OSPFtopology.txt", mkDevice=OSPFmkDevice, configure=OSPFconfigure)
