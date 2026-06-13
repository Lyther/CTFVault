s3 = b'7~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=LCIT{99'

# What if the string is just XORed with a repeating key?
# Let's try to find the key.
# We know the flag starts with "CIT{".
# Where is "CIT{" in the string?
# It's at the end! "CIT{99"
# So the key for the last 6 characters is 0.
# If the key is 0, then the key is a repeating sequence of 0s.
# But the rest of the string is gibberish.
# So the key is NOT a repeating sequence of 0s.
# What if the key is a repeating sequence of characters?
# If the key is a repeating sequence of characters, then the key for the last 6 characters is 0.
# This means the key must be 0 for those 6 characters.
# So the key must be 0 everywhere!
# But the rest of the string is gibberish.
# This means the string is NOT XORed with a repeating key.

# What if the string is a Vigenere cipher?
# If it's a Vigenere cipher, the key for the last 6 characters is 0.
# So the key must be 0 everywhere!
# But the rest of the string is gibberish.
# This means the string is NOT a Vigenere cipher.

# What if the string is a substitution cipher?
# If it's a substitution cipher, then 'C' -> 'C', 'I' -> 'I', 'T' -> 'T', '{' -> '{', '9' -> '9'.
# We already tried to break it with simulated annealing, and it failed.
# Why did it fail?
# Maybe the text is NOT English!
# What if the text is a piece of code?
# What if the text is a URL?
# What if the text is a base64 string?
# If the text is a base64 string, then the substitution cipher would map the 52 unique characters to the 64 base64 characters.
# But we don't know the mapping.
# And base64 strings don't have bigram frequencies like English text.
# So simulated annealing wouldn't work.

# What if the string is NOT a substitution cipher?
# What if the string is a transposition cipher?
# If it's a transposition cipher, the characters are just rearranged.
# But the characters are gibberish.
# So it's NOT a transposition cipher.

# What if the string is a piece of text that has been encoded with a custom base encoding?
# We checked, it's not Base52.

# What if the string is a piece of text that has been encoded with a custom encoding?
# Let's look at the original text again.
text = "啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵"
# We know that the codepoints are:
# 21833, 40308, 78703, 40295, 21876, 40308, 77925, 21861, 39543, 39538, 27424, 27189, 27443, 74016, 77935, 78196, 21804, 78690, 21876, 21833, 78695, 78181, 21875, 21833, 38519, 21875, 77943, 67183, 24935, 40480, 21876, 38519, 21875, 27190, 26677, 25397, 15885, 15885, 32323, 131412, 42291, 26722, 37988, 41792, 37996, 67123, 25955, 26212, 40046, 131893
# We converted them to hex strings:
# 5549, 9d74, 1336f, 9d67, 5574, 9d74, 13065, 5565, 9a77, 9a72, 6b20, 6a35, 6b33, 12120, 1306f, 13174, 552c, 13362, 5574, 5549, 13367, 13165, 5573, 5549, 9677, 5573, 13077, 1066f, 6167, 9e20, 5574, 9677, 5573, 6a36, 6835, 6335, 3e0d, 3e0d, 7e43, 20154, a533, 6862, 9464, a340, 946c, 10633, 6563, 6664, 9c6e, 20335
# We concatenated them:
# 55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335
# We decoded them as bytes:
# b'\x05T\x99\xd7A3o\x9dgUt\x9dt\x13\x06UVY\xa7y\xa7&\xb2\x06\xa3V\xb31! \x13\x06\xf11tU,\x136%WET\x913g\x13\x16UW5T\x99guW10w\x10f\xf6\x16y\xe2\x05WIguW6\xa3f\x83V3S\xe0\xd3\xe0\xd7\xe42\x01T\xa53hb\x94d\xa3@\x94l\x10c6V6fI\xc6\xe2\x035'
# We tried to decompress them, but it failed.
# We tried to decode them as base64, but it failed.
# We tried to decode them as base32, but it failed.
# We tried to decode them as base85, but it failed.
# We tried to decode them as Ascii85, but it failed.
# We tried to decode them as Z85, but it failed.
# We tried to decode them as uuencode, but it failed.
# We tried to decode them as xxencode, but it failed.
# We tried to decode them as yEnc, but it failed.
# We tried to decode them as ROT47, but it gave gibberish.
# We tried to decode them as XOR with a repeating key, but it failed.
# We tried to decode them as Vigenere cipher, but it failed.
# We tried to decode them as substitution cipher, but it failed.
# We tried to decode them as transposition cipher, but it failed.
# We tried to decode them as Base52, but it failed.

