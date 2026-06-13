# The script above didn't find "CIT{".
# What if we map the 16 unique codons to 4-bit values?
# We did that, and we found 3 permutations that give a printable ASCII string ending in "CIT{99".
# The string is 220 bytes long.
# We checked if it's Base64, Base32, Ascii85, Base91, Base92, Z85, uuencode, xxencode, yEnc, Base58, Base62.
# We checked if it's a substitution cipher, a Vigenere cipher, a repeating key XOR.
# We checked if it's compressed with zlib, bz2, lzma.
# None of these worked.

# Let's look at the 3 strings again:
s1 = b'7\x7fuO2&u1>OM@Vl);QlurTM);TqCt%+~((+~Q[&"Q[&H)VLD)[H~)VHqU,-s%>OMFVmCt.&t((L_U,46*7\x7fu17\x7fuO>OM@QmCt.+~((&q((z Q)&"((&qU,4E3>OC\x7fVl+BQl)4-MurTM)\x7fTlurSl+-TW+%T\'+IT\'M4/\'M4/\'\'7%mC%.\x7ft[(Hq)-+HQ,+t[/zDQ,+_U,O*_7Qu/7Q),2&EW>LCIT{99'
s2 = b'7~uN2&u1?NM@Vl);QlurTM);TqCt%+\x7f((+\x7fQ[&"Q[&H)VLD)[H\x7f)VHqU,-s%?NMFVmCt/&t((L^U,46*7~u17~uN?NM@QmCt/+\x7f((&q((z Q)&"((&qU,4E3?NC~Vl+BQl)4-MurTM)~TlurSl+-TW+%T\'+IT\'M4.\'M4.\'\'7%mC%/~t[(Hq)-+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW?LCIT{99'
s3 = b'7~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=LCIT{99'

# Wait, what if the string is ROT47 encoded?
# We did that, it gave gibberish.

# What if the string is a URL?
# What if the string is a piece of code?
# What if the string is a piece of text that has been encoded with a custom base encoding?
# What if the string is a piece of text that has been encoded with a custom encoding?
# Let's count the number of unique characters in s3.
print("Unique chars in s3:", len(set(s3)))
# 52 unique characters.
# What if the string is a piece of text that has been encoded with a substitution cipher, but the alphabet is NOT A-Z?
# We tried to break the substitution cipher, but it failed.

# Let's look at the original text again.
# "One layer at a time, the message reveals itself... can you read it?"
# "It's all there, just buried."
# Layer 1: Morse code
# Layer 2: DNA
# Layer 3: Amino acids?
# We found that the amino acids are:
# C M C G M C F M W G M C L M L _ M C F M C S M C L M W G M W V M W V M F _ M _ G M L G M C S M F S M _ G M C F M C L M F W M W V M L G M C S M F W M C S M W C M C W M L F M L S M C L M L G M L G M L
# Every second amino acid is 'M'.
# What if 'M' is a delimiter?
# If 'M' is a delimiter, then the string is:
# C, C G, C F, W G, C L, L _, C F, C S, C L, W G, W V, W V, F _, _ G, L G, C S, F S, _ G, C F, C L, F W, W V, L G, C S, F W, C S, W C, C W, L F, L S, C L, L G, L G, L
# Notice that most of the chunks are 2 amino acids long!
# C
# C G
# C F
# W G
# C L
# L _
# C F
# C S
# C L
# W G
# W V
# W V
# F _
# _ G
# L G
# C S
# F S
# _ G
# C F
# C L
# F W
# W V
# L G
# C S
# F W
# C S
# W C
# C W
# L F
# L S
# C L
# L G
# L G
# L
# Wait! Why are there single amino acids at the beginning and end?
# C at the beginning.
# L at the end.
# What if the 'M' is NOT a delimiter, but part of the message?
# What if the amino acids are just a string of characters?
# We mapped the amino acids to base64, but it didn't work.

# What if the DNA codons are NOT translated to amino acids?
# What if the DNA codons are mapped to 2-bit values?
# A=00, C=01, G=10, T=11.
# Let's try that!
