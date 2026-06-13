text = "啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵"

# Let's see the hex of the codepoints
codepoints = [ord(c) for c in text]
print("Codepoints:", codepoints)

# What if we XOR them with something?
# Or maybe they are just base 10 numbers?
# 21833, 40308, 78703, 40295, 21876, 40308, 77925, 21861, 39543, 39538, 27424, 27189, 27443, 74016, 77935, 78196, 21796, 78690, 21876, 21833, 78695, 78181, 21875, 21833, 38519, 21875, 77943, 67183, 24935, 40480, 21876, 38519, 21875, 27190, 26677, 25397, 15885, 15885, 32323, 131412, 42291, 26722, 37988, 41792, 37996, 67123, 25955, 26212, 40046, 131893

# Let's check the differences
diffs = [codepoints[i] - codepoints[i-1] for i in range(1, len(codepoints))]
print("Diffs:", diffs)

# What if we just take them modulo 256?
mod256 = [c % 256 for c in codepoints]
print("Mod 256:", "".join(chr(c) if 32 <= c <= 126 else "." for c in mod256))

# What if we take them modulo 128?
mod128 = [c % 128 for c in codepoints]
print("Mod 128:", "".join(chr(c) if 32 <= c <= 126 else "." for c in mod128))

