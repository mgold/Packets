class IP:
    """Encapsulates an immutable IPv4 address or address block"""

    def __init__(self, a, b, c, d, cidr=32, bcast=False):

        self.address = self.humanReadable = self.hash =  ''
        for byte in [a, b, c, d]:
            assert(0 <= byte <= 255)
            self.address += bin(byte)[2:].zfill(8)
            self.humanReadable += str(byte) + '.'
            self.hash += str(byte)
        self.humanReadable = self.humanReadable[:-1] + '/' + str(cidr)
        self.hash += str(cidr)
        self.hash = int(self.hash)
        self.address = int(self.address, 2)

        assert(0 <= cidr <= 32)
        self.cidr = cidr
        self.mask = int('1' * self.cidr + '0' * (32 - self.cidr), 2)
        self.bcast = bcast
        if not bcast:
            self.broadcastQuadruple = []
            broadcastAddress = self.address | ~self.mask
            for i in range(0, 32, 8):
                byte = broadcastAddress << i
                byte >>= 24
                byte &= 255
                self.broadcastQuadruple.append(byte)

    def broadcast(self):
        if self.bcast:
            return self
        return IP(self.broadcastQuadruple[0], self.broadcastQuadruple[1],
                  self.broadcastQuadruple[2], self.broadcastQuadruple[3], self.cidr, True)

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
