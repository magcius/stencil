
from zope.interface import Interface, Attribute

class IField(Interface):
    name = Attribute("The name for the field.")
    format = Attribute("The format for the field.")

    def get_value(context):
        pass

    def set_value(context, value):
        pass

class IFormat(Interface):
    length = Attribute("IFormatLength")

    def read(stream, context):
        """
        Read from stream.
        """

    def write(stream, argument, context):
        """
        Write argument to stream.
        """

class IFormatLength(Interface):
    def evaluate(context):
        """
        Get the length at the field given a length.
        """
