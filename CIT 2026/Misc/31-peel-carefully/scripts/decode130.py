# Let's look at the binary data again.
# b'\x05T\x99\xd7A3o\x9dgUt\x9dt\x13\x06UVY\xa7y\xa7&\xb2\x06\xa3V\xb31! \x13\x06\xf11tU,\x136%WET\x913g\x13\x16UW5T\x99guW10w\x10f\xf6\x16y\xe2\x05WIguW6\xa3f\x83V3S\xe0\xd3\xe0\xd7\xe42\x01T\xa53hb\x94d\xa3@\x94l\x10c6V6fI\xc6\xe2\x035'
# Wait!
# The binary data is 107 bytes long.
# What if we XOR it with a repeating key?
# We did that, it failed.

# What if the binary data is a piece of code?
# What if the binary data is a compressed string?
# We tried zlib, bz2, lzma.

# What if the binary data is a Base64 string but with a custom alphabet?
# No, it's binary data.

# Let's look at the Chinese characters again.
# 啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵
# There are 51 characters.
# What if the codepoints are NOT hex strings?
# What if the codepoints are just numbers, and we need to convert them to something else?
# Let's write the codepoints in decimal:
# 21833, 40308, 78703, 40295, 21876, 40308, 77925, 21861, 39543, 39538, 27424, 27189, 27443, 74016, 77935, 78196, 21804, 78690, 21876, 21833, 78695, 78181, 21875, 21833, 38519, 21875, 77943, 67183, 24935, 40480, 21876, 38519, 21875, 27190, 26677, 25397, 15885, 15885, 32323, 131412, 42291, 26722, 37988, 41792, 37996, 67123, 25955, 26212, 40046, 131893
# What if we convert them to characters?
# We did that, it gave us the Chinese characters.

# What if we interpret the codepoints as UTF-8 bytes?
# We did that, it gave us the UTF-8 bytes of the Chinese characters.

# What if we interpret the codepoints as UTF-16 bytes?
# We did that, it gave us the UTF-16 bytes of the Chinese characters.

# What if we interpret the codepoints as UTF-32 bytes?
# We did that, it gave us the UTF-32 bytes of the Chinese characters.

# What if the codepoints are just a sequence of numbers, and we need to decode them with a custom encoding?
# What if we subtract a constant from each codepoint?
# What if we divide each codepoint by a constant?
# What if we take the modulo of each codepoint?
# We tried modulo 256 and modulo 128.
# Modulo 256 gave:
# Itogtteewr 53 ot,btIgesIwswog tws655\r\rCT3bd@l3cdn5
# Modulo 128 gave:
# Itogtteewr 53 ot,btIgesIwswog tws655\r\rCT3bd@l3cdn5
# Wait!
# "Itogtteewr 53 ot,btIgesIwswog tws655\r\rCT3bd@l3cdn5"
# This looks like English!
# "Itogtteewr" -> "It got tee wr"?
# "53 ot,btIgesIwswog tws655" -> "53 ot, bt I ges I wswog tws 655"?
# "CT3bd@l3cdn5" -> "CT3bd@l3cdn5"?
# It looks like a substitution cipher!
# Let's try to break the substitution cipher on this string!
