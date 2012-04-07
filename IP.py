class IP:
    """Encapsulates an IPv4 address"""

    def __init__(self, a, b, c, d, cidr=32):
        self.address = self.humanReadable = ''
        for byte in [a, b, c, d]:
            self.address += bin(byte)[2:].zfill(8)
            self.humanReadable = byte + '.'
        self.humanReadable += '/' + cidr
        self.cidr = cidr

    def inSubnet(self, otherIP):
        mask = '1' * self.cidr
        return otherIP.address & mask == self.address & mask

    def __str__(self):
        return self.humanReadable

    def __repr__(self):
        return "<%s instance at %s with IP %s>" % (self.__class__.__name__, id(self), self.__str__())
