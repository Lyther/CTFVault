# Let's look at the Chinese characters again.
# "啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵"
# What if the Chinese characters are just a way to encode a Base64 string?
# The hex string is:
# 55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335
# What if we just decode the hex string as a base64 string?
# We tried, it failed.

# Let's try to decode the hex string as a Base32 string.
# We tried, it failed.

# Let's try to decode the hex string as a Base85 string.
# We tried, it failed.

# Let's try to decode the hex string as Ascii85.
# We tried, it failed.

# Let's try to decode the hex string as Z85.
# We tried, it failed.

# Let's try to decode the hex string as uuencode.
# We tried, it failed.

# Let's try to decode the hex string as xxencode.
# We tried, it failed.

# Let's try to decode the hex string as yEnc.
# We tried, it failed.

# Let's try to decode the hex string as ROT47.
# We tried, it gave gibberish.

# Let's try to decode the hex string as a sequence of 7-bit values.
# We tried, it gave gibberish.

# Let's try to decode the hex string as a sequence of 6-bit values.
# We tried, it gave gibberish.

# Let's try to decode the hex string as a sequence of 5-bit values.
# We tried, it gave gibberish.

# Let's try to decode the hex string as a sequence of 4-bit values.
# We tried, it gave gibberish.

# What if the original text is NOT the payload?
# What if the payload is the Morse code?
# We decoded the Morse code to DNA, then to Amino Acids.
# We found that the Amino Acids are:
# C M C G M C F M W G M C L M L _ M C F M C S M C L M W G M W V M W V M F _ M _ G M L G M C S M F S M _ G M C F M C L M F W M W V M L G M C S M F W M C S M W C M C W M L F M L S M C L M L G M L G M L
# Every second amino acid is 'M'.
# The non-M amino acids are:
# C G C F W G C L L _ C F C S C L W G W V W V F _ _ G L G C S F S _ G C F C L F W W V L G C S F W C S W C C W L F L S C L L G L G L
# What if we map the non-M amino acids to base64?
# There are 8 unique amino acids: C, G, F, W, L, _, S, V.
# We mapped them to 3 bits, but it didn't work.

# What if we map the non-M amino acids to 4 bits?
# We mapped them to 4 bits, but it didn't work.

# What if we map the codons directly?
# We have 16 unique codons.
# 16 unique codons = 4 bits per codon.
# 440 codons * 4 bits = 1760 bits = 220 bytes.
# We found 3 permutations that give a printable ASCII string ending in "CIT{99".
# The 3 strings are:
# s1 = b'7\x7fuO2&u1>OM@Vl);QlurTM);TqCt%+~((+~Q[&"Q[&H)VLD)[H~)VHqU,-s%>OMFVmCt.&t((L_U,46*7\x7fu17\x7fuO>OM@QmCt.+~((&q((z Q)&"((&qU,4E3>OC\x7fVl+BQl)4-MurTM)\x7fTlurSl+-TW+%T\'+IT\'M4/\'M4/\'\'7%mC%.\x7ft[(Hq)-+HQ,+t[/zDQ,+_U,O*_7Qu/7Q),2&EW>LCIT{99'
# s2 = b'7~uN2&u1?NM@Vl);QlurTM);TqCt%+\x7f((+\x7fQ[&"Q[&H)VLD)[H\x7f)VHqU,-s%?NMFVmCt/&t((L^U,46*7~u17~uN?NM@QmCt/+\x7f((&q((z Q)&"((&qU,4E3?NC~Vl+BQl)4-MurTM)~TlurSl+-TW+%T\'+IT\'M4.\'M4.\'\'7%mC%/~t[(Hq)-+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW?LCIT{99'
# s3 = b'7~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=LCIT{99'
# Notice that these strings are 220 characters long.
# And they end in "CIT{99".
# What if the flag is "CIT{99...}" and it wraps around to the beginning of the string?
# Let's try to submit "CIT{997~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=L}"
# No, that's too long and looks like gibberish.

# What if the string is base85 encoded, but using a custom alphabet?
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
