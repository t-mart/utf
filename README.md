# utf

A Python implementation of Unicode encoding and decoding, despite Python already having
functions for this anyway. I built this project to explore how the Unicode standard works.

This code won't recognize broken UTF-8 continuation byte prefixes or UTF-16 lower surrogate prefixes and just assumes they are the correct format. (If you think about it, these byte prefixes are redundant because the leading byte of each encoded character already signals the number of continuation bytes or surrogacy. These prefixes *are* however useful if you're seeking arbitrarily around a byte stream and need to build the current character.) But, if you work with strings/bytes from the respective Python functions, you should not run into any problems.

There may be other problems I haven't thought of either.

## API
```python
from utf import encode_utf8, decode_utf8
from utf import encode_utf16be, decode_utf16be, encode_utf16le, decode_utf16le
from utf import encode_utf32be, decode_utf32be, encode_utf32le, decode_utf32le
```

Encoding functions take a string object as the only argument.

Decoding functions take a bytes object as the only argument.

## Tests
```bash
pytest
```