import pygame, os
from pygame.locals import *
try:
    import pygame.mixer as mixer
except ImportError:
    import android_mixer as mixer
from core.main import packets
from Computer import Computer
from core.Link import Link
from Firewall import Firewall
from Text import Text
from time import sleep

"""
Main - Virus

Defines functions passed in as arguments to packets(), defined in core/main;
see there for documentation on the role of each. Then makes multiple calls in
sequence.
"""

def loadSound(filename):
    """ pygame.mixer.sound(filename) will fail silently - wtf? """
    if os.path.isfile(filename):
        return mixer.Sound(filename)
    if os.path.isfile('virus/'+filename):
        return mixer.Sound('virus/'+filename)
    raise pygame.error("Sound "+filename+" does not exist.")

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
            if not isinstance(device, Text) and device.rect.collidepoint(event.pos):
                if selectedDevice:
                    if selectedDevice != device:
                        selectedDevice.attack(device)
                    try:
                        loadSound("deselect.wav").play()
                    except Exception: pass
                    selectedDevice.selected = False
                    return None
                elif device.owner == "RED":
                    try:
                        loadSound("select.wav").play()
                    except Exception: pass
                    device.selected = 1
                    return device
    return selectedDevice

def winningCondition(devices):
    return len([d for d in devices if d.owner != "RED"])

def arenaWin(devices):
     return len([d for d in devices if d.owner == "RED"]) and len([d for d in devices if d.owner == "GREEN"])

def textScreen(screen, filename):
    text = Text(screen, 25, 10, filename)
    textLen = len(text.message)

    clock = pygame.time.Clock()
    FPS = 50
    time_passed = 0

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
                if text.current_line  == textLen:
                    return
                else:
                    text.current_line = textLen
    
        text.update()
        screen.fill((0,0,0))
        text.draw()
        pygame.display.flip() 

def main():
<<<<<<< HEAD
    levels = ["one.txt", "two.txt", "three.txt", "four.txt", "five.txt"]

    arenas = ["six.txt", "arena.txt", "giveandtake.txt"]
=======
>>>>>>> 0868a2c3f74062bc7773fdc567b0c76262715242

    if not os.path.isfile(levels[0]) and os.path.isfile("virus/"+levels[0]):
        prefix = "virus/"
    else:
        prefix = ""

    pygame.init()

    #Screen
    WIDTH, HEIGHT = 480, 320
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Virus for Android')
    screen = pygame.display.get_surface() 

    #Music
    try:
        mixer.music.load( "../core/music.wav")
        mixer.music.play(-1)
        winsound = loadSound("winlevel.wav")
    except Exception:
        try:
            mixer.music.load( "core/music.wav")
            mixer.music.play(-1)
            winsound = loadSound("virus/winlevel.wav")
        except Exception:
            winsound = None

    textScreen(screen, "intro.txt")   

    for level in "one.txt", "two.txt", "three.txt", "four.txt", "five.txt":
        packets(topology=prefix+level, 
                mkDevice = mkComputer, 
                handleEvent = handle, 
                guard=winningCondition, 
                mkLink = mkLink, 
                screen = screen)
        if winsound:
            winsound.play()
        sleep(.75)

    for arena in "six.txt", "arena.txt", "giveandtake.txt":
        packets(topology=prefix+arena, 
            mkDevice = mkComputerArena, 
            handleEvent = handle,
            guard=arenaWin,
            mkLink = mkLinkArena,
            screen = screen)
        if winsound:
            winsound.play()
        sleep(.75)

    textScreen(screen, "credits1.txt")   
    textScreen(screen, "credits2.txt")   

if __name__ == "__main__":
    main()
