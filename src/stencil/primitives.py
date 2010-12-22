
from struct import Struct as PythonStruct

from stencil.core import Field

class ByteString(Field):
    def decode(self, context, value):
        return value

    def encode(self, context, length, value):
        return value

class FormatField(Field):
    def __init__(self, name, format):
        self.format = PythonStruct(format)
        Field.__init__(self, name, self.format.size)

    def decode(self, context, value):
        return self.format.unpack(value)[0]

    def encode(self, context, length, value):
        return self.format.pack(value)
