import struct

_byteorder_structs = {
    'little': struct.Struct('<I'),
    'big': struct.Struct('>I'),
}


def _encode_utf32(s: str, byteorder: str):
    return b''.join(_byteorder_structs[byteorder].pack(ord(c)) for c in s)


def encode_utf32le(s: str):
    return _encode_utf32(s, 'little')


def encode_utf32be(s: str):
    return _encode_utf32(s, 'big')


def _decode_utf32(b: bytes, byteorder: str):
    return "".join(chr(c[0]) for c in _byteorder_structs[byteorder].iter_unpack(b))


def decode_utf32le(b: bytes):
    return _decode_utf32(b, 'little')


def decode_utf32be(b: bytes):
    return _decode_utf32(b, 'big')
