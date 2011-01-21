
from io import BytesIO

from stencil.core import Struct, Field
from stencil.primitives import ByteString, UInt, SInt

def test_ByteString_write():
    stream = BytesIO()
    format = ByteString(5)
    context = {}
    format.write(stream, "12345", context)
    assert stream.getvalue() == b"12345"

def test_ByteString_read():
    stream = BytesIO("12345")
    format = ByteString(5)
    context = {}
    value = format.read(stream, context)
    assert value == "12345"

def _test_IntBase_read_base(format_):
    # test one-byte values
    stream = BytesIO("\x25")
    format = format_(1)
    context = {}
    value = format.read(stream, context)
    assert value == 0x25

    # test two-byte values
    stream = BytesIO("\x15\x16")
    format = format_(2)
    context = {}
    value = format.read(stream, context)
    assert value == 0x1615

    # test three-byte values (our decoder)
    stream = BytesIO("\x15\x16\x17")
    format = format_(3)
    context = {}
    value = format.read(stream, context)
    assert value == 0x171615

    # test endianness
    stream = BytesIO("\x15\x16\x17")
    format = format_(3, ">")
    context = {}
    value = format.read(stream, context)
    assert value == 0x151617

    # test 'L' format to guarantee non-special alignment
    stream = BytesIO("\x15\x16\x17\x18")
    format = format_(4)
    context = {}
    value = format.read(stream, context)
    assert value == 0x18171615

def _test_IntBase_write_base(format_):
    # test one-byte values
    stream = BytesIO()
    format = format_(1)
    context = {}
    format.write(stream, 0x25, context)
    assert stream.getvalue() == "\x25"

    # test two-byte values
    stream = BytesIO()
    format = format_(2)
    context = {}
    format.write(stream, 0x1516, context)
    assert stream.getvalue() == "\x16\x15"

    # test three-byte values (our decoder)
    stream = BytesIO()
    format = format_(3)
    context = {}
    format.write(stream, 0x171615, context)
    assert stream.getvalue() == "\x15\x16\x17"

    # test endianness
    stream = BytesIO()
    format = format_(3, ">")
    context = {}
    format.write(stream, 0x151617, context)
    assert stream.getvalue() == "\x15\x16\x17"

    # test 'L' format to guarantee non-special alignment
    stream = BytesIO()
    format = format_(4)
    context = {}
    format.write(stream, 0x18171615, context)
    assert stream.getvalue() == "\x15\x16\x17\x18"

def test_UInt_read():
    _test_IntBase_read_base(UInt)

    # test high values
    stream = BytesIO("\xA0")
    format = UInt(1)
    context = {}
    value = format.read(stream, context)
    assert value == 0xA0

    # test three-byte values (our decoder)
    stream = BytesIO("\xFF\xFF\xFF")
    format = UInt(3)
    context = {}
    value = format.read(stream, context)
    assert value == 2**24-1

def test_UInt_write():
    _test_IntBase_write_base(UInt)

    # test high values
    stream = BytesIO()
    format = UInt(1)
    context = {}
    format.write(stream, 0xA0, context)
    assert stream.getvalue() == "\xA0"

    # test three-byte values (our decoder)
    stream = BytesIO()
    format = UInt(3)
    context = {}
    format.write(stream, 2**24-1, context)
    assert stream.getvalue() == "\xFF\xFF\xFF"

def test_SInt_read():
    _test_IntBase_read_base(SInt)

    # test high values
    stream = BytesIO("\xA0")
    format = SInt(1)
    context = {}
    value = format.read(stream, context)
    assert value == 0xA0-256

    # test three-byte values (our decoder)
    stream = BytesIO("\xFF\xFF\xFF")
    format = SInt(3)
    context = {}
    value = format.read(stream, context)
    assert value == -1

def test_SInt_write():
    _test_IntBase_write_base(SInt)

    # test high values
    stream = BytesIO()
    format = SInt(1)
    context = {}
    format.write(stream, 0xA0-256, context)
    assert stream.getvalue() == "\xA0"

    # test three-byte values (our decoder)
    stream = BytesIO()
    format = SInt(3)
    context = {}
    format.write(stream, -1, context)
    assert stream.getvalue() == "\xFF\xFF\xFF"
