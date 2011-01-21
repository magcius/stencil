
from struct import pack, unpack

from zope.interface import implements

from stencil import interfaces, util

class ByteString(object):
    implements(interfaces.IFormat)
    def __init__(self, length):
        self.length = interfaces.IFormatLength(length)

    def read(self, stream, context):
        length = self.length.evaluate(context)
        return stream.read(length)

    def write(self, stream, bytes, context):
        length = self.length.evaluate(context)
        assert len(bytes) == length
        stream.write(bytes)

class _IntBase(object):
    implements(interfaces.IFormat)

    formats = {}
    def __init__(self, length, endianness='<'):
        self.length = interfaces.IFormatLength(length)
        self.endianness = endianness

    def read(self, stream, context):
        length = self.length.evaluate(context)

        if length in self.formats:
            return unpack(self.endianness+self.formats[length], stream.read(length))[0]

        return self.decode_raw(length, stream.read(length))

    def write(self, stream, num, context):
        length = self.length.evaluate(context)

        if length in self.formats:
            stream.write(pack(self.endianness+self.formats[length], num))
        else:
            stream.write(self.encode_raw(length, num))

class UInt(_IntBase):
    formats = {1: "B", 2: "H", 4: "L", 8: "Q"}
    def decode_raw(self, length, bytes):
        if self.endianness == "<":
            bytes = bytes[::-1]

        return util.decode_bytes(bytes)

    def encode_raw(self, length, num):
        bytes = util.encode_int(num, length)

        if self.endianness != "<":
            return bytes[::-1]

        return bytes

class SInt(_IntBase):
    formats = {1: "b", 2: "h", 4: "l", 8: "q"}
    def decode_raw(self, length, bytes):
        if self.endianness == "<":
            bytes = bytes[::-1]

        length *= 8
        value = util.decode_bytes(bytes)
        if value > (1 << length-1):
            return value - (1 << length)
        return value

    def encode_raw(self, length, num):
        bytes = util.encode_int(num, length)

        if self.endianness != "<":
            return bytes[::-1]

        return bytes
