class IP:
    """
    IP - Encapsulates an immutable IPv4 address or address block
    
    I have made the simplifying restriction that all addresses take the form
    192.168.xxx.yyy and the CIDR is either /24 or /32. That is, it's the class
    system in CIDR notation.
    """

    def __init__(self, subnet, suffix=0):
        assert(0 <= subnet <= 255)
        assert(0 <= suffix <= 255)

        self.subnet = subnet
        self.suffix = suffix
        self.address = int(str(subnet).zfill(3) + str(suffix).zfill(3))

        if suffix == 0:
            self.cidr = 24
        else:
            self.cidr = 32

    def broadcast(self):
        return IP(self.subnet, 255)

    def isBroadcast(self):
        return self.suffix == 255

    def __contains__(self, otherIP):
        return otherIP.subnet == self.subnet and self.cidr == 24

    def __cmp__(self, otherIP):
        return self.address.__cmp__(otherIP.address)

    def __eq__(self, otherIP):
        return self.address == otherIP.address

    def __hash__(self):
        return self.address

    def __str__(self):
        return '192.168.'+str(self.subnet)+'.'+str(self.suffix)+'/'+str(self.cidr)

    def __repr__(self):
        return "<%s instance at %s with IP %s>" % (self.__class__.__name__, id(self), self.__str__())


class DNSIP(IP):
    """
    DNS IP - A way to add "DNS" as an IP without cluttering the IP class.

    Carries no informaion other than the fact that it is a DNS IP.
    """

    def __init__(self):
        self.subnet = self.suffix = self.address = -1

    def broadcast(self):
        raise NotImplementedError

    def isBroadcast(self):
        return False

    def __contains__(self, otherIP):
        return isinstance(otherIP, DNSIP)

    def __cmp__(self, otherIP):
        raise NotImplementedError

    def __eq__(self, otherIP):
        return isinstance(otherIP, DNSIP)

    def __hash__(self):
        return 1111 #Homage to 1.1.1.1

    def __str__(self):
        return "DNS"

    def __repr__(self):
        return "<%s instance at %s>" % (self.__class__.__name__, id(self))
