# What if the Chinese characters are encoded with a custom encoding?
# What if we take the codepoints, and subtract a constant from each?
# What if we take the codepoints, and divide each by a constant?
# What if we take the codepoints, and take the modulo of each?
# We tried modulo 256 and modulo 128.
# Modulo 256 gave:
# Itogtteewr 53 ot,btIgesIwswog tws655\r\rCT3bd@l3cdn5
# Modulo 128 gave:
# Itogtteewr 53 ot,btIgesIwswog tws655\r\rCT3bd@l3cdn5
# Wait, let's look at this string again!
# "Itogtteewr 53 ot,btIgesIwswog tws655\r\rCT3bd@l3cdn5"
# This string is 50 characters long.
# And it ends with "CT3bd@l3cdn5".
# What if "CT3bd@l3cdn5" is the flag?
# The flag format is "CIT{...}".
# "CT3bd@l3cdn5" is 12 characters long.
# If it's a Vigenere cipher, and the plaintext is "CIT{...}", then the key is:
# C -> C (0)
# T -> I (-11)
# 3 -> T (27)
# b -> { (25)
# This is not a repeating key.

# What if it's a substitution cipher?
# We tried to break it with simulated annealing, and it failed.
# But wait! The simulated annealing script we used was trying to find English text!
# What if the text is NOT English?
# What if the text is a piece of code?
# What if the text is a URL?
# What if the text is a base64 string?
# If it's a base64 string, it would have characters from A-Z, a-z, 0-9, +, /.
# But our string has characters like ' ', ',', '@', '\r'.
# So it's not a base64 string.

# What if the string "Itogtteewr 53 ot,btIgesIwswog tws655\r\rCT3bd@l3cdn5" is just a hint?
# "Itogtteewr 53 ot,btIgesIwswog tws655"
# What if we apply ROT13 to it?
# "Vgbtggrrje 53 bg,ogVtrfVjfjbt gjf655\r\rPG3oq@y3pqa5"
# What if we apply ROT47 to it?
# "xE@8EE66HC db @E[3Ex86DxHDH@8 EHDeddr\r\r%b35o=b45?d"

# What if the string is encrypted with a custom cipher?
# Let's look at the characters again.
# I, t, o, g, t, t, e, e, w, r,  , 5, 3,  , o, t, ,, b, t, I, g, e, s, I, w, s, w, o, g,  , t, w, s, 6, 5, 5, \r, \r, C, T, 3, b, d, @, l, 3, c, d, n, 5
# Wait, "Itogtteewr" -> "I to g t t e e w r"?
# "I to get the e w r"?
# "53 ot,btIgesIwswog tws655" -> "53 ot, bt I ges I wswog tws 655"?
# "I guess I was wrong"?
# "I guess I was wrong" -> "I ges Iwswog"
# Let's check the mapping!
# I -> I
# g -> g
# e -> u
# s -> e
# I -> I
# w -> w
# s -> a
# w -> s
# o -> r
# g -> o
# This is a substitution cipher!
# Let's map it!
# I -> I
# g -> g
# e -> u
# s -> e
#   ->  
# I -> I
# w -> w
# s -> a
# w -> s
# o -> r
# g -> o
#   -> n
# t -> g
# w -> s
# s -> a
# 6 -> ?
# 5 -> ?
# 5 -> ?
# Wait, "Iwswog" -> "I was wrong"?
# I -> I
# w -> w
# s -> a
# w -> s
# o -> r
# g -> o
# n -> n
# g -> g
# So "Iwswog" -> "Iwasro"? No, "I was wrong" is 11 characters. "Iwswog" is 6 characters.
# "I was wrong" -> "I w a s w r o n g"?
# "Iwswog" -> "I w s w o g".
# If I=I, w=w, s=a, w=s, o=r, g=o. Then "Iwswog" -> "I w a s r o".
# This doesn't make sense.
