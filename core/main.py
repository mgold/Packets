import pygame, sys, os
from pygame.locals import *
from loadLevel import loadLevel

"""
Main - Core

This is it: the main game loop. Configuration is done by calling packets() with
custom arguments. This file can also be run directly to show the core in
"vanilla" mode, using the default arguments. The most commonly overriden
arguments are toplogy and mkDevice.

topology: a text file as described in loadLevel.py containing the physical and
logical structure of the network.

mkDevice(screen, x, y, uniqueIdentifier): Must return a Device.

mkLink(screen, uniqueID1, device1, uniqueID2, device2): Must return a Link.

configure(devices, links): Called just before the main game loop begins. Acts
by side effect, except that it returns a closure...

handleEvent(event, devices, closure): Handles pygame events. The closure is the
returned value of configure, or None if no configure was supplied, on the first
call. Should return a closure to be used on the next call.

"""

def quit():
    pygame.quit()
    sys.exit()

def packets(topology="topology.txt", mkDevice=None, mkLink=None, configure=None, handleEvent=lambda e, ds,c: c):

    if not os.path.isfile(topology) and os.path.isfile("core/"+topology):
        topology = "core/"+topology

    pygame.init()

    #Music
    for music in "music.wav", "core/music.wav", "../core/music.wav":
        try:
            pygame.mixer.music.load(music)
            pygame.mixer.music.play(-1)
            break
        except:
            pass

    #Screen
    WIDTH, HEIGHT = 1440, 900
    window = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN)
    pygame.display.set_caption('Packets')
    screen = pygame.display.get_surface() 

    #Clock
    clock = pygame.time.Clock()
    FPS = 50
    time_passed = 0

    #Read in a file to generate the sprites on a level
    devices, links = loadLevel(topology, screen, mkDevice, mkLink)

    if configure:
        closure = configure(devices, links)
    else:
        closure = None

    #game loop
    while True:
        time_passed = clock.tick(FPS)

        #Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit()
            else:
                closure = handleEvent(event, devices, closure)

        #Update
        for device in devices:
            device.update()
        for link in links:
            link.update()

        #Draw
        screen.fill((0,0,0))
        for link in links:
            link.draw()
        for device in devices:
            device.draw()

        pygame.display.flip() 

if __name__ == "__main__":
    packets()
