import pygame, sys, os
from pygame.locals import *
from loadLevel import loadLevel

def quit():
    pygame.quit()
    sys.exit()

def packets(levelName="topology.txt", setup=None):

    pygame.init()

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
    devices, links = loadLevel(levelName, screen)

    #Setup devices according to caller
    if setup:
        map(setup, devices)

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
