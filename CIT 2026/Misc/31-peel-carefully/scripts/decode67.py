text = "啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵"

# Let's convert the codepoints to a base-16 string and decode it as ASCII
# Wait, we already did that, it gave us the 213-character hex string.
# What if we convert the codepoints to a base-10 string?
dec_str = "".join(str(ord(c)) for c in text)
print("Dec string:", dec_str)

# What if we convert the codepoints to a base-8 string?
oct_str = "".join(oct(ord(c))[2:] for c in text)
print("Oct string:", oct_str)

# What if we convert the codepoints to a base-2 string?
bin_str = "".join(bin(ord(c))[2:] for c in text)
print("Bin string:", bin_str)

# What if we convert the codepoints to bytes in big-endian?
b = b"".join(ord(c).to_bytes(4, 'big') for c in text)
print("Bytes:", b[:20])

