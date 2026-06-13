# In decode45.py, I created a byte array `res` from the mapped codons.
# Then I printed `res.decode('ascii')`, which gave the Base64 string!
# Then I decoded the Base64 string to get the bytes!
# And the bytes decoded to UTF-8!
# This means the Base64 string is VALID!
# And the Base64 string is exactly 213 characters long?
# No, `res` is 220 bytes long!
# Wait, if `res` is 220 bytes long, and it's a valid Base64 string, then it decodes to 165 bytes!
# And those 165 bytes decode to UTF-8!
# Let's check the Base64 string again!
# "5ZWJ6bW08JONr+m1p+WVtOm1tPCTgaXllaXpqbfpqbLmrKDmqLXmrLPwkoSg8JOBr/CThbTllKzwk42i5ZW05ZWJ8JONp/CThaXllbPllYnpmbfllbPwk4G38JCZr+aFp+m4oOWVtOmZt+WVs+aotuagteaMteO4jeO4jee5g/CghZTqlLPmoaLpkaTqjYDpkazwkJiz5pWj5pmk6bGu8KCMtQ=="
# This is a valid Base64 string!
# And it decodes to the Chinese characters!
# 啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵
# So the Chinese characters ARE the payload!
# And we got them by mapping the codons to 4-bit values!
# The mapping was:
# 'GGA': 10, 'GGC': 11, 'GGG': 12, 'GGT': 13, 'GTA': 14, 'GTC': 15,
# 'TCG': 0, 'TCT': 1, 'TGA': 2, 'TGC': 3, 'TGG': 4, 'TGT': 5,
# 'TTA': 6, 'TTC': 7, 'TTG': 8, 'TTT': 9
# Wait, this mapping gave us a valid Base64 string!
# How did I find this mapping?
# I just did `(i - 6) % 16` on the ordered list of codons!
# Why did that work?
# Because the codons were ordered alphabetically!
# GGA, GGC, GGG, GGT, GTA, GTC, TCG, TCT, TGA, TGC, TGG, TGT, TTA, TTC, TTG, TTT
# And the mapping is just the index shifted by 6!
# This is an INCREDIBLE coincidence, or it's the intended solution!
# If it's the intended solution, then the Chinese characters are the next layer!
# The Chinese characters are:
# 啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵
# We already extracted the codepoints of these characters and concatenated them into a hex string:
# 55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335
# And we noticed that this hex string is 213 characters long.
# What if the hex string is the payload, and we need to decode it?
# Let's look at the Chinese characters again.
# "啉" is U+5549.
# "鵴" is U+9D74.
# "𓍯" is U+1336F.
# "鵧" is U+9D67.
# "啴" is U+5574.
# Notice that the codepoints are exactly the hex string!
# So the Chinese characters are just a way to encode the hex string!
# The hex string is the real payload!
# But what is the hex string?
# 55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335
# We tried to decode it as Base64, Base32, Ascii85, Z85, etc.
# We tried to decode it as bytes, and got gibberish.
# What if we decode the hex string as Base58?
import base58
try:
    val = int("55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335", 16)
    b = val.to_bytes((val.bit_length() + 7) // 8, 'big')
    print(base58.b58encode(b))
except Exception as e:
    pass
