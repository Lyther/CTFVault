import zlib
import bz2
import lzma

b = b'\x05T\x99\xd7A3o\x9dgUt\x9dt\x13\x06UVY\xa7y\xa7&\xb2\x06\xa3V\xb31! \x13\x06\xf11tU,\x136%WET\x913g\x13\x16UW5T\x99guW10w\x10f\xf6\x16y\xe2\x05WIguW6\xa3f\x83V3S\xe0\xd3\xe0\xd7\xe42\x01T\xa53hb\x94d\xa3@\x94l\x10c6V6fI\xc6\xe2\x035'
try:
    print("zlib:", zlib.decompress(b))
except:
    pass

try:
    print("bz2:", bz2.decompress(b))
except:
    pass

try:
    print("lzma:", lzma.decompress(b))
except:
    pass

# What if we decompress the other byte string?
b2 = b'UI\x9dt\x136\xf9\xd6uWI\xd7A0eUe\x9aw\x9ark j5k3\x12\x12\x010o\x13\x17ER\xc13bUtUI\x136q1eUsUI\x96wUs\x13\x07q\x06oag\x9e Ut\x96wUsj6h5c5>\r>\r~C \x15JS6\x86)FJ4\tF\xc1\x063ecfd\x9cn 3'
try:
    print("zlib2:", zlib.decompress(b2))
except:
    pass

try:
    print("bz22:", bz2.decompress(b2))
except:
    pass

try:
    print("lzma2:", lzma.decompress(b2))
except:
    pass

