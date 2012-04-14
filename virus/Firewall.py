import pygame
from pygame.locals import *
from core.Link import Link
from math import atan2, degrees

class Firewall(Link):
    
    def __init__ (self, screen, d1, d2, speed=5):
        Link.__init__(self, screen, d1, d2)

        self.good = self.d1
        self.bad = self.d2

        self.image = pygame.Surface((35, 35))
        self.imagePos = ((self.good.pos[0] + self.bad.pos[0])//2 -16, (self.good.pos[1] + self.bad.pos[1])//2 -19)

        self.theta = degrees(atan2(-self.toPos2[1], self.toPos2[0]))
        self.rect = pygame.Rect(self.imagePos, (33, 33))

        self.updateOwner()
    
    def updateOwner(self):
        self.owner = self.good.owner
        self.ownerColor = self.good.color
      
        pygame.draw.lines(self.image, self.ownerColor, True, [(0, 35), (35, 17), (0, 0)], self.thickness)
        pygame.draw.line (self.image, self.ownerColor, (33, 0), (33, 33), self.thickness)
        pygame.draw.rect (self.image, (0,0,0,0), pygame.Rect(0,0,2,2))

    def update(self):
        Link.update(self)

        if self.good.owner != self.owner:
            self.updateOwner()

        for packet in [packet for packet in self.packets if packet.owner != self.owner and self.rect.colliderect(packet.rect)]:
            self.packets.remove(packet)

    def draw(self):
        if self.active:
            self.screen.blit(pygame.transform.rotate(self.image, self.theta), self.imagePos)
            Link.draw(self)
