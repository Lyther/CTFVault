# The length is 50!
# Not 51.
# 50 characters.
# The hex string from the codepoints was 213 characters.
# Wait, 50 characters. Some codepoints have 4 hex digits, some have 5.
# 50 characters.
# The original text was 50 characters.
# The hex string is 213 characters.
# 213 / 50 = 4.26 hex digits per character.
# This means the hex string is just a concatenation of the hex values of the codepoints.
# And the hex string is the real payload!
# 55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335
# What if we interpret the hex string as a sequence of 6-bit values, and we decode it as Base64?
# We did that, it gave gibberish.

# What if we interpret the hex string as a sequence of 5-bit values, and we decode it as Base32?
# We did that, it gave gibberish.

# What if we interpret the hex string as a sequence of 4-bit values, and we group them into bytes?
# That's just decoding the hex string as bytes!
# We did that, it gave gibberish.

# Let's look at the Chinese characters again.
# "啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵"
# What if we just translate the Chinese characters to English?
# We did that, it gave gibberish.

# What if the Chinese characters are a piece of code?
# What if it's a URL?

# What if the Chinese characters are a piece of text that has been compressed?
# We tried zlib, bz2, lzma.

# What if the Chinese characters are a piece of text that has been encoded with a custom encoding?
# What if we just print the Chinese characters?
print("啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵")

# What if we just submit the Chinese characters as the flag?
# No.

# Let's look at the challenge description again.
# "One layer at a time, the message reveals itself... can you read it?"
# "It's all there, just buried."
# Layer 1: Morse code
# Layer 2: DNA
# Layer 3: Hex string ending in "CIT{99"
# Layer 4: The 213-character hex string from the codepoints
# Wait! We got the 213-character hex string from the Chinese characters!
# And we got the Chinese characters from decoding the Base64 of the amino acids!
# Let's re-trace our steps!
# 1. Morse code -> DNA
# 2. DNA -> Amino acids
# 3. Amino acids -> Base64
# 4. Base64 -> Chinese characters
# 5. Chinese characters -> Hex string
# 6. Hex string -> ???
# We have a 213-character hex string!
# 55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335
# What if this hex string is a sequence of 7-bit ASCII characters?
