import pygame
from pygame.locals import *
from core.Packet import Packet
from core.Device import Device
from copy import copy

class Router(Device):
    def __init__ (self, screen, x, y):
        Device.__init__(self, screen, x, y)
        self.color = (0, 128, 128) 
        self.timer = 0
        
        self.packetColor = (128, 255, 128)

        self.IPfont = pygame.font.SysFont(u'couriernew,courier', 18, bold=True)
        self.font = pygame.font.Font(None, 36)

        self.table = {}
        #All IPs -> (weight, local Link)

        self.interfaces = {}
        #local Link -> local IP
        
        self.IP = "IP Unset"
    
    def update(self):
        if self.timer == 0:
            packet = Packet(self.screen, self.pos[0], self.pos[1])
            packet.color = self.packetColor
            packet.payload = {}
            packet.protocol = "OSPF"
            for link in self.links:
                packetCopy = copy(packet)
                for subnetIP in self.table:
                    if self.table[subnetIP][1] != link: #poisoned reverse
                        interface = self.interfaces[link]
                        packetCopy.source = interface
                        packetCopy.destination = interface.broadcast()
                        packetCopy.payload[subnetIP] = (self.table[subnetIP][0], link)
                link.send(packetCopy, self)
            self.timer = 250
        else:
            self.timer -= 1

    def receive(self, packet):
        if packet.destination.isBroadcast():
            self.broadcast(packet)
        elif packet.destination in self.IP:
            self.sendLocal(packet)
        else:
            for subnetIP in self.table:
                if packet.destination in subnetIP:
                    self.table[subnetIP][1].send(packet, self)

        if packet.protocol == "OSPF":
            pl = packet.payload
            weight = packet.link.weight
            for subnetIP in pl:
                if subnetIP not in self.table or pl[subnetIP][0] + weight <= self.table[subnetIP][0]:
                    self.table[subnetIP] = (pl[subnetIP][0]+ weight, packet.link)

    def broadcast(self, packet):
        pass

    def sendLocal(self, packet):
        pass

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
            address = self.IPfont.render(str(IP)[:-3], 1, self.color)
            if link.d1 == self:
                x,y = link.toPos2
            else:
                x,y = link.toPos1
            if y == 0:
                if x < 0:
                    x = -self.radius - 145
                    y = 4
                else:
                    x = self.radius + 5
                    y = -20
            elif x == 0:
                if y > 0:
                    y = self.radius + 15
                else:
                    y = -self.radius - 25
                x = -81
            elif x < 0 and y < 0:
                x *= 5
                x -= 90
                y = -self.radius - 17
            elif x < 0 and y > 0:
                x *= 5
                x -= 50
                y *= 5
                y += 5
            else:
                x *= 5
                x -= 50
                y *= 5
            self.screen.blit(address, (self.pos[0] + x, self.pos[1] + y))

    def drawTable(self):
        x = 40
        y = 470
        dy = 19
        header = self.IPfont.render( "Routing Table for Router "+str(self.IP), 1, self.selectColor)
        self.screen.blit(header, (x, y))
        for link in self.links:
            listing = str(self.interfaces[link]) + "  0  localhost"
            y += dy
            rendlisting = self.IPfont.render(listing, 1, self.color)
            self.screen.blit(rendlisting, (x, y))
        for IP, (weight, link) in self.table.iteritems():
            listing = str(IP).ljust(14) + str(weight).rjust(4)+"  "
            listing += str(self.interfaces[link]).ljust(16)
            y += dy
            rendlisting = self.IPfont.render(listing, 1, self.color)
            self.screen.blit(rendlisting, (x, y))
        footer = self.IPfont.render(str(len(self.table)+len(self.links))+
            " entries, "+str(len(self.table))+" foreign", 1, self.selectColor)
        self.screen.blit(footer, (x, y+dy))


    def __repr__(self):
        return "<%s instance at %s with IP %s>" % (self.__class__.__name__, id(self), str(self.IP))

    def __str__(self):
        listing = ""
        for IP, (weight, link) in self.table.iteritems():
            listing += str(IP).ljust(16) + str(weight).rjust(4)+"  "
            if link:
                if link.d1 == self:
                    listing += link.d2.IP.ljust(16) + "\n"
                else:
                    listing += link.d1.IP.ljust(16) + "\n"
            else:
                listing += "localhost\n"
        return "Router "+str(self.IP)+"\n" + listing

