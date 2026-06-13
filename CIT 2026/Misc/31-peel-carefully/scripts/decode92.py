s3 = b'7~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=LCIT{99'

# Let's try to XOR it with a repeating key.
# We know the flag starts with "CIT{".
# Where is the flag?
# It's at the end of the string! "CIT{99"
# Wait, if the flag is at the end of the string, maybe the string is NOT XORed?
# Because "CIT{" is already in plaintext!
# If it's already in plaintext, the XOR key must be 0!
# But the rest of the string is gibberish.
# This means the string is NOT XORed.

# Wait, what if the flag is "CIT{99..." and the rest of the string is the rest of the flag?
# But the rest of the string is 214 characters long.
# And it's gibberish.
# What if the string is base85 encoded?
# We checked, it has characters outside base85.

# What if the string is Ascii85 encoded?
# Ascii85 uses characters from '!' (33) to 'u' (117) and 'z' (122).
# Our string has '~' (126), '}' (125), '|' (124).
# So it's NOT Ascii85.

# What if the string is a custom base encoding?
# Let's count the number of unique characters in s3.
print("Unique chars:", len(set(s3)))
# We did that, it was 52 unique characters.
# 52 unique characters!
# Wait! 52 unique characters!
# A-Z and a-z are exactly 52 characters!
# But our string has characters like '~', '&', '=', '@', ';', '(', ')', '%', '[', ']', '"', '*', '+', '-', '.', '/', ':', '<', '>', '?', '\\', '^', '_', '`', '{', '|', '}'.
# Wait! If it has 52 unique characters, it could be a simple substitution cipher!
# We did that in decode9.py!
# We mapped the 52 unique pairs of codons to 52 characters.
# And we got a string of length 220.
# Then we tried to break the substitution cipher in decode32.py.
# The best result we got was:
# MSATCSRTALLYIERHISTOLERORPDWNTEENTHHCBHHCAEYAQEHATEYARVEG WTALZYXPDBCDEEAKVED!W MSR MSATALLHXPDBNTEECREESGHECBEECRVEDJ TAPMYIN"HIEDGLSTOLEMOISTFINGOFNWOUNAOULDEULDEUU WXPWBMDHEAREGNAHENDHESQHENKVEAWK HSE HEETCJFTAPAORMM
# This looks like English!
# "TALLY IER HISTOLE" -> "TALLY HER PISTOL"?
# "MOIST FING OF NWOUN AOULDE ULDEUU" -> "MOIST FING OF NOWUN WOULD WOULD"?
# Let's look closer at the substitution cipher.
