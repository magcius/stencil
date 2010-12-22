
from io import BytesIO

from stencil.core import Struct
from stencil.primitives import FormatField

XY = Struct("XY", [FormatField("X", "l"),
                   FormatField("Y", "l")])

def test_XY_read():
    stream = BytesIO("\x20\x20\x00\x00\x40\x40\x00\x00")
    context = {}
    values = XY.read(stream, context)
    assert values['X'] == 0x2020
    assert values['Y'] == 0x4040

def test_XY_write():
    stream = BytesIO()
    context = {}
    values = dict(X=0x2020, Y=0x4040)
    XY.write(stream, values, context)
    assert stream.getvalue() == b"\x20\x20\x00\x00\x40\x40\x00\x00"