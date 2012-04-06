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
                        interface = self.interfaces[link]
                        packetCopy.source = interface
                        packetCopy.destination = interface[:-2]+"255"
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
                if entry != "DNS":
                    entry = entry[:10]
                if entry not in self.table or pl[entry][0] + weight <= self.table[entry][0]:
                    self.table[entry] = (pl[entry][0]+ weight, packet.link)
        elif packet.protocol == "DNS Request":
            if "DNS" in self.table:
                self.table["DNS"][1].send(packet, self)
        elif packet.protocol == "DNS Response":
            if packet.destination[:10] in self.table:
                self.table[packet.destination[:10]][1].send(packet, self)

    def draw(self):
        if self.selected:
            self.drawTable()
            pygame.draw.circle(self.screen, self.selectColor, self.pos, self.radius+5) 

        pygame.draw.circle(self.screen, self.color, self.pos, self.radius) 
        self.drawLabel()
        self.drawIPs()
        
    def drawLabel(self):
        tableSize = self.font.render(str(len(self.table)), 1, (0,0,0))
        if len(self.table) < 10:
            self.screen.blit(tableSize, (self.pos[0] - 7, self.pos[1] - 10))
        else:
            self.screen.blit(tableSize, (self.pos[0] - 13, self.pos[1] - 10))

    def drawIPs(self):
        for link, IP in self.interfaces.iteritems():
            address = self.IPfont.render(IP, 1, self.color)
            if link.d1 == self:
                x,y = link.toPos2
            else:
                x,y = link.toPos1
            if -0.001 < y < 0.001:
                if x < 0:
                    x = -self.radius - 145
                    y = 4
                else:
                    x = self.radius + 5
                    y = -20
            elif -0.001 < x < 0.001:
                if y > 0:
                    y = self.radius + 15
                else:
                    y = -self.radius - 35
                x = -81
            else:
                x *= 5
                x -= 50
                y *= 5
            self.screen.blit(address, (self.pos[0] + x, self.pos[1] + y))

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
        return "Router "+self.IP+"\n" + listing

    def drawTable(self):
        x = 40
        y = 470
        dy = 19
        header = self.IPfont.render( "Routing Table for Router "+self.IP, 1, self.selectColor)
        self.screen.blit(header, (x, y))
        for link in self.links:
            listing = self.interfaces[link] + "/32  0  localhost"
            y += dy
            rendlisting = self.IPfont.render(listing, 1, self.color)
            self.screen.blit(rendlisting, (x, y))
        for IP, (weight, link) in self.table.iteritems():
            if IP != "DNS":
                IP += ".0/24"
            else:
                IP = "DNS            "
            listing = IP.ljust(14) + str(weight).rjust(4)+"  "
            listing += self.interfaces[link].ljust(16)
            y += dy
            rendlisting = self.IPfont.render(listing, 1, self.color)
            self.screen.blit(rendlisting, (x, y))
        footer = self.IPfont.render(str(len(self.table)+len(self.links))+
            " entries, "+str(len(self.table))+" foreign", 1, self.selectColor)
        self.screen.blit(footer, (x, y+dy))
