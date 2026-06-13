# What if the Chinese characters are a piece of code?
# What if the Chinese characters are a URL?
# What if the Chinese characters are a file path?
# What if the Chinese characters are a piece of text that has been compressed?
# What if the Chinese characters are a piece of text that has been encrypted with AES?
# If it's encrypted with AES, it would be random bytes, not printable ASCII.

# Let's count the number of Chinese characters again.
text = "啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵"
print(len(text))
# 51 characters.

# Wait, what if the Chinese characters are just a translation of the flag?
# 啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵
# Could this be "CIT{..."?
# Let's look at the first 4 characters: 啉 鵴 𓍯 鵧
# If this is "CIT{", then:
# 啉 -> C
# 鵴 -> I
# 𓍯 -> T
# 鵧 -> {
# Let's check if there are any other '啉' in the text.
print("Indices of 啉:", [i for i, c in enumerate(text) if c == '啉'])
# Indices are 0, 19, 23.
# If 啉 is C, then there are Cs at indices 0, 19, 23.
# Let's check if there are any other '鵴' in the text.
print("Indices of 鵴:", [i for i, c in enumerate(text) if c == '鵴'])
# Indices are 1, 5.
# If 鵴 is I, then there are Is at indices 1, 5.
# Let's check if there are any other '𓍯' in the text.
print("Indices of 𓍯:", [i for i, c in enumerate(text) if c == '𓍯'])
# Indices are 2.
# If 𓍯 is T, then there is a T at index 2.
# Let's check if there are any other '鵧' in the text.
print("Indices of 鵧:", [i for i, c in enumerate(text) if c == '鵧'])
# Indices are 3.
# If 鵧 is {, then there is a { at index 3.

# What about the last character?
# 𠌵
# Is it '}'?
# Let's check if there are any other '𠌵' in the text.
print("Indices of 𠌵:", [i for i, c in enumerate(text) if c == '𠌵'])
# Indices are 50.
# If 𠌵 is }, then there is a } at index 50.

# This looks like a substitution cipher!
# Let's try to break this substitution cipher!
