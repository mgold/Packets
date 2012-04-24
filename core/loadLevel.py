import pygame
from pygame.locals import *
from Device import Device
from Link import Link

def loadLevel(level_name, screen, mkDevice=None, mkLink=None):
    """
    loadLevel - Core
    
    Expects the name of a sprite map and the screen, and returns the
    sprites for the level. Extensions to the core are implemented almost
    entirely by functions that take effect in this module.
    
    The sprite map is the name of a file, whose contents consist of spaces,
    newlines, and unique identifiers, followed by a list of pairs of unique
    identifiers. A unique identifier is any character that is not whitespace, a
    comma, or a parenthesis.  A unique identifier must not appear more than
    once outside the list of pairs of unique identifiers. That list is of the
    form (a, b) where a and b are unique identifiers. See topology.txt for an
    example.

    The spaces, newlines, and unique identifiers determine the onscreen layout
    of the network. The list of pairs of unique identifiers is an adjacency
    list, determining the logical layout of the network.

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
           return links(screen, spriteMap, devices, mkLink)
        else:
            if mkDevice:
                devices[region] = mkDevice(screen, x, y, region)
            else:
                devices[region] = Device(screen, x, y) 

        col += 1
        region = spriteMap.read(1)

    print "Found no links!"
    return devices, []

def links(screen, spriteMap, devices, mkLink):
    d1 = None
    id1 = None
    linkList = [] #A list of Link objects. What did you think it was?
    region = "("
    ignoreThese = [" ", ",", "(", ")", "\n", ""]
    while region != "":
        region = spriteMap.read(1)
        if region not in ignoreThese:
            if d1:
                d2 = devices[region]
                if mkLink:
                    link = mkLink(screen, id1, d1, region, d2)
                else:
                    link = Link(screen, d1, d2)
                d1.links.append(link)
                d2.links.append(link)
                linkList.append(link)
                d1 = None
                id1 = None
            else:
                d1 = devices[region]
                id1 = region
    spriteMap.close()
    return devices.values(), linkList

