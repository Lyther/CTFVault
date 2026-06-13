s3 = b'7~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=LCIT{99'

# What if the string is just Base85 encoded, but using a custom alphabet?
# What if the string is just Base91 encoded, but using a custom alphabet?
# What if the string is just Base92 encoded, but using a custom alphabet?

# What if the string is encrypted with a Vigenere cipher?
# We tried that.

# What if the string is encrypted with a substitution cipher?
# We tried that.

# What if the string is encrypted with a transposition cipher?
# What if the string is just a URL?
# What if the string is a piece of code?

# Let's count the number of unique characters in s3.
print("Unique chars in s3:", len(set(s3)))
# 52 unique characters.

# What if the string is a piece of text that has been encoded with a custom base encoding?
# Base52 uses 52 characters.
# We tried to decode it as Base52, but it failed.

# What if the string is just the flag itself, but it's been obfuscated?
# "CIT{99..."
# If the flag is "CIT{99...", then the rest of the string is the flag!
# But the rest of the string is 214 characters long.
# And it looks like gibberish.

# What if the string is a piece of text that has been encoded with a custom encoding?
# What if we just print the string?
print(s3)

# What if we just submit the string as the flag?
# No.

# Let's think about the layers again.
# 1. Morse code -> DNA
# 2. DNA -> Hex string
# 3. Hex string -> Printable ASCII string ending in "CIT{99"
# 4. Printable ASCII string -> ???

# What if the printable ASCII string is a piece of text that has been compressed?
# What if the printable ASCII string is a piece of text that has been encrypted with AES?
# If it's encrypted with AES, it would be random bytes, not printable ASCII.

# What if the printable ASCII string is a piece of text that has been encoded with a custom base encoding?
# We checked, it's not Base52.

# What if the printable ASCII string is a piece of text that has been encoded with a custom encoding?
# What if we just decode the printable ASCII string as a sequence of 7-bit values?
# What if we just decode the printable ASCII string as a sequence of 6-bit values?
# What if we just decode the printable ASCII string as a sequence of 5-bit values?
