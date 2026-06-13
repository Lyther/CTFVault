# What if the string is "Itogtteewr 53 ot,btIgesIwswog tws655\r\rCT3bd@l3cdn5"?
# "Itogtteewr" -> "I thought we"
# "53" -> "re"
# "ot," -> "not,"
# "bt" -> "but"
# "I" -> "I"
# "ges" -> "gue"
# "Iwswog" -> "I was wrong"
# "tws655" -> "tws655"?
# Let's check the lengths!
# "Itogtteewr" (10 chars) -> "I thought " (10 chars)
# "53" (2 chars) -> "we" (2 chars)
# " ot," (4 chars) -> "re," (3 chars)? No, " ot," is 4 chars.
# Let's map it character by character!
text = "Itogtteewr 53 ot,btIgesIwswog tws655\r\rCT3bd@l3cdn5"
# I -> I
# t ->  
# o -> t
# g -> h
# t -> o
# t -> u
# e -> g
# e -> h
# w -> t
# r ->  
# 5 -> w
# 3 -> e
#   ->  
# o -> a
# t -> r
# , -> e
# b -> ,
# t ->  
# I -> b
# g -> u
# e -> t
# s ->  
# I -> I
# w ->  
# s -> g
# w -> u
# o -> e
# g -> s
#   -> s
# t ->  
# w -> I
# s ->  
# 6 -> w
# 5 -> a
# 5 -> s
# This doesn't make sense. 't' maps to ' ', 'o', 'u', 'r', ' ', ' '.

# What if the string is encrypted with a Vigenere cipher?
# Let's try to break Vigenere cipher on this string.
# We know the plaintext starts with "I thought we were not, but I guess I was wrong".
# Let's see if we can find the key!
def vigenere_key(ciphertext, plaintext):
    key = ""
    for c, p in zip(ciphertext, plaintext):
        if 32 <= ord(c) <= 126 and 32 <= ord(p) <= 126:
            k = (ord(c) - ord(p)) % 95 + 32
            key += chr(k)
        else:
            key += "?"
    return key

print(vigenere_key(text, "I thought we were not, but I guess I was wrong"))

