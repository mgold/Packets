import pygame, os
from pygame.locals import *
from core.main import packets
from Computer import Computer
from core.Link import Link
from Firewall import Firewall
from time import sleep

"""
Main - Virus

Defines functions passed in as arguments to packets(), defined in core/main;
see there for documentation on the role of each. Then makes multiple calls in
sequence.
"""

def mkComputer(screen, x, y, id):
    if id.isupper():
        if id == "Z":
            computer = Computer(screen, x, y, radius=60)
            computer.count = 150
        else:
            computer = Computer(screen, x, y, radius=30)
            computer.count = 15
    else:
        computer = Computer(screen, x, y, radius=15)
        computer.count = 5
    if id == "a":
        computer.changeOwner("RED")
        computer.count = 10
    elif id == "G":
        computer = Computer(screen, x, y, radius=15)
        computer.changeOwner("GREEN")
        computer.count = 10
    return computer

def mkLink(screen, id1, device1, id2, device2):
    if id1 == "F" and id2 != "f":
        return Firewall(screen, device1, device2)
    else: return Link(screen, device1, device2)

def mkComputerArena(screen, x, y, id):
    if id.isupper():
        computer = Computer(screen, x, y, radius=30)
        computer.count = 15
    else:
        computer = Computer(screen, x, y, radius=15)
        computer.count = 5
    if id == "A" or id == "B":
        computer.changeOwner("RED")
        computer.count = 10
    elif id == "Y" or id == "Z":
        computer.changeOwner("GREEN")
        computer.count = 10
    return computer

def mkLinkArena(screen, id1, device1, id2, device2):
    if (id1.isdigit() and id2.isupper()) or (id1.isupper() and id2.islower()):
        return Firewall(screen, device1, device2)
    return Link(screen, device1, device2)

def handle(event, devices, selectedDevice):
    if event.type == MOUSEBUTTONDOWN:
        for device in devices:
            if device.rect.collidepoint(event.pos):
                if selectedDevice:
                    if selectedDevice != device:
                        selectedDevice.attack(device)
                    selectedDevice.selected = False
                    return None
                elif device.owner == "RED":
                    device.selected = 1
                    return device
    return selectedDevice

def winningCondition(devices):
    return len([d for d in devices if d.owner != "RED"])

def arenaWin(devices):
     return len([d for d in devices if d.owner == "RED"]) and len([d for d in devices if d.owner == "GREEN"])

def main():
    levels = ["one.txt", "two.txt", "three.txt", "four.txt", "five.txt"]

    arenas = ["six.txt", "arena.txt", "giveandtake.txt"]

    if not os.path.isfile(levels[0]) and os.path.isfile("virus/"+levels[0]):
        prefix = "virus/"
    else:
        prefix = ""

    for level in levels:
        packets(topology=prefix+level, mkDevice = mkComputer, handleEvent =
        handle, guard=winningCondition, mkLink = mkLink)
        sleep(.75)

    for arena in arenas:
        packets(topology=prefix+arena, mkDevice = mkComputerArena, handleEvent =
        handle, guard=arenaWin, mkLink = mkLinkArena)
        sleep(.75)

if __name__ == "__main__":
    main()