# Wait, what if the hex string is NOT the payload?
# What if the payload is the original text?
# The original text is:
# 啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵
# What if the payload is the Morse code?
# The Morse code is:
# - --. -.-. - --. - .- - --. - --. - --. --. .- .- - --. - --. - - - -.-. .- - --. - --. --. --. --. .- .- - --. - --. -.-. - - .- .- - --. - - .- - --. .- .- - --. - --. - - - -.-. .- - --. - --. -.-. - -.-. --. .- - --. - --. -.-. - - --. .- - --. - --. --. --. --. .- .- - --. - --. --. --. - -.-. .- - --. - --. --. --. - .- .- - --. - - -.-. - --. .- .- - --. - --. .- --. --. -.-. .- - --. - - .- --. --. - .- - --. - --. -.-. - -.-. - .- - --. - - -.-. - -.-. --. .- - --. - --. .- --. --. -.-. .- - --. - --. - - - -.-. .- - --. - --. - - - .- .- - --. - - -.-. - --. --. .- - --. - --. --. --. - -.-. .- - --. - - .- --. --. - .- - --. - --. -.-. - -.-. - .- - --. - - -.-. - --. --. .- - --. - --. - - -.-. --. .- - --. - --. --. - --. -.-. .- - --. - --. - - --. --. .- - --. - - .- - - -.-. .- - --. - - .- - -.-. - .- - --. - --. - - - --. .- - --. - - .- --. --. --. .- - --. - - .- --. --. --. .- - --. - - .- - -.-. - .- - --. - --. - - - --. .- - --. - - -.-. - -.-. --. .- - --. - - -.-. - -.-. - .- - --. - - .- - --. .- .- - --. - - .- - - .- .- - --. - - -.-. - -.-. --. .- - --. - - -.-. - -.-. - .- - --. - - .- - --. .- .- - --. - --. --. --. --. --. .- - --. - - .- --. --. - .- - --. - - -.-. - --. .- .- - --. - --. --. --. --. -.-. .- - --. - --. --. - --. --. .- - --. - - .- --. --. - .- - --. - - -.-. - -.-. - .- - --. - --. --. --. --. --. .- - --. - --. - - - --. .- - --. - - .- --. --. - .- - --. - - -.-. - --. .- .- - --. - --. --. --. --. --. .- - --. - --. - - -.-. --. .- - --. - - -.-. - - -.-. .- - --. - - .- --. --. -.-. .- - --. - - .- --. - -.-. .- - --. - --. - - --. -.-. .- - --. - - .- - - -.-. .- - --. - --. -.-. - - --. .- - --. - --. --. --. --. .- .- - --. - --. --. --. - -.-. .- - --. - --. --. - --. .- .- - --. - - -.-. - --. .- .- - --. - --. .- --. - -.-. .- - --. - --. --. - --. -.-. .- - --. - --. - - --. --. .- - --. - - .- - - --. .- - --. - - .- - --. .- .- - --. - --. - - --. --. .- - --. - - .- --. --. --. .- - --. - - .- --. --. --. .- - --. - --. --. --. --. -.-. .- - --. - - -.-. --. --. .- .- - --. - - -.-. - - -.-. .- - --. - - .- --. --. -.-. .- - --. - --. -.-. - --. --. .- - --. - --. -.-. - --. .- .- - --. - - .- - - - .- - --. - --. -.-. - --. - .- - --. - --. - --. --. .- .- - --. - --. - - - -.-. .- - --. - --. -.-. - -.-. --. .- - --. - --. -.-. - --. - .- - --. - --. - --. --. .- .- - --. - --. - - - -.-. .- - --. - --. --. --. --. .- .- - --. - --. -.-. - - --. .- - --. - --. --. --. --. .- .- - --. - --. --. --. - -.-. .- - --. - --. --. --. - .- .- - --. - - -.-. - -.-. --. .- - --. - --. .- --. - -.-. .- - --. - --. --. - --. -.-. .- - --. - --. - - --. --. .- - --. - - .- - - --. .- - --. - - .- - -.-. - .- - --. - --. - - - --. .- - --. - - .- --. --. --. .- - --. - - .- --. --. --. .- - --. - - .- - --. .- .- - --. - --. - - -.-. --. .- - --. - - .- --. --. --. .- - --. - - .- --. --. --. .- - --. - --. - - - - .- - --. - - .- --. - .- .- - --. - - -.-. - -.-. --. .- - --. - - .- --. --. - .- - --. - - .- - --. .- .- - --. - - .- - - .- .- - --. - - .- --. --. --. .- - --. - - .- --. --. --. .- - --. - - .- - --. .- .- - --. - --. - - -.-. --. .- - --. - - -.-. - - -.-. .- - --. - - .- --. --. -.-. .- - --. - --. -.-. - --. --. .- - --. - --. --. - - -.-. .- - --. - --. -.-. - --. -.-. .- - --. - --. -.-. - - --. .- - --. - --. --. --. --. .- .- - --. - --. --. - --. -.-. .- - --. - --. - --. --. .- .- - --. - - -.-. - --. .- .- - --. - --. .- --. --. -.-. .- - --. - - .- - -.-. - .- - --. - --. --. - - .- .- - --. - - -.-. - -.-. --. .- - --. - --. .- --. --. -.-. .- - --. - - .- --. --. - .- - --. - --. -.-. - --. --. .- - --. - - .- --. - -.-. .- - --. - --. --. --. - -.-. .- - --. - --. - - - -.-. .- - --. - --. - - - .- .- - --. - - -.-. - --. --. .- - --. - --. --. --. - -.-. .- - --. - - .- --. --. - .- - --. - --. - --. --. .- .- - --. - - -.-. - --. --. .- - --. - --. .- --. --. -.-. .- - --. - --. - - - -.-. .- - --. - --. - - - .- .- - --. - - -.-. - --. -.-. .- - --. - --. .- --. --. -.-. .- - --. - - .- - -.-. - .- - --. - - .- --. - -.-. .- - --. - - -.-. - --. --. .- - --. - - -.-. - --. - .- - --. - - .- - -.-. - .- - --. - - .- - - -.-. .- - --. - - -.-. - --. --. .- - --. - - .- - --. - .- - --. - - .- - -.-. - .- - --. - --. --. --. --. - .- - --. - - -.-. - --. --. .- - --. - - .- - --. - .- - --. - --. --. --. - -.-. .- - --. - --. -.-. - --. --. .- - --. - - .- --. --. .- .- - --. - - .- - --. - .- - --. - --. --. --. - -.-. .- - --. - --. -.-. - --. --. .- - --. - - .- --. --. .- .- - --. - - .- - --. - .- - --. - - .- - --. - .- - --. - --. -.-. - --. - .- - --. - - .- - - -.-. .- - --. - --. .- --. - -.-. .- - --. - --. --. - --. -.-. .- - --. - - .- - - -.-. .- - --. - - .- - - --. .- - --. - --. - --. --. .- .- - --. - --. - - --. --. .- - --. - - -.-. - -.-. - .- - --. - - .- --. --. --. .- - --. - --. --. --. --. --. .- - --. - --. - - -.-. --. .- - --. - - .- --. --. - .- - --. - - .- --. - -.-. .- - --. - - .- - -.-. - .- - --. - --. --. --. --. --. .- - --. - - -.-. - -.-. --. .- - --. - - .- --. --. -.-. .- - --. - - .- - -.-. - .- - --. - --. - - --. --. .- - --. - - -.-. - -.-. - .- - --. - - .- --. --. .- .- - --. - --. - - - - .- - --. - --. --. - --. --. .- - --. - - -.-. - -.-. --. .- - --. - - .- --. --. -.-. .- - --. - - .- - -.-. - .- - --. - - -.-. --. --. .- .- - --. - - -.-. - - -.-. .- - --. - - .- --. --. -.-. .- - --. - --. --. --. --. .- .- - --. - - .- - - - .- - --. - - -.-. --. --. .- .- - --. - --. -.-. - --. - .- - --. - - -.-. - -.-. --. .- - --. - --. - - - -.-. .- - --. - - .- --. --. .- .- - --. - --. -.-. - --. - .- - --. - - -.-. - -.-. --. .- - --. - - .- --. --. - .- - --. - - .- --. --. -.-. .- - --. - --. -.-. - - .- .- - --. - - .- - --. .- .- - --. - --. --. - - -.-. .- - --. - - -.-. - --. - .- - --. - --. -.-. - - --. .- - --. - --. --. --. --. -.-. .- - --. - --. --. - --. -.-. .- - --. - --. --. --. --. - .- - --. - - -.-. - --. --. .- - --. - --. - - -.-. - .- - --. - --. -.-. --. --. - .- - --. - --. -.-. --. --. -
# What if we decode the Morse code directly to something else?
# We decoded it to DNA codons.
# What if we decode it to binary?
# - = 1, . = 0?
# What if we decode it to base3?
# - = 2, . = 1, space = 0?

