import binascii

hex_str = "55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335"

# What if the hex string is a sequence of 5-bit values, and we decode it as Base32?
# We did that, it gave gibberish.

# What if we reverse the hex string, and then decode it as bytes?
rev_hex_str = hex_str[::-1]
try:
    b = bytes.fromhex(rev_hex_str + "0")
    print("Reversed:", b)
except:
    pass

# What if the hex string is a sequence of 7-bit values, and we decode it as ASCII?
# We did that, it gave gibberish.

# What if the hex string is a sequence of 6-bit values, and we decode it as Base64?
# We did that, it gave gibberish.

# What if the hex string is a sequence of 8-bit values, and we decode it as Base85?
# We checked, it has characters outside Base85.

# Let's look at the hex string again.
# 55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335
# What if it's a sequence of 4-bit values, and we decode it as Hex?
# It IS a sequence of 4-bit values!
# And we decoded it as Hex!
# And we got 107 bytes!
# And the 107 bytes are:
# b'\x05T\x99\xd7A3o\x9dgUt\x9dt\x13\x06UVY\xa7y\xa7&\xb2\x06\xa3V\xb31! \x13\x06\xf11tU,\x136%WET\x913g\x13\x16UW5T\x99guW10w\x10f\xf6\x16y\xe2\x05WIguW6\xa3f\x83V3S\xe0\xd3\xe0\xd7\xe42\x01T\xa53hb\x94d\xa3@\x94l\x10c6V6fI\xc6\xe2\x035'
# What if we XOR this with a repeating key?
# We tried that, it failed.

# What if we XOR this with the Morse code?
# What if we XOR this with the DNA codons?
# What if we XOR this with the Amino acids?
# What if we XOR this with the Base64 string?
# What if we XOR this with the Chinese characters?

# Let's look at the original text again.
# "One layer at a time, the message reveals itself... can you read it?"
# "It's all there, just buried."
# Layer 1: Morse code
# Layer 2: DNA
# Layer 3: Amino acids?
# Layer 4: Base64?
# Layer 5: Chinese characters?
# Layer 6: Hex string?
# Layer 7: ???

# Wait! The Chinese characters were:
# 啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵
# And we extracted their codepoints and concatenated them to get the hex string.
# But wait, what if the codepoints are NOT hex strings?
# What if the codepoints are just numbers, and we need to convert them to characters?
# We did that, it gave us the Chinese characters.

# What if the codepoints are just numbers, and we need to convert them to binary, and then decode the binary as ASCII?
# We did that, it gave gibberish.

# Let's look at the codepoints again.
codepoints = [21833, 40308, 78703, 40295, 21876, 40308, 77925, 21861, 39543, 39538, 27424, 27189, 27443, 74016, 77935, 78196, 21804, 78690, 21876, 21833, 78695, 78181, 21875, 21833, 38519, 21875, 77943, 67183, 24935, 40480, 21876, 38519, 21875, 27190, 26677, 25397, 15885, 15885, 32323, 131412, 42291, 26722, 37988, 41792, 37996, 67123, 25955, 26212, 40046, 131893]
# Notice that 21833 is 0x5549.
# 40308 is 0x9D74.
# 78703 is 0x1336F.
# 40295 is 0x9D67.
# 21876 is 0x5574.
# 40308 is 0x9D74.
# 77925 is 0x13065.
# 21861 is 0x5565.
# 39543 is 0x9A77.
# 39538 is 0x9A72.
# 27424 is 0x6B20.
# 27189 is 0x6A35.
# 27443 is 0x6B33.
# 74016 is 0x12120.
# 77935 is 0x1306F.
# 78196 is 0x13174.
# 21804 is 0x552C.
# 78690 is 0x13362.
# 21876 is 0x5574.
# 21833 is 0x5549.
# 78695 is 0x13367.
# 78181 is 0x13165.
# 21875 is 0x5573.
# 21833 is 0x5549.
# 38519 is 0x9677.
# 21875 is 0x5573.
# 77943 is 0x13077.
# 67183 is 0x1066F.
# 24935 is 0x6167.
# 40480 is 0x9E20.
# 21876 is 0x5574.
# 38519 is 0x9677.
# 21875 is 0x5573.
# 27190 is 0x6A36.
# 26677 is 0x6835.
# 25397 is 0x6335.
# 15885 is 0x3E0D.
# 15885 is 0x3E0D.
# 32323 is 0x7E43.
# 131412 is 0x20154.
# 42291 is 0xA533.
# 26722 is 0x6862.
# 37988 is 0x9464.
# 41792 is 0xA340.
# 37996 is 0x946C.
# 67123 is 0x10633.
# 25955 is 0x6563.
# 26212 is 0x6664.
# 40046 is 0x9C6E.
# 131893 is 0x20335.

# Wait! The hex string is:
# 5549 9d74 1336f 9d67 5574 9d74 13065 5565 9a77 9a72 6b20 6a35 6b33 12120 1306f 13174 552c 13362 5574 5549 13367 13165 5573 5549 9677 5573 13077 1066f 6167 9e20 5574 9677 5573 6a36 6835 6335 3e0d 3e0d 7e43 20154 a533 6862 9464 a340 946c 10633 6563 6664 9c6e 20335
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

# Wait! Look at the ASCII characters!
# UI, Ut, Ue, k , j5, k3, U,, Ut, UI, Us, UI, Us, ag, Ut, Us, j6, h5, c5, >\r, >\r, ~C, hb, ec, fd.
# Does this look like a flag? No.

