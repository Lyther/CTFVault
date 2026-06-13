# Let's look at the base64 string again.
b64_str = "VUmddBM2+dZ1V0nXQTBlVWWad5pyayBqNWszEhIBMG8TF0VSwTNiVXRVSRM2cTFlVXNVSZZ3VXMTB3EGb2FnniBVdJZ3VXNqNmg1YzU+DT4NfkMgFUpTNoYpRko0CUbBBjNlY2ZknG4gM1"
# And the decoded bytes:
# b'UI\x9dt\x136\xf9\xd6uWI\xd7A0eUe\x9aw\x9ark j5k3\x12\x12\x010o\x13\x17ER\xc13bUtUI\x136q1eUsUI\x96wUs\x13\x07q\x06oag\x9e Ut\x96wUsj6h5c5>\r>\r~C \x15JS6\x86)FJ4\tF\xc1\x063ecfd\x9cn 3'
# This is a sequence of 106 bytes.
# What if it's a piece of text that has been encrypted with a repeating key XOR?
# We checked, it's not XORed.

# What if it's a Vigenere cipher?
# We checked, it's not a Vigenere cipher.

# What if it's a substitution cipher?
# We checked, it's not a substitution cipher.

# What if it's a transposition cipher?
# We checked, it's not a transposition cipher.

# Let's look at the original Chinese characters again.
text = "啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵"
# Is it possible that the Chinese characters are a piece of text that has been encoded with a custom encoding?
# What if we just translate the Chinese characters to English?
# "啉" = "drink"
# "鵴" = "a kind of bird"
# "𓍯" = Egyptian Hieroglyph V028
# "鵧" = "a kind of bird"
# "啴" = "pant"
# "鵴" = "a kind of bird"
# "𓁥" = Egyptian Hieroglyph A042
# "啥" = "what"
# "驷" = "team of four horses"
# "驲" = "post horse"
# "欠" = "owe"
# "樵" = "firewood"
# "欳" = "pant"
# "𒄠" = Cuneiform sign AM
# "𓁯" = Egyptian Hieroglyph A052
# "𓅴" = Egyptian Hieroglyph G043
# "唬" = "bluff"
# "𓍢" = Egyptian Hieroglyph V001
# "啴" = "pant"
# "啉" = "drink"
# "𓍧" = Egyptian Hieroglyph V006
# "𓅥" = Egyptian Hieroglyph G028
# "啳" = "pant"
# "啉" = "drink"
# "陷" = "trap"
# "啳" = "pant"
# "𓁷" = Egyptian Hieroglyph D002
# "𐙯" = Linear A sign AB054
# "慧" = "wisdom"
# "鸠" = "dove"
# "啴" = "pant"
# "陷" = "trap"
# "啳" = "pant"
# "樶" = "a kind of tree"
# "栵" = "a kind of tree"
# "挵" = "play with"
# "㸍" = "fire"
# "㸍" = "fire"
# "繃" = "bind"
# "𠅔" = CJK Unified Ideograph-20154
# "ꔳ" = Vai syllable ta
# "桢" = "a kind of tree"
# "鑤" = "plane"
# "ꍀ" = Yi syllable pu
# "鑬" = "look at"
# "𐘳" = Linear B syllable ta
# "散" = "scatter"
# "晤" = "meet"
# "鱮" = "a kind of fish"
# "𠌵" = CJK Unified Ideograph-20335

# This is definitely gibberish.
# The payload is definitely the hex string of the codepoints!
# 55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335
# And we know that this hex string is 213 characters long.
# And we know that 213 is not a multiple of 2.
# So it's not a sequence of bytes.
# But what if we pad it with a 0 at the beginning?
# We did that, and we got 107 bytes.
# b'\x05T\x99\xd7A3o\x9dgUt\x9dt\x13\x06UVY\xa7y\xa7&\xb2\x06\xa3V\xb31! \x13\x06\xf11tU,\x136%WET\x913g\x13\x16UW5T\x99guW10w\x10f\xf6\x16y\xe2\x05WIguW6\xa3f\x83V3S\xe0\xd3\xe0\xd7\xe42\x01T\xa53hb\x94d\xa3@\x94l\x10c6V6fI\xc6\xe2\x035'
# Does this look like a flag? No.
