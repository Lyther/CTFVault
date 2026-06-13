with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer3_ascii.txt", "r") as f:
    text = f.read().strip()

decoded = ""
for b in text:
    c = ord(b)
    if 33 <= c <= 126:
        decoded += chr(33 + ((c - 33 + 47) % 94))
    else:
        decoded += b

print("ROT47:", decoded[:100])
