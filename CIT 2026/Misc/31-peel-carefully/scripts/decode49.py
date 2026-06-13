with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer6.bin", "rb") as f:
    data = f.read()

if b"CIT{" in data:
    print("Found CIT{ in layer6.bin!")
else:
    print("Not found.")

# Let's search for XORed CIT{
for i in range(256):
    target = bytes([0x43 ^ i, 0x49 ^ i, 0x54 ^ i, 0x7B ^ i])
    if target in data:
        print(f"Found XORed CIT{{ with key {i:02x}")
