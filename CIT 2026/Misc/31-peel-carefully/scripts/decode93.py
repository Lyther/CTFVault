import string
import collections
import random
import math

s3 = b'7~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=LCIT{99'

# We know the last 6 characters are "CIT{99".
# This means:
# 'C' -> 'C'
# 'I' -> 'I'
# 'T' -> 'T'
# '{' -> '{'
# '9' -> '9'
# '9' -> '9'
# So these mappings are fixed!
# Wait, if 'C' maps to 'C', 'I' maps to 'I', 'T' maps to 'T', '{' maps to '{', '9' maps to '9',
# maybe the whole string is already decrypted?
# But the rest of the string is gibberish!
# How can part of the string be gibberish and part of it be plaintext?
# Maybe the string is encrypted with a Vigenere cipher?
# Let's try to find the key for Vigenere cipher.
# If the ciphertext ends in "CIT{99", and the plaintext ends in "CIT{99", then the key for those characters is 0.
# If the key is 0, maybe the key is "A" (or 0)?
# But the rest of the string is gibberish.

# What if the string is base64 encoded, but the last characters are just literal "CIT{99" appended to it?
# No, we derived the whole string from the codons!
# The codons translated to the hex string, and the hex string ended in "4349547B3939", which is "CIT{99".
# This means the hex string IS the plaintext!
# But the hex string is 440 characters long, which is 220 bytes.
# And the 220 bytes look like gibberish, EXCEPT for the last 6 bytes!
# Why would the last 6 bytes be "CIT{99" and the rest be gibberish?
# Maybe the rest of the string is ALSO hex encoded?
# No, we already decoded it from hex to bytes.
# The bytes are:
# b'7~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=LCIT{99'
# This is 220 bytes.
# What if this is a Base85 string?
# We checked, it has characters outside Base85.

# What if it's a Base91 string?
# Base91 alphabet: A-Z, a-z, 0-9, !#$%&()*+,./:;<=>?@[]^_`{|}~"
# It does not use -, ', \.
# But our string has -, ', \.
# Let's check if our string has '\'.
print("Has \\:", b'\\' in s3)
# It has '\'!
# Let's check if it has '-'.
print("Has -:", b'-' in s3)
# It has '-'!
# Let's check if it has "'".
print("Has ':", b"'" in s3)
# It has "'"!

# What encoding uses these characters?
# Ascii85 uses !-u and z.
# Z85 uses 0-9, a-z, A-Z, ., -, :, +, =, ^, !, /, *, ?, &, <, >, (, ), [, ], {, }, @, %, $, #.
# It does NOT use ~, |, }, \, ', ", `, _.
# Our string has ~, }, |, \, ', ", ^, _.
# So it's NOT Z85.

# What if it's uuencode?
# uuencode uses 32-95 (space to _).
# Our string has characters up to ~ (126).
# So it's NOT uuencode.

# What if it's xxencode?
# xxencode uses +-z.
# Our string has characters outside this range.

# What if it's yEnc?
# yEnc uses A-Z, a-z, 0-9, ., -, +, =.
# Our string has characters outside this range.

# What if it's a custom base encoding?
# The string has 52 unique characters.
# The characters are:
print("Unique chars:", sorted(list(set(s3))))

