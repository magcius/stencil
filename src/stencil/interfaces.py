
from zope.interface import Interface, Attribute

class IField(Interface):
    name = Attribute("The name for the field.")
    length = Attribute("IFieldLength for the field.")
    
    def read(stream, context):
        """
        Read from stream.
        """

    def decode(context, argument):
        """
        Decode.
        """

    def write(stream, argument, context):
        """
        Write argument to stream.
        """

    def encode(context, length, argument):
        """
        Encode.
        """

class IFieldLength(Interface):
    def evaluate(context):
        """
        Get the length at the field given a length.
        """
