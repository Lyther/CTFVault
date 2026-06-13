# Let's look at the base64 string again.
b64_str = "VUmddBM2+dZ1V0nXQTBlVWWad5pyayBqNWszEhIBMG8TF0VSwTNiVXRVSRM2cTFlVXNVSZZ3VXMTB3EGb2FnniBVdJZ3VXNqNmg1YzU+DT4NfkMgFUpTNoYpRko0CUbBBjNlY2ZknG4gM1"
# We decoded it and got:
# b'UI\x9dt\x136\xf9\xd6uWI\xd7A0eUe\x9aw\x9ark j5k3\x12\x12\x010o\x13\x17ER\xc13bUtUI\x136q1eUsUI\x96wUs\x13\x07q\x06oag\x9e Ut\x96wUsj6h5c5>\r>\r~C \x15JS6\x86)FJ4\tF\xc1\x063ecfd\x9cn 3'
# What if this is a piece of text that has been encrypted with a repeating key XOR?
# Let's try to break repeating key XOR on this!
b = b'UI\x9dt\x136\xf9\xd6uWI\xd7A0eUe\x9aw\x9ark j5k3\x12\x12\x010o\x13\x17ER\xc13bUtUI\x136q1eUsUI\x96wUs\x13\x07q\x06oag\x9e Ut\x96wUsj6h5c5>\r>\r~C \x15JS6\x86)FJ4\tF\xc1\x063ecfd\x9cn 3'

def bxor(s1, s2):
    return bytes(a ^ b for a, b in zip(s1, s2))

# We know the flag starts with "CIT{".
# Let's try to find the key by XORing with "CIT{".
for i in range(len(b) - 3):
    key = bxor(b[i:i+4], b"CIT{")
    if all(32 <= k <= 126 for k in key):
        # print(f"Key candidate at {i}: {key}")
        pass

# What if the key is just 1 byte?
for k in range(256):
    dec = bytes(x ^ k for x in b)
    if b"CIT{" in dec:
        print(f"Found CIT{{ with 1-byte key {k}")
        print(dec)

# What if the key is just 2 bytes?
for k1 in range(256):
    for k2 in range(256):
        key = bytes([k1, k2])
        dec = bytes(b[i] ^ key[i % 2] for i in range(len(b)))
        if b"CIT{" in dec:
            print(f"Found CIT{{ with 2-byte key {key}")
            print(dec)

