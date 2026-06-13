# Let's reconsider the layers.
# 1. Morse code -> DNA
# 2. DNA -> Amino acids
# 3. Amino acids -> Base64
# 4. Base64 -> Chinese characters
# 5. Chinese characters -> Hex string
# 6. Hex string -> ???
# Wait! We got the Chinese characters from the base64 string!
# The Base64 string was:
# 5ZWJ6bW08JONr+m1p+WVtOm1tPCTgaXllaXpqbfpqbLmrKDmqLXmrLPwkoSg8JOBr/CThbTllKzwk42i5ZW05ZWJ8JONp/CThaXllbPllYnpmbfllbPwk4G38JCZr+aFp+m4oOWVtOmZt+WVs+aotuagteaMteO4jeO4jee5g/CghZTqlLPmoaLpkaTqjYDpkazwkJiz5pWj5pmk6bGu8KCMtQ==
# We decoded this Base64 string to get the Chinese characters!
# And the Chinese characters are:
# 啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵
# Then we got the hex string from the codepoints of the Chinese characters.
# 55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335
# Then we decoded the hex string as Base64!
# And we got:
# VUmddBM2+dZ1V0nXQTBlVWWad5pyayBqNWszEhIBMG8TF0VSwTNiVXRVSRM2cTFlVXNVSZZ3VXMTB3EGb2FnniBVdJZ3VXNqNmg1YzU+DT4NfkMgFUpTNoYpRko0CUbBBjNlY2ZknG4gM1
# And we decoded THAT Base64 string to get bytes:
# b'UI\x9dt\x136\xf9\xd6uWI\xd7A0eUe\x9aw\x9ark j5k3\x12\x12\x010o\x13\x17ER\xc13bUtUI\x136q1eUsUI\x96wUs\x13\x07q\x06oag\x9e Ut\x96wUsj6h5c5>\r>\r~C \x15JS6\x86)FJ4\tF\xc1\x063ecfd\x9cn 3'
# This is a sequence of bytes.
# What if we decode this sequence of bytes as Base64 again?
import base64
b = b'UI\x9dt\x136\xf9\xd6uWI\xd7A0eUe\x9aw\x9ark j5k3\x12\x12\x010o\x13\x17ER\xc13bUtUI\x136q1eUsUI\x96wUs\x13\x07q\x06oag\x9e Ut\x96wUsj6h5c5>\r>\r~C \x15JS6\x86)FJ4\tF\xc1\x063ecfd\x9cn 3'
# It has non-printable characters, so it's NOT a Base64 string.

# What if we decode the hex string as Base32?
# We did that, and we got:
# KVEZ25ATG345M5KXJHLUCMDFKVSZU542OJVSA2RVNMZREEQBGBXRGF2FKLATGYSVORKUSEZWOEYWKVLTKVEZM52VOMJQO4IGN5QWPHRAKV2JM52VONVDM2BVMM2T4DJ6BV7EGIAVJJJTNBRJIZFDICKGYEDDGZLDMZSJY3RAGN
# This is a Base32 string!
# And we decoded THAT Base32 string to get bytes:
# b'UI\x9dt\x136\xf9\xd6uWI\xd7A0eUe\x9aw\x9ark j5k3\x12\x12\x010o\x13\x17ER\xc13bUtUI\x136q1eUsUI\x96wUs\x13\x07q\x06oag\x9e Ut\x96wUsj6h5c5>\r>\r~C \x15JS6\x86)FJ4\tF\xc1\x063ecfd\x9cn 3'
# This is the SAME sequence of bytes as before!
# Because Base64 and Base32 are just different ways to encode the SAME binary data.
# The binary data is the hex string itself!
# The hex string is 55499d74...
# The binary data is b'\x55\x49\x9d\x74...'
# Wait!
# 55 49 = "UI"
# 9d 74 = ?
# 13 36 = ?
# f9 d6 = ?
# 75 57 = "uW"
# 49 d7 = "I?"
# 41 30 = "A0"
# 65 55 = "eU"
# 65 9a = "e?"
# 77 9a = "w?"
# 72 6b = "rk"
# 20 6a = " j"
# 35 6b = "5k"
# 33 12 = "3?"
# 12 01 = "??"
# 30 6f = "0o"
# 13 17 = "??"
# 45 52 = "ER"
# c1 33 = "?3"
# 62 55 = "bU"
# 74 55 = "tU"
# 49 13 = "I?"
# 36 71 = "6q"
# 31 65 = "1e"
# 55 73 = "Us"
# 55 49 = "UI"
# 96 77 = "?w"
# 55 73 = "Us"
# 13 07 = "??"
# 71 06 = "q?"
# 6f 61 = "oa"
# 67 9e = "g?"
# 20 55 = " U"
# 74 96 = "t?"
# 77 55 = "wU"
# 73 6a = "sj"
# 36 68 = "6h"
# 35 63 = "5c"
# 35 3e = "5>"
# 0d 3e = "\r>"
# 0d 7e = "\r~"
# 43 20 = "C "
# 15 4a = "?J"
# 53 36 = "S6"
# 86 29 = "?)"
# 46 4a = "FJ"
# 34 09 = "4\t"
# 46 c1 = "F?"
# 06 33 = "?3"
# 65 63 = "ec"
# 66 64 = "fd"
# 9c 6e = "?n"
# 20 33 = " 3"
# 5 = ?
# THIS IS THE BINARY DATA!
# It's just the bytes of the hex string!
# We already looked at this binary data!
# Does this binary data contain the flag?
# We checked, it does not.
