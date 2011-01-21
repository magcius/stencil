
from io import BytesIO

from stencil.core import Struct, Field
from stencil.primitives import UInt, SInt

BasicXY = Struct([Field("X", SInt(2)),
                  Field("Y", SInt(2))])

def test_BasicXY_write():
    stream = BytesIO()
    context = {}
    values = dict(X=-24, Y=73)
    XY.write(stream, values, context)
    assert stream.getvalue() == "\xE8\xFF\x49\x00"

def test_BasicXY_read():
    stream = BytesIO("\xE8\xFF\x49\x00")
    context = {}
    values = XY.read(stream, context)
    assert values['X'] == -24
    assert values['Y'] == 73


XY = Struct([Field("NBytes", UInt(2)),
             Field("X", SInt("NBytes")),
             Field("Y", SInt("NBytes"))])

def test_XY_write():
    stream = BytesIO()
    context = {}
    values = dict(X=-24, Y=73)
    XY.write(stream, values, context)
    assert stream.getvalue() == "\x02\x00\xE8\xFF\x49\x00"

def test_XY_read():
    stream = BytesIO("\x02\x00\xE8\xFF\x49\x00")
    context = {}
    values = XY.read(stream, context)
    assert values['X'] == -24
    assert values['Y'] == 73
