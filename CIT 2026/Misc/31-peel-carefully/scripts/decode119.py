# Let's reconsider the original text:
text = "啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵"
# The codepoints are:
# 21833, 40308, 78703, 40295, 21876, 40308, 77925, 21861, 39543, 39538, 27424, 27189, 27443, 74016, 77935, 78196, 21804, 78690, 21876, 21833, 78695, 78181, 21875, 21833, 38519, 21875, 77943, 67183, 24935, 40480, 21876, 38519, 21875, 27190, 26677, 25397, 15885, 15885, 32323, 131412, 42291, 26722, 37988, 41792, 37996, 67123, 25955, 26212, 40046, 131893
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

# Wait! The hex string we got from the codepoints is EXACTLY the same as the hex string we got from the codons!
# Let's check!
hex_str_codons = "377?754?3226753?3?4?4?4?566?293B5?6?7572544?293B547?4374252B7?20202B7?5?5B26225?5B264029564?44295B407?2956407?552?2?73253?4?4?46566?43742?267420204?5?552?34362?377?753?377?754?3?4?4?4?5?6?43742?2B7?2020267?20207?2?5?2926222020267?552?3445333?4?437?566?2B425?6?29342?4?7572544?297?546?7572536?2B2?54572B2554272B4954274?342?274?342?272737256?43252?7?745B20407?292?2B405?2?2B745B2?7?445?2?2B5?552?4?2?5?375?752?375?292?322645573?4?4349547B3939"
hex_str_codepoints = "55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335"

# Are they the same?
# No!
# hex_str_codons has 440 characters.
# hex_str_codepoints has 213 characters.
# Oh, I see!
# I got confused!
# The hex string we got from the codons ended in "4349547B3939", which is "CIT{99".
# The hex string we got from the codepoints ended in "20335".
# So they are completely different!

# What is the relationship between the codons and the codepoints?
# The codons are:
# TGG TGC GGT TTC TGT TCT TTA TGA ...
# The codepoints are:
# 5549, 9D74, 1336F, 9D67, 5574, 9D74, 13065, 5565 ...

# Wait! The original text is the Chinese characters!
# And the Morse code is inside the challenge.txt file!
# I completely forgot about the challenge.txt file!
# The challenge.txt file contains the Morse code!
# Let's look at the challenge.txt file again.
