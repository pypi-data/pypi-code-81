import struct


class Convert(object):
    def encode(self, o):
        return o

    def decode(self, o):
        return o


class ConvertStr(Convert):
    def __init__(self, encoding="utf-8"):
        self.encoding = encoding

    def encode(self, o):
        return o.encode(self.encoding)

    def decode(self, o):
        return o.decode(self.encoding)


class ConvertInteger(Convert):
    def __init__(self, as_unsigned=True):
        self.as_unsigned = as_unsigned
        self.format = "Q" if as_unsigned else "q"

    def encode(self, o):
        return struct.pack(self.format, o)

    def decode(self, o):
        return struct.unpack(self.format, o)[0]


class ConvertFloat(Convert):
    def __init__(self, as_double=True):
        self.as_double = as_double
        self.format = "d" if as_double else "f"

    def encode(self, o):
        return struct.pack(self.format, o)

    def decode(self, o):
        return struct.unpack(self.format, o)[0]


class ConvertComplex(Convert):
    def __init__(self, as_double=True):
        self.as_double = as_double
        self.format = "dd" if as_double else "ff"

    def encode(self, o):
        return struct.pack(self.format, o.real, o.imag)

    def decode(self, o):
        return complex(*struct.unpack(self.format, o))
