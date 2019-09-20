import struct
from collections import namedtuple

ByteOrderStructPair = namedtuple('ByteOrderStructPair', ['one_codeunit', 'two_codeunit'])

_byteorder_encode_structs = {
    'little': ByteOrderStructPair(
        struct.Struct('<H'),
        struct.Struct('<2H')
    ),
    'big': ByteOrderStructPair(
        struct.Struct('>H'),
        struct.Struct('>2H')
    ),
}

_byteorder_decode_structs = {
    'little': struct.Struct('<H'),
    'big': struct.Struct('>H')
}


def _encode_utf16(s: str, byteorder: str):
    encoded = b''
    for i, c in enumerate(s):
        codepoint = ord(c)
        if 0xD800 <= codepoint <= 0xDFFF:
            raise ValueError(f"Codepoint {hex(codepoint)} at index {i} is in surrogate pair range of 0xD800 to 0xDFFF")
        if codepoint <= 0xFFFF:
            encoded += _byteorder_encode_structs[byteorder].one_codeunit.pack(codepoint)
        else:
            codepoint_lower_16 = codepoint & ~0x10000
            encoded += _byteorder_encode_structs[byteorder].two_codeunit.pack(
                (codepoint_lower_16 >> 10) | 0xD800,
                (codepoint_lower_16 & 0x3ff) | 0xDC00
            )
    return encoded


def encode_utf16le(s: str):
    return _encode_utf16(s, 'little')


def encode_utf16be(s: str):
    return _encode_utf16(s, 'big')


def _decode_utf16(b: bytes, byteorder: str):
    decoded = list()
    it = map(lambda t: t[0], _byteorder_decode_structs[byteorder].iter_unpack(b))
    while True:
        try:
            first_unit = next(it)
        except StopIteration:
            return "".join(chr(c) for c in decoded)
        if 0xD800 <= first_unit <= 0xDBFF:
            # start of surrogate pair
            decoded.append(((first_unit & ~0xD800) << 10) + (next(it) & ~0xDC00) | 0x10000)
        else:
            decoded.append(first_unit)


def decode_utf16le(b: bytes):
    return _decode_utf16(b, 'little')


def decode_utf16be(b: bytes):
    return _decode_utf16(b, 'big')
