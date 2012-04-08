import pygame, sys, os
from pygame.locals import *
from loadLevel import loadLevel

"""
Packets

This is it: the main game loop. Configuration is done by calling packets() with
custom arguments.
"""

def quit():
    pygame.quit()
    sys.exit()

def packets(topology="topology.txt", mkDevice=None, mkLink=None, configure=None):

    if not os.path.isfile(topology) and os.path.isfile("core/"+topology):
        topology = "core/"+topology

    pygame.init()

    #Music
    try:
        pygame.mixer.music.load("music.wav")
        pygame.mixer.music.play(-1)
    except:
        try:
            pygame.mixer.music.load("core/music.wav")
            pygame.mixer.music.play(-1)
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
        configure(devices, links)

    try:
        selectedDevice = filter (lambda d: d.selected, devices)[0]
    except:
        selectedDevice = None

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
            elif event.type == MOUSEBUTTONDOWN:
                for device in devices:
                    if device.rect.collidepoint(event.pos) and device.selectable:
                        if selectedDevice and selectedDevice == device:
                            device.selected = False
                            selectedDevice = None
                        else:
                            device.selected = True
                            if selectedDevice:
                                selectedDevice.selected = False
                            selectedDevice = device

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
