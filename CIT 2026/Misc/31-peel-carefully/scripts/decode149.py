# Let's look at the Chinese characters again.
text = "啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵"
# What if the Chinese characters are just an obfuscated string?
# What if we encode the Chinese characters as UTF-8, and then decode it as something else?
utf8_bytes = text.encode('utf-8')
print("UTF-8 bytes:", utf8_bytes)

# What if we decode it as Base64?
import base64
try:
    print(base64.b64decode(utf8_bytes))
except Exception as e:
    print(e)
    
# What if we decode it as Base32?
try:
    print(base64.b32decode(utf8_bytes))
except Exception as e:
    print(e)

# What if we decode it as Base85?
try:
    print(base64.b85decode(utf8_bytes))
except Exception as e:
    print(e)

# What if we decode it as Ascii85?
try:
    print(base64.a85decode(utf8_bytes))
except Exception as e:
    print(e)

# What if we decompress it?
import zlib
try:
    print(zlib.decompress(utf8_bytes))
except Exception as e:
    print(e)

import bz2
try:
    print(bz2.decompress(utf8_bytes))
except Exception as e:
    print(e)

import lzma
try:
    print(lzma.decompress(utf8_bytes))
except Exception as e:
    print(e)
