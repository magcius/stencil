
from collections import Callable

from zope.interface import implements
from zope.component import provideAdapter

from stencil import interfaces

class ValueNotFound(Exception):
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return "Value not found for field " + self.name

    __repr__ = __str__

class Field(object):
    implements(interfaces.IField)

    def __init__(self, name, length):
        self.name = name
        self.length = interfaces.IFieldLength(length)

    def read(self, stream, context):
        length = self.length.evaluate(context)
        return self.decode(context, stream.read(length))

    def decode(self, context, value):
        pass

    def write(self, stream, argument, context):
        length = self.length.evaluate(context)
        stream.write(self.encode(context, length, argument))

    def encode(self, context, length, value):
        pass

class StaticFieldLength(object):
    implements(interfaces.IFieldLength)

    def __init__(self, length):
        self.value = length

    def evaluate(self, context):
        return self.value

provideAdapter(StaticFieldLength, [int], interfaces.IFieldLength)
provideAdapter(StaticFieldLength, [long], interfaces.IFieldLength)

class CallableFieldLength(object):
    implements(interfaces.IFieldLength)
    
    def __init__(self, func):
        self.func = func

    def evaluate(self, context):
        return self.func(context)

provideAdapter(CallableFieldLength, [Callable], interfaces.IFieldLength)

class ContextFieldLength(object):
    implements(interfaces.IFieldLength)

    def __init__(self, name):
        self.name = name

    def evaluate(self, context):
        return context[self.name]

provideAdapter(ContextFieldLength, [str], interfaces.IFieldLength)

class SumFieldLength(object):
    implements(interfaces.IFieldLength)

    def __init__(self, fields):
        self.fields = fields

    def evaluate(self, context):
        return sum(field.length.evaluate(context) for field in self.fields)

class Struct(Field):
    """
    A struct contains an ordered list of fields that use field
    names for easy identification, like a C struct.
    """
    def __init__(self, name, fields=None):
        Field.__init__(self, name, SumFieldLength(fields))
        self.fields = fields or []

    def read(self, stream, context):
        struct = {}
        for field in self.fields:
            value = field.read(stream, context)
            struct[field.name] = value
        return struct

    def write(self, stream, struct, context):
        for field in self.fields:
            if field.name in struct:
                field.write(stream, struct[field.name], context)
            elif field.name in context:
                field.write(stream, context[field.name], context)
            else:
                raise ValueNotFound(field.name)
