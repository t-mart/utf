import struct

_CONTINUATION_PREFIX = 0b1000_0000
_CONTINUATION_MASK = 0b0011_1111

_TWO_BYTE_PREFIX = 0b1100_0000
_THREE_BYTE_PREFIX = 0b1110_0000
_FOUR_BYTE_PREFIX = 0b1111_0000

_ONE_BYTE_STRUCT = struct.Struct('B')
_TWO_BYTE_STRUCT = struct.Struct('2B')
_THREE_BYTE_STRUCT = struct.Struct('3B')
_FOUR_BYTE_STRUCT = struct.Struct('4B')


def encode_utf8(s: str):
    encoded = b''
    for c in s:
        codepoint = ord(c)
        if codepoint < 0x80:
            encoded += _ONE_BYTE_STRUCT.pack(codepoint)
        elif codepoint < 0x800:
            encoded += _TWO_BYTE_STRUCT.pack(
                _TWO_BYTE_PREFIX | (codepoint >> 6),
                _CONTINUATION_PREFIX | (codepoint & _CONTINUATION_MASK),
            )
        elif codepoint < 0x10000:
            encoded += _THREE_BYTE_STRUCT.pack(
                _THREE_BYTE_PREFIX | (codepoint >> 12),
                _CONTINUATION_PREFIX | ((codepoint >> 6) & _CONTINUATION_MASK),
                _CONTINUATION_PREFIX | (codepoint & _CONTINUATION_MASK),
            )
        else:
            encoded += _FOUR_BYTE_STRUCT.pack(
                _FOUR_BYTE_PREFIX | (codepoint >> 18),
                _CONTINUATION_PREFIX | ((codepoint >> 12) & _CONTINUATION_MASK),
                _CONTINUATION_PREFIX | ((codepoint >> 6) & _CONTINUATION_MASK),
                _CONTINUATION_PREFIX | (codepoint & _CONTINUATION_MASK),
            )
    return encoded


def decode_utf8(b: bytes):
    decoded = list()
    it = iter(b)
    while True:
        try:
            first_byte = next(it)
        except StopIteration:
            return "".join(chr(c) for c in decoded)
        if first_byte & _FOUR_BYTE_PREFIX == _FOUR_BYTE_PREFIX:
            decoded.append(
                ((first_byte & ~_FOUR_BYTE_PREFIX) << 18)
                + ((next(it) & _CONTINUATION_MASK) << 12)
                + ((next(it) & _CONTINUATION_MASK) << 6)
                + (next(it) & _CONTINUATION_MASK)
            )
        elif first_byte & _THREE_BYTE_PREFIX == _THREE_BYTE_PREFIX:
            decoded.append(
                ((first_byte & ~_THREE_BYTE_PREFIX) << 12)
                + ((next(it) & _CONTINUATION_MASK) << 6)
                + (next(it) & _CONTINUATION_MASK)
            )
        elif first_byte & _TWO_BYTE_PREFIX == _TWO_BYTE_PREFIX:
            decoded.append(((first_byte & ~_TWO_BYTE_PREFIX) << 6) + (next(it) & _CONTINUATION_MASK))
        else:
            decoded.append(first_byte)
