# Let's look at the codepoints again.
codepoints = [21833, 40308, 78703, 40295, 21876, 40308, 77925, 21861, 39543, 39538, 27424, 27189, 27443, 74016, 77935, 78196, 21804, 78690, 21876, 21833, 78695, 78181, 21875, 21833, 38519, 21875, 77943, 67183, 24935, 40480, 21876, 38519, 21875, 27190, 26677, 25397, 15885, 15885, 32323, 131412, 42291, 26722, 37988, 41792, 37996, 67123, 25955, 26212, 40046, 131893]

# What if we take the codepoints modulo 256, and then decode them as ASCII?
# We did that, and we got:
# Itogtteewr 53 ot,btIgesIwswog tws655\r\rCT3bd@l3cdn5
# Wait, look at the last 12 characters:
# "CT3bd@l3cdn5"
# What if the flag is "CIT{...}"?
# The first character is C.
# The second character is T.
# The third character is 3.
# The fourth character is b.
# The fifth character is d.
# The sixth character is @.
# The seventh character is l.
# The eighth character is 3.
# The ninth character is c.
# The tenth character is d.
# The eleventh character is n.
# The twelfth character is 5.
# What if this is a Vigenere cipher?
# C -> C (0)
# T -> I (-11)
# 3 -> T (27)
# b -> { (25)
# This is not a Vigenere cipher.

# What if the codepoints are just a sequence of numbers, and we need to decode them with a custom encoding?
# What if we take the codepoints modulo 256, and then XOR them with a repeating key?
# We checked, it's not XORed.
# What if we take the codepoints modulo 256, and then decode them as Base64?
# We checked, it's not Base64.

# Wait, what if the codepoints are just a sequence of numbers, and we need to subtract a constant from each codepoint?
# What if we subtract 21833 from each codepoint?
# What if we divide each codepoint by a constant?
# What if we take the modulo of each codepoint?
# We tried modulo 256 and modulo 128.
# Modulo 256 gave:
# Itogtteewr 53 ot,btIgesIwswog tws655\r\rCT3bd@l3cdn5
# Modulo 128 gave:
# Itogtteewr 53 ot,btIgesIwswog tws655\r\rCT3bd@l3cdn5
# Wait, what if the modulo is 127?
# What if the modulo is 126?
# Let's try different modulos!
for m in range(2, 257):
    dec = "".join(chr(c % m) if 32 <= c % m <= 126 else "." for c in codepoints)
    if "CIT{" in dec:
        print(f"Modulo {m}: {dec}")
