import pygame
from pygame.locals import *
from Packet import Packet
from Device import Device
from copy import copy

class Router(Device):
    def __init__ (self, screen, x, y):
        Device.__init__(self, screen, x, y)
        self.color = (0, 128, 128) 
        self.timer = 0
        
        self.packetColor = (128, 255, 128)

        self.IPfont = pygame.font.SysFont(u'couriernew,courier', 18, bold=True)
        self.font = pygame.font.Font(None, 36)

        #table is all known routers, interfaces is local links to subnets
        self.table = {}
        self.interfaces = {}
        
        self.IP = "IP Unset"
        self.selectColor = (191, 191, 191)
    
    def update(self):
        if self.timer == 0:
            packet = Packet(self.screen, self.pos[0], self.pos[1])
            packet.color = self.packetColor
            packet.payload = {}
            packet.protocol = "OSPF"
            for link in self.links:
                packetCopy = copy(packet)
                for entry in self.table:
                    if self.table[entry][1] != link: #poisoned reverse
                        packetCopy.payload[entry] = (self.table[entry][0], link)
                link.send(packetCopy, self)
            self.timer = 250
        else:
            self.timer -= 1

    def receive(self, packet):
        if packet.protocol == "OSPF":
            pl = packet.payload
            weight = packet.link.weight
            for entry in pl:
                if entry not in self.table or pl[entry][0] + weight <= self.table[entry][0]:
                        self.table[entry] = (pl[entry][0]+ weight, packet.link)

    def draw(self):
        if self.selected:
            self.blitTable()
            pygame.draw.circle(self.screen, self.selectColor, self.pos, self.radius+5) 

        pygame.draw.circle(self.screen, self.color, self.pos, self.radius) 

        tableSize = self.font.render(str(len(self.table)), 1, (0,0,0))
        if len(self.table) < 10:
            self.screen.blit(tableSize, (self.pos[0] - 7, self.pos[1] - 10))
        else:
            self.screen.blit(tableSize, (self.pos[0] - 15, self.pos[1] - 10))

        for link, IP in self.interfaces.iteritems():
            address = self.IPfont.render(IP[8:], 1, self.color)
            if len(self.interfaces) == 1:
                self.screen.blit(address, (self.pos[0] - 60, self.pos[1] + self.radius + 4))
            else:
                if link.d1 == self:
                    x,y = link.toPos2
                else:
                    x,y = link.toPos1
                self.screen.blit(address, (self.pos[0] + 10*x-27, self.pos[1] + 10*y - 20))

    def __repr__(self):
        return "Router: "+self.IP

    def __str__(self):
        listing = ""
        for IP, (weight, link) in self.table.iteritems():
            listing += IP.ljust(16) + str(weight).rjust(4)+"  "
            if link:
                if link.d1 == self:
                    listing += link.d2.IP.ljust(16) + "\n"
                else:
                    listing += link.d1.IP.ljust(16) + "\n"
            else:
                listing += "localhost\n"
        return "Routing Table for "+self.IP+"\n" + listing

    def blitTable(self):
        x = 40
        y = 470
        header = self.IPfont.render( "Routing Table for "+self.IP, 1, self.selectColor)
        self.screen.blit(header, (x, y))
        for IP, (weight, link) in self.table.iteritems():
            listing = IP.ljust(14) + str(weight).rjust(4)+"  "
            if link:
                listing += self.interfaces[link].ljust(16)
            else:
                listing += "localhost"
            y += 19
            rendlisting = self.IPfont.render(listing, 1, self.color)
            self.screen.blit(rendlisting, (x, y))
        footer = self.IPfont.render(str(len(self.table))+" entries", 1, self.selectColor)
        self.screen.blit(footer, (x, y+20))
