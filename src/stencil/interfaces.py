
from zope.interface import Interface, Attribute

class IField(Interface):
    name = Attribute("The name for the field.")
    
    def read(stream, context):
        """
        Read from stream.
        """

    def write(stream, argument, context):
        """
        Write argument to stream.
        """
