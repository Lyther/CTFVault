# Wait!
# The Chinese characters are:
# 啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵
# And their hex codepoints are:
# 5549, 9d74, 1336f, 9d67, 5574, 9d74, 13065, 5565, 9a77, 9a72, 6b20, 6a35, 6b33, 12120, 1306f, 13174, 552c, 13362, 5574, 5549, 13367, 13165, 5573, 5549, 9677, 5573, 13077, 1066f, 6167, 9e20, 5574, 9677, 5573, 6a36, 6835, 6335, 3e0d, 3e0d, 7e43, 20154, a533, 6862, 9464, a340, 946c, 10633, 6563, 6664, 9c6e, 20335
# Notice that 5549 is "UI".
# 9d74 is not ASCII.
# 1336f is not ASCII.
# 9d67 is not ASCII.
# 5574 is "Ut".
# 9d74 is not ASCII.
# 13065 is not ASCII.
# 5565 is "Ue".
# 9a77 is not ASCII.
# 9a72 is not ASCII.
# 6b20 is "k ".
# 6a35 is "j5".
# 6b33 is "k3".
# 12120 is not ASCII.
# 1306f is not ASCII.
# 13174 is not ASCII.
# 552c is "U,".
# 13362 is not ASCII.
# 5574 is "Ut".
# 5549 is "UI".
# 13367 is not ASCII.
# 13165 is not ASCII.
# 5573 is "Us".
# 5549 is "UI".
# 9677 is not ASCII.
# 5573 is "Us".
# 13077 is not ASCII.
# 1066f is not ASCII.
# 6167 is "ag".
# 9e20 is not ASCII.
# 5574 is "Ut".
# 9677 is not ASCII.
# 5573 is "Us".
# 6a36 is "j6".
# 6835 is "h5".
# 6335 is "c5".
# 3e0d is ">\r".
# 3e0d is ">\r".
# 7e43 is "~C".
# 20154 is not ASCII.
# a533 is not ASCII.
# 6862 is "hb".
# 9464 is not ASCII.
# a340 is not ASCII.
# 946c is not ASCII.
# 10633 is not ASCII.
# 6563 is "ec".
# 6664 is "fd".
# 9c6e is not ASCII.
# 20335 is not ASCII.

# What if the hex string is just a piece of text that has been encoded with a custom encoding?
# What if we just decode the hex string as a sequence of 7-bit values?
# What if we just decode the hex string as a sequence of 6-bit values?
# What if we just decode the hex string as a sequence of 5-bit values?

# Let's count the number of unique characters in the hex string.
print("Unique chars in hex string:", len(set("55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335")))
# 16 unique characters.

# What if the hex string is a piece of text that has been compressed?
# What if the hex string is a piece of text that has been encrypted with AES?
# If it's encrypted with AES, it would be random bytes, not printable ASCII.

# What if the hex string is a piece of text that has been encoded with a custom base encoding?
# We checked, it's not Base52.

# What if the hex string is a piece of text that has been encoded with a custom encoding?
# What if we just print the hex string?
print("55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335")

