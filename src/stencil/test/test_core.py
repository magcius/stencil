
from io import BytesIO
from stencil.core import UnsignedByteField

def test_bytefield():
    stream = BytesIO()
    fields = [UnsignedByteField(name) for name in ("a", "b", "c")]
    values = [5, 6, 7] 
    context = {}
    for field, value in zip(fields, values):
        field.write(stream, value, context)

    assert stream.getvalue() == b"\x05\x06\x07"