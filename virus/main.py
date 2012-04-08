import pygame, os
from pygame.locals import *
from core.main import packets
from Computer import Computer

def mkComputer(screen, x, y, id):
    if id.isupper():
        computer = Computer(screen, x, y, radius=30)
    else:
        computer = Computer(screen, x, y, radius=15)
    if id == "a":
        computer.changeOwner("RED")
    computer.count = 5
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
                            selectedDevice.clearForwarding()
                    else:
                        selectedDevice.attack(device)
                        selectedDevice.selectLevel = 0
                    if not selectedDevice.selectLevel:
                        return None
                elif device.owner == "RED":
                    device.selectLevel = 1
                    return device
    return selectedDevice

def config(devices, link):
    for device in devices:
        device.queues = {link: 0 for link in device.links}

def main():
    level = "one.txt"

    if not os.path.isfile(level) and os.path.isfile("virus/"+level):
        level = "/virus"+level

    packets(topology=level, mkDevice = mkComputer, handleEvent = handle, configure=config)

if __name__ == "__main__":
    main()
