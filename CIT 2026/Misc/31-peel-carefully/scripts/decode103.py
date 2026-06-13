# The decoded ascii85 string is 176 bytes long.
# Let's look at the decoded bytes for shift 20:
b = b"\x83W\x85oN!S\xd3\xcf@+6\x91\x9d\x11\xc5\xdfVk\xfa\x11\x89\x87Q5\xe4\xd6\xca\xd6p\xf4\x08\xf3\xa1=\xcb\xc6\x0b<\xd75\xf3Q\x8a\xe1+\x92x\x97\xc1UE\x0bP\x80\x92\x19\xe47\xc6\xe1,*\xe4\x83W{\xd38\\\xe5q\xcf?\x9f2\x1a\x13W\x96T\xec\xd9\xff,H\xd5\xceBV\xe7\xd9\xe1,/\xe8\x97\xbf\xf5\xa6\x01\x1f\x0e'X\x8f\xce\xfc\x15K\xbf\xf1\xdc\xe9\xcd\\\x01\x1c\xf75^@O\x85\xbdKa\x12g\xa8\x12\xa9Q\xdd\xc7a\xa8\xe8p\xb0\xf3\xb3\xf3\xd5j\xe9W\x1e]\xab(\x87\xad\xa1.)\xe1/\x04\xe6\x85,\x05\x1e\xd4\x9d\x189\xb0\xf7\xd7\x0b\xbdJ#V"

# Does it contain CIT{?
print("Contains CIT{:", b"CIT{" in b)

# What if the shift is different?
# Ascii85 uses 5 characters to encode 4 bytes.
# The original string was 220 characters.
# 220 / 5 = 44. 44 * 4 = 176 bytes.
# If the flag is "CIT{99...", it would be in the decoded bytes!
# But the decoded bytes don't contain "CIT{".
# Wait, "CIT{99" was at the end of the original string BEFORE Ascii85 decoding!
# If "CIT{99" is at the end of the original string, then the original string is NOT Ascii85 encoded!
# Because if it was Ascii85 encoded, the plaintext would be inside the decoded bytes, not the encoded string!
# The fact that "CIT{99" is in the string itself means the string IS the plaintext!
# But the string is gibberish except for the last 6 characters.
# How can a string be gibberish except for the last 6 characters?
# Maybe the string is encrypted with a stream cipher, and the key ran out?
# Or maybe the string is encrypted with a block cipher, and the last block was not encrypted?
# Or maybe the string is a polyalphabetic cipher, and the key is "CIT{"?
# Let's check if the string is XORed with a repeating key.
# We tried that.
