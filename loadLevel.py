import pygame
from pygame.locals import *
from Device import Device
from Link import Link

def loadLevel(level_name, screen):
    """
    loadLevel - expects the name of a sprite map and the screen, and returns the
    sprites for the level.
    
    The sprite map is the name of a file, whose contents consist of spaces,
    newlines, and unique identifiers, followed by a list of pairs of unique
    identifiers. A unique identifier is any character that is not whitespace, a
    comma, or a parenthesis.  A unique identifier must not appear more than
    once outside the list of pairs of unique identifiers. That list is of the
    form (a, b) where a and b are unique identifiers.
    
    Return type: a tuple of a list of Device objects and a list of Link objects.
    """

    devices = {}

    col = row = 0
    GRANULARITY = 30
    
    spriteMap = open(level_name)
    region = spriteMap.read(1)
    while region != "":
        x, y = col*GRANULARITY, row*GRANULARITY
        if region == " ":
            pass
        elif region == "\n":
            row += 1
            col  = -1
        elif region == "(":
           return links(screen, spriteMap, devices)
        else:
            devices[region] = Device(screen, x, y)

        col += 1
        region = spriteMap.read(1)

    print "Found no links!"
    return devices, []

def links(screen, spriteMap, devices):
    d1 = None 
    linkList = [] #A list of Link objects. What did you think it was?
    region = "("
    ignoreThese = [" ", ",", "(", ")", "\n", ""]
    while region != "":
        region = spriteMap.read(1)
        if region not in ignoreThese:
            if d1:
                d2 = devices[region]
                link = Link(screen, d1, d2)
                d1.links.append(link)
                d2.links.append(link)
                linkList.append(link)
                d1 = None
            else:
                d1 = devices[region]
    spriteMap.close()
    return devices.values(), linkList

