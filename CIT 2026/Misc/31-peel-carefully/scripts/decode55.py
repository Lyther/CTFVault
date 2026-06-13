text = "啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵"
# What if we encode this to utf-8?
utf8_data = text.encode('utf-8')
print("UTF-8 length:", len(utf8_data))
print(utf8_data)

# What if we encode this to utf-16?
utf16_data = text.encode('utf-16le')
print("UTF-16 length:", len(utf16_data))
print(utf16_data)

# Let's look at the UTF-16 bytes
for i in range(0, len(utf16_data), 2):
    val = utf16_data[i] | (utf16_data[i+1] << 8)
    print(f"{val:04x}", end=" ")
print()
