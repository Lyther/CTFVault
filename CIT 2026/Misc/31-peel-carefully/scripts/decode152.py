# The key for Vigenere cipher is gibberish.
# So it's not a Vigenere cipher.

# What if the string "Itogtteewr 53 ot,btIgesIwswog tws655\r\rCT3bd@l3cdn5" is a piece of text that has been encoded with a custom encoding?
# Let's count the number of unique characters in the string.
text = "Itogtteewr 53 ot,btIgesIwswog tws655\r\rCT3bd@l3cdn5"
print("Unique chars:", len(set(text)))
# 22 unique characters.

# What if the string is a piece of text that has been encoded with a transposition cipher?
# Let's check the characters.
# I, t, o, g, t, t, e, e, w, r,  , 5, 3,  , o, t, ,, b, t, I, g, e, s, I, w, s, w, o, g,  , t, w, s, 6, 5, 5, \r, \r, C, T, 3, b, d, @, l, 3, c, d, n, 5
# Wait, "CT3bd@l3cdn5" is 12 characters.
# "Itogtteewr 53 ot,btIgesIwswog tws655" is 36 characters.
# 36 + 2 (\r\r) + 12 = 50 characters.
# The original text had 51 characters.
# Where is the 51st character?
# Let's check the length of the string.
print("Length:", len(text))
# 50 characters.
# The original text had 51 characters.
# What happened to the 51st character?
# Let's check the original Chinese characters again.
orig_text = "啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵"
print("Original length:", len(orig_text))
# 51 characters.
# Let's check the modulo 256 string again.
dec = "".join(chr(ord(c) % 256) if 32 <= ord(c) % 256 <= 126 else "." for c in orig_text)
print(dec)
# "Itogtteewr 53 ot,btIgesIwswog tws655..CT3bd@l3cdn5"
# The two dots are the \r\r.
# And the last character is '5'.
# Wait, "Itogtteewr 53 ot,btIgesIwswog tws655..CT3bd@l3cdn5" is 51 characters!
# I just miscounted.

# What if the string is a piece of text that has been encoded with a custom encoding?
# What if we take the codepoints modulo 256, and then decode them as ASCII?
# We did that, and we got:
# "Itogtteewr 53 ot,btIgesIwswog tws655\r\rCT3bd@l3cdn5"
# Wait, what if the string is NOT a substitution cipher?
# What if the string is a piece of code?
# What if the string is a URL?
# What if the string is a Base64 string?
# It has characters outside Base64.
# What if the string is a Base85 string?
# It has characters outside Base85.
# What if the string is a Base91 string?
# It has characters outside Base91.

# Let's look at the Chinese characters again.
# "啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵"
# Is it possible that the Chinese characters are just a translation of the flag?
# No, we checked, it's not a translation.
# What if the Chinese characters are a piece of text that has been compressed?
# We tried zlib, bz2, lzma.
