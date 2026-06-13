# Let's look at the original text again.
text = "啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵"
# Is there any other way to extract data from the codepoints?
codepoints = [ord(c) for c in text]
# What if we take the codepoints modulo 256?
# What if we take the codepoints modulo 10?
# What if we take the codepoints modulo 16?
# What if we take the codepoints modulo 2?
# What if the codepoints are indices into a dictionary?
# There are 51 codepoints.
# What if the codepoints are just Unicode characters, and we need to translate them?
# Let's translate them!
# 啉 = "lin"
# 鵴 = "ju"
# 𓍯 = ? (Egyptian Hieroglyph)
# 鵧 = "pi"
# 啴 = "tan"
# 鵴 = "ju"
# 𓁥 = ? (Egyptian Hieroglyph)
# 啥 = "sha"
# 驷 = "si"
# 驲 = "ri"
# 欠 = "qian"
# 樵 = "qiao"
# 欳 = "kui"
# 𒄠 = ? (Cuneiform)
# 𓁯 = ? (Egyptian Hieroglyph)
# 𓅴 = ? (Egyptian Hieroglyph)
# 唬 = "hu"
# 𓍢 = ? (Egyptian Hieroglyph)
# 啴 = "tan"
# 啉 = "lin"
# 𓍧 = ? (Egyptian Hieroglyph)
# 𓅥 = ? (Egyptian Hieroglyph)
# 啳 = "quan"
# 啉 = "lin"
# 陷 = "xian"
# 啳 = "quan"
# 𓁷 = ? (Egyptian Hieroglyph)
# 𐙯 = ? (Linear A)
# 慧 = "hui"
# 鸠 = "jiu"
# 啴 = "tan"
# 陷 = "xian"
# 啳 = "quan"
# 樶 = "zui"
# 栵 = "lie"
# 挵 = "nong"
# 㸍 = ?
# 㸍 = ?
# 繃 = "beng"
# 𠅔 = ?
# ꔳ = ? (Vai)
# 桢 = "zhen"
# 鑤 = "bao"
# ꍀ = ? (Yi)
# 鑬 = "lan"
# 𐘳 = ? (Linear B)
# 散 = "san"
# 晤 = "wu"
# 鱮 = "xu"
# 𠌵 = ?

# This looks like a random collection of Unicode characters.
# Why these specific characters?
# Because their hex representations concatenate to the hex string!
# 5549, 9d74, 1336f, 9d67, 5574, 9d74, 13065, 5565...
# So the characters themselves are just a way to encode the hex string!
# The hex string is the real payload!
# But what is the hex string?
# 55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335
# And we know that this hex string is 213 characters long.
# And we know that 213 is not a multiple of 2.
# So it's not a sequence of bytes.
# But what if we pad it with a 0 at the beginning?
# We did that, and we got 107 bytes.
# b'\x05T\x99\xd7A3o\x9dgUt\x9dt\x13\x06UVY\xa7y\xa7&\xb2\x06\xa3V\xb31! \x13\x06\xf11tU,\x136%WET\x913g\x13\x16UW5T\x99guW10w\x10f\xf6\x16y\xe2\x05WIguW6\xa3f\x83V3S\xe0\xd3\xe0\xd7\xe42\x01T\xa53hb\x94d\xa3@\x94l\x10c6V6fI\xc6\xe2\x035'
# Does this look like a flag? No.
