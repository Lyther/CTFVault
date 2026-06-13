import math
import random
import collections

text = "Itogtteewr 53 ot,btIgesIwswog tws655\r\rCT3bd@l3cdn5"
# Wait, this is 51 characters long.
# What if it's a substitution cipher?
# Let's try to break it.
# Wait, "CT3bd@l3cdn5" looks like a flag!
# "CIT{...}"
# If "CT3bd@l3cdn5" is the flag, then:
# C -> C
# T -> I
# 3 -> T
# b -> {
# d -> ?
# @ -> ?
# l -> ?
# 3 -> ?
# c -> ?
# d -> ?
# n -> ?
# 5 -> }
# Let's check this mapping!
# C -> C
# T -> I
# 3 -> T
# b -> {
# 5 -> }
# Let's apply this mapping to the rest of the text!
mapping = {'C': 'C', 'T': 'I', '3': 'T', 'b': '{', '5': '}'}
# What about the other characters?
# "Itogtteewr 53 ot,btIgesIwswog tws655"
# I -> ?
# t -> ?
# o -> ?
# g -> ?
# t -> ?
# t -> ?
# e -> ?
# e -> ?
# w -> ?
# r -> ?
#   -> ?
# 5 -> }
# 3 -> T
#   -> ?
# o -> ?
# t -> ?
# , -> ?
# b -> {
# t -> ?
# I -> ?
# g -> ?
# e -> ?
# s -> ?
# I -> ?
# w -> ?
# s -> ?
# w -> ?
# o -> ?
# g -> ?
#   -> ?
# t -> ?
# w -> ?
# s -> ?
# 6 -> ?
# 5 -> }
# 5 -> }
# Wait, "53" -> "}T".
# "655" -> "?}}".
# This doesn't look right.
# "tws655" -> "? ? ? ? } }".
# "53" -> "} T".
# If 5 is }, then 53 is }T.
# But "Itogtteewr }T ot,{tIgesIwswog tws6}}"
# This doesn't make sense.
# What if the mapping is NOT a substitution cipher?
# What if the string "Itogtteewr 53 ot,btIgesIwswog tws655\r\rCT3bd@l3cdn5" is encrypted with ROT47?
decoded = ""
for x in text.encode('ascii'):
    if 33 <= x <= 126:
        decoded += chr(33 + ((x - 33 + 47) % 94))
    else:
        decoded += chr(x)
print("ROT47:", decoded)

# What if the string is encrypted with ROT13?
import codecs
print("ROT13:", codecs.encode(text, 'rot_13'))

# What if the string is encrypted with Vigenere cipher?
# If "CT3bd@l3cdn5" is the flag, and it starts with "CIT{", then the key is:
# C -> C (shift 0)
# T -> I (shift -11)
# 3 -> T (shift ?)
# b -> { (shift ?)
# This is not a standard Vigenere cipher.
