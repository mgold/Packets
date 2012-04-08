import pygame, os
from pygame.locals import *
from core.main import packets
from Router import Router
from Subnet import Subnet
from DNS import DNS
from Host import Host
from Client import Client
from IP import *

"""
Main - Web

Run python on this file to launch to web module, simulating the internet.

Routers send out packets exchanging distance vector information, building their
routing tables. Note that IP addresses are associated with an interface (one
side of a link). Alice and Bob contact the DNS server, and then each other.
"""

def mkDevice(screen, x, y, id):
    if id.isdigit():
        subnet = Subnet(screen, x, y)
        subnet.IP = IP(int(id))
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
        if id == "h":
            host = Client(screen, x, y)
            host.name = "Alice"
            host.corespondent = "Bob"
        elif id == "x":
            host = Client(screen, x, y)
            host.name = "Bob"
            host.corespondent = "Alice"
        else:
            host = Host(screen, x ,y)
        host.IP = str(ord(list(id)[0]))
        return host
    else:
        print "Unrecognized unique identifier in sprite map"
        return None

def configure(devices, links):
    names = {}
    selected = None
    for device in filter(lambda d: not isinstance(d, Subnet), devices):
        if device.selected:
            selected = device
        for link in device.links:
            subnet = link.other(device)
            if isinstance(subnet, Subnet):
                if not isinstance(device.IP, IP): 
                    device.IP = IP(subnet.IP.subnet, int(device.IP))
                if isinstance(device, Router):
                    device.interfaces[link] = IP(subnet.IP.subnet, device.IP.suffix)
                    device.table[subnet.IP] = (1, link)
                elif isinstance(device, Host):
                    device.link = device.links[0]
                    assert(len(device.links)==1)
                    if isinstance(device, Client):
                        names[device.name] = device.IP
                        device.names[device.name] = device.IP
            else:
                print "Devices connected directly, rather than through a Subnet"
                
    for dns in filter(lambda d: isinstance(d, DNS), devices):
        dns.names = names

    return selected
   
def handle(event, devices, selectedDevice):
    if event.type == MOUSEBUTTONDOWN:
        for device in devices:
            if device.rect.collidepoint(event.pos) and device.selectable:
                if selectedDevice and selectedDevice == device:
                    device.selected = False
                    return None
                else:
                    device.selected = True
                    if selectedDevice:
                        selectedDevice.selected = False
                    return device
    return selectedDevice

def main():
    topology = "network.txt"

    if not os.path.isfile(topology) and os.path.isfile("web/"+topology):
        topology = "web/"+topology

    packets(topology=topology, mkDevice=mkDevice, configure=configure, handleEvent=handle)

if __name__ == "__main__":
    main()
