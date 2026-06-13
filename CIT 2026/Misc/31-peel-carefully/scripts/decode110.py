# The decoded bytes are exactly the same as the bytes we got from the hex string.
# b'UI\x9dt\x136\xf9\xd6uWI\xd7A0eUe\x9aw\x9ark j5k3\x12\x12\x010o\x13\x17ER\xc13bUtUI\x136q1eUsUI\x96wUs\x13\x07q\x06oag\x9e Ut\x96wUsj6h5c5>\r>\r~C \x15JS6\x86)FJ4\tF\xc1\x063ecfd\x9cn 3'
# This is because Base64 and Base32 are just different ways to encode the same binary data.

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
# Wait, 8 unique amino acids!
# 8 unique amino acids = 3 bits per amino acid!
# Let's map them to 3 bits!
# We can find the mapping by trying all 8! permutations.
import itertools

non_m = "CGCFWGCLL_CFCSCLWGWVWVFF__GLGCSFS_GCFCLFWWVLGCCSFWCSWCCWLFLSCLLGLGL"
# Wait, the non-M string I printed before was:
# CMGCMGCM_CMSCMGWMVFMGLMSFMGCMLFMVLMSFMSWMWLMSCMGLMSCMSFM_LMSFM_WMGFMGWMGFMGCMGFMGCMFLMVCMFCMGWM_FMVW
# Let's re-extract the non-M amino acids.
codon_table = {
    'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
    'GTA': 'V', 'GTC': 'V',
    'TCG': 'S', 'TCT': 'S',
    'TGA': '_', 'TGC': 'C', 'TGG': 'W', 'TGT': 'C',
    'TTA': 'L', 'TTC': 'F', 'TTG': 'L', 'TTT': 'F'
}

with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer1.txt", "r") as f:
    data = f.read().strip()

triplets = [data[i:i+3] for i in range(0, len(data), 3)]
translated = "".join(codon_table.get(t, '?') for t in triplets)

# The translated string is:
# C M C G M C F M W G M C L M L _ M C F M C S M C L M W G M W V M W V M F _ M _ G M L G M C S M F S M _ G M C F M C L M F W M W V M L G M C S M F W M C S M W C M C W M L F M L S M C L M L G M L G M L
# Let's extract the non-M amino acids.
non_m = ""
for i in range(0, len(translated), 2):
    non_m += translated[i]

print("Non-M:", non_m)
print("Length:", len(non_m))
print("Unique:", set(non_m))

# We have 8 unique amino acids: C, G, F, W, L, _, S, V.
# We can map them to 3 bits.
# 3 bits * 165 amino acids = 495 bits.
# 495 / 8 = 61.875 bytes. Not a multiple of 8.

# What if we map them to 4 bits?
# 4 bits * 165 = 660 bits = 82.5 bytes.

# What if we map the codons directly?
# We have 16 unique codons.
# 16 unique codons = 4 bits per codon.
# 440 codons * 4 bits = 1760 bits = 220 bytes.
# We already did this, and we found a mapping that gives a string ending in "CIT{99".
# The string is:
# b'7~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=LCIT{99'
# This string is 220 bytes long.
# And it ends with "CIT{99".
# What if the flag is "CIT{99..." and the rest of the flag is at the beginning of the string?
# "CIT{997~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=L}"
# Let's try to submit this flag!
