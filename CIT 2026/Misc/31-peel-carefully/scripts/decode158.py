# Let's reconsider the string "Itogtteewr 53 ot,btIgesIwswog tws655\r\rCT3bd@l3cdn5"
# We got this string by taking the codepoints modulo 256.
# Why did this give us a string that looks like English?
# "I to g t t e e w r"
# "53 ot, bt I ges I wswog tws 655"
# "\r\rCT3bd@l3cdn5"
# It's NOT English. It's just a coincidence that some characters look like English.
# "I", "t", "o", "g", "e", "w", "r", "s" are all common English letters.
# But "Itogtteewr" is not a word.

# What if the string is encrypted with a substitution cipher?
# We tried to break it, and the best we got was:
# "I thought we were not, but I guess I was wrong"
# Wait!
# "I thought we were not, but I guess I was wrong"
# Let's check the lengths!
# "I" (1) -> "I" (1)
# "t" (1) -> " " (1)
# "o" (1) -> "t" (1)
# "g" (1) -> "h" (1)
# "t" (1) -> "o" (1)
# "t" (1) -> "u" (1)
# "e" (1) -> "g" (1)
# "e" (1) -> "h" (1)
# "w" (1) -> "t" (1)
# "r" (1) -> " " (1)
# " " (1) -> "w" (1)
# "5" (1) -> "e" (1)
# "3" (1) -> " " (1)
# " " (1) -> "w" (1)
# "o" (1) -> "e" (1)
# "t" (1) -> "r" (1)
# "," (1) -> "e" (1)
# "b" (1) -> " " (1)
# "t" (1) -> "n" (1)
# "I" (1) -> "o" (1)
# "g" (1) -> "t" (1)
# "e" (1) -> "," (1)
# "s" (1) -> " " (1)
# "I" (1) -> "b" (1)
# "w" (1) -> "u" (1)
# "s" (1) -> "t" (1)
# "w" (1) -> " " (1)
# "o" (1) -> "I" (1)
# "g" (1) -> " " (1)
# " " (1) -> "g" (1)
# "t" (1) -> "u" (1)
# "w" (1) -> "e" (1)
# "s" (1) -> "s" (1)
# "6" (1) -> "s" (1)
# "5" (1) -> " " (1)
# "5" (1) -> "I" (1)
# "\r" (1) -> " " (1)
# "\r" (1) -> "w" (1)
# "C" (1) -> "a" (1)
# "T" (1) -> "s" (1)
# "3" (1) -> " " (1)
# "b" (1) -> "w" (1)
# "d" (1) -> "r" (1)
# "@" (1) -> "o" (1)
# "l" (1) -> "n" (1)
# "3" (1) -> "g" (1)
# "c" (1) -> "." (1)
# "d" (1) -> "." (1)
# "n" (1) -> "." (1)
# "5" (1) -> "." (1)
# This is NOT a substitution cipher! 't' maps to ' ', 'o', 'u', 'r', 'n', 'u'.

# What if the string is encrypted with a Vigenere cipher?
# We tried to find the key, and it was gibberish.

# What if the string is NOT "I thought we were not, but I guess I was wrong"?
# What if the string is just gibberish?
# Yes, it's just gibberish.

# Let's go back to the hex string.
# 55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335
# What if we just decode the hex string as a base64 string?
# We tried, it failed.
