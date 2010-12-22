
from zope.interface import implements

from stencil import interfaces

class Field(object):
    implements(interfaces.IField)

    def __init__(self, name):
        self.name = name

    def read(self, stream, context):
        return NotImplemented

    def write(self, stream, argument, context):
        return NotImplemented

class UnsignedByteField(Field):
    def read(self, stream, context):
        return ord(stream.read(1))

    def write(self, stream, argument, context):
        assert 0 <= argument < 256
        return stream.write(chr(argument))