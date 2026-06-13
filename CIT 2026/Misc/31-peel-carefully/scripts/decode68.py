hex_str = "55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335"

# What if we pair the hex digits differently?
# 55 49 9d 74 13 36 f9 d6 75 ...
# What if we interpret them as a base32 string?
# Base32 uses A-Z, 2-7.
# The hex string contains 0-9, a-f.
# What if we interpret them as a base16 string, but it's actually just a string of hex digits?
# Yes, it's a string of hex digits.
# What if we decode it as a hex string, and then XOR it with a repeating key?
# We tried that.

# Let's look at the original characters again.
text = "啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵"

# What if the text is just a translation of some other characters?
# The challenge description: "One layer at a time, the message reveals itself... can you read it?"
# "It's all there, just buried."
# Layer 1: Morse code
# Layer 2: DNA codons
# Layer 3: ?
# Layer 4: ?
# Layer 5: ?
# Layer 6: ?

# Let's review Layer 2:
# The DNA codons were mapped to amino acids.
# But wait! DNA to Amino Acid translation is a known steganography technique!
# We did that in decode4.py:
# CCMCGMCFMWGMCLML_MCFMCSMCLMWGMWVMWVMF_M_GMLGMCSMFSM_GMCFMCLMFWMWVMLGMCSMFWMCSMWCMCWMLFMLSMCLMLGMLGML
# Wait, this is the amino acid sequence!
# What if we use the 1-letter amino acid codes?
# C = Cysteine, M = Methionine, G = Glycine, F = Phenylalanine, W = Tryptophan, L = Leucine, _ = Stop, S = Serine, V = Valine.
# Let's look at the 1-letter codes we got:
# C M C G M C F M W G M C L M L _ M C F M C S M C L M W G M W V M W V M F _ M _ G M L G M C S M F S M _ G M C F M C L M F W M W V M L G M C S M F W M C S M W C M C W M L F M L S M C L M L G M L G M L
# Notice that EVERY SECOND amino acid is 'M' (Methionine)!
# C M C G M C F M W G M C L M L _ M C F M C S M C L M W G M W V M W V M F _ M _ G M L G M C S M F S M _ G M C F M C L M F W M W V M L G M C S M F W M C S M W C M C W M L F M L S M C L M L G M L G M L
# Let's extract the other amino acids!
