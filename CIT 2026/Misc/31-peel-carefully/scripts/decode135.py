# Let's write a simple base58 decoder
alphabet = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def b58decode(v):
    v = v.lstrip(b'1')
    acc = 0
    for char in v:
        acc = acc * 58 + alphabet.index(char)
    return acc.to_bytes((acc.bit_length() + 7) // 8, 'big')

try:
    b = b"55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335"
    print(b58decode(b))
except Exception as e:
    print(e)
