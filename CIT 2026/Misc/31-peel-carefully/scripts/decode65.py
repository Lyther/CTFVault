import base64
text = "啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵"
# Look at the hex of the codepoints again:
# 5549 9d74 1336f 9d67 5574 9d74 13065 5565 9a77 9a72 6b20 6a35 6b33 12120 1306f 13174 552c 13362 5574 5549 13367 13165 5573 5549 9677 5573 13077 1066f 6167 9e20 5574 9677 5573 6a36 6835 6335 3e0d 3e0d 7e43 20154 a533 6862 9464 a340 946c 10633 6563 6664 9c6e 20335
# What if this is a Base64 string?
# 55 49 9d 74 13 36 f9 d6 75 57 49 d7 41 30 65 55 65 9a 77 9a 72 6b 20 6a 35 6b 33 12 12 01 30 6f 13 17 45 52 c1 33 62 55 74 55 49 13 36 71 31 65 55 73 55 49 96 77 55 73 13 07 71 06 6f 61 67 9e 20 55 74 96 77 55 73 6a 36 68 35 63 35 3e 0d 3e 0d 7e 43 20 15 4a 53 36 86 29 46 4a 34 09 46 c1 06 33 65 63 66 64 9c 6e 20 33 5
# No, it's a hex string.
# What if it's base58?
import base58
try:
    print(base58.b58decode(text))
except Exception as e:
    print(e)
