
from zope.interface import implements
from zope.component import provideAdapter

from collections import Callable

from stencil import interfaces

class ValueNotFound(Exception):
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return "Value not found for field " + self.name

    __repr__ = __str__

class Field(object):
    implements(interfaces.IField)

    def __init__(self, name, format):
        self.name = name
        self.format = interfaces.IFormat(format)

    def get_value(self, context):
        try:
            return context[self.name]
        except KeyError:
            raise ValueNotFound(self.name)

    def set_value(self, context, value):
        context[self.name] = value

class StaticFormatLength(object):
    implements(interfaces.IFormatLength)

    def __init__(self, length):
        self.value = length

    def evaluate(self, context):
        return self.value

provideAdapter(StaticFormatLength, [int], interfaces.IFormatLength)
provideAdapter(StaticFormatLength, [long], interfaces.IFormatLength)
provideAdapter(StaticFormatLength, [None], interfaces.IFormatLength)

class CallableFormatLength(object):
    implements(interfaces.IFormatLength)
    
    def __init__(self, func):
        self.func = func

    def evaluate(self, context):
        return self.func(context)

provideAdapter(CallableFormatLength, [Callable], interfaces.IFormatLength)

class ContextFormatLength(object):
    implements(interfaces.IFormatLength)

    def __init__(self, name):
        self.name = name

    def evaluate(self, context):
        return context[self.name]

provideAdapter(ContextFormatLength, [str], interfaces.IFormatLength)

class StructBase(object):
    implements(interfaces.IFormat)

    def create_fields(self, context):
        pass

    def read(self, stream, context=None):
        context = context or dict()
        for field in self.create_fields(context):
            field = interfaces.IField(field)
            value = field.format.read(stream, context)
            field.set_value(context, value)
        return context

    def write(self, stream, values, context=None):
        if context:
            context = dict(context)
        else:
            context = dict()
        context.update(values)
        for field in self.create_fields(context):
            field = interfaces.IField(field)
            value = field.get_value(context)
            field.format.write(stream, value, context)

class StructFieldLength(object):
    implements(interfaces.IFormatLength)

    def __init__(self, fields):
        self.fields = fields

    def evaluate(self, context):
        return sum(field.length.evaluate(context) for field in self.fields)

class Struct(StructBase):
    """
    A struct contains an ordered list of fields that use field
    names for identification, like a C struct.
    """
    def __init__(self, fields=None):
        self.fields = fields or []
        self.length = StructFieldLength(self.fields)

    def create_fields(self, context):
        return iter(self.fields)
