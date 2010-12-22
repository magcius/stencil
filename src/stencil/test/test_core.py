
from io import BytesIO

from stencil.core import Struct
from stencil.primitives import ByteString

def test_ByteString_write():
    stream = BytesIO()
    field = ByteString("a", 5)
    context = {}
    field.write(stream, "12345", context)

    assert stream.getvalue() == b"12345"

def test_ByteString_read():
    stream = BytesIO("12345")
    field = ByteString("a", 5)
    context = {}
    value = field.read(stream, context)
    assert value == "12345"

def test_Struct_write():
    stream = BytesIO()
    struct = Struct("struct", [ByteString(name, 3) for name in ("a", "b", "c")])
    context = {}
    values = dict(a="fgh", b="ijk", c="lmn")
    struct.write(stream, values, context)
    assert stream.getvalue() == "fghijklmn"

def test_Struct_read():
    stream = BytesIO("fghijklmn")
    struct = Struct("struct", [ByteString(name, 3) for name in ("a", "b", "c")])
    context = {}
    values = struct.read(stream, context)
    assert values["a"] == "fgh"
    assert values["b"] == "ijk"
    assert values["c"] == "lmn"
