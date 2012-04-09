import pygame, os
from pygame.locals import *
from core.main import packets
from Computer import Computer

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
    return computer


def handle(event, devices, selectedDevice):
    if event.type == MOUSEBUTTONDOWN:
        for device in devices:
            if device.rect.collidepoint(event.pos):
                if selectedDevice:
                    if selectedDevice == device:
                        selectedDevice.selectLevel += 1
                        if selectedDevice.selectLevel == 4:
                            selectedDevice.selectLevel = 0
                            selectedDevice.forwardOn = None
                    else:
                        selectedDevice.attack(device)
                        selectedDevice.selectLevel = 0
                    if not selectedDevice.selectLevel:
                        return None
                elif device.owner == "RED":
                    device.selectLevel = 1
                    return device
    return selectedDevice

def config(devices, links):
    for device in devices:
        device.queues = {link: 0 for link in device.links}

def winningCondition(devices):
    return len([d for d in devices if d.owner != "RED"])

def main():
    levels = ["one.txt", "two.txt", "three.txt", "four.txt"]

    if not os.path.isfile(levels[0]) and os.path.isfile("virus/"+levels[0]):
        prefix = "virus/"
    else:
        prefix = ""

    for level in levels:
        packets(topology=prefix+level, mkDevice = mkComputer, handleEvent =
        handle, configure=config, guard=winningCondition)

if __name__ == "__main__":
    main()
