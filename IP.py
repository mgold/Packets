class IP:
    """Encapsulates an immutable IPv4 address or address block"""

    def __init__(self, a, b, c, d, cidr=32):
        self.address = self.humanReadable = ''
        for byte in [a, b, c, d]:
            self.address += bin(byte)[2:].zfill(8)
            self.humanReadable += str(byte) + '.'
        self.humanReadable = self.humanReadable[:-1] + '/' + str(cidr)
        self.hash = ''.join(filter(lambda c: c != '.' and c != '/', list(self.humanReadable)))
        self.address = int(self.address, 2)

        self.cidr = cidr
        self.mask = int('1' * self.cidr + '0' * (32 - self.cidr), 2)

    def __contains__(self, otherIP):
        return otherIP.address & self.mask == self.address & self.mask

    def __cmp__(self, otherIP):
        return self.address.__cmp__(otherIP.address)

    def __eq__(self, otherIP):
        return self.address == otherIP.address and self.cidr == otherIP.cidr

    def __hash__(self):
        return self.hash

    def __str__(self):
        return self.humanReadable

    def __repr__(self):
        return "<%s instance at %s with IP %s>" % (self.__class__.__name__, id(self), self.__str__())
