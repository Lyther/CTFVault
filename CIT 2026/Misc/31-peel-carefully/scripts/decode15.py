import base64

with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer1.txt", "r") as f:
    data = f.read().strip()

triplets = [data[i:i+3] for i in range(0, len(data), 3)]
chunks = []
curr = []
for t in triplets:
    if t == "ATG":
        if curr: chunks.append(curr)
        curr = []
    else:
        curr.append(t)
if curr: chunks.append(curr)

mapping = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
b64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

b64_str = ""
for c in chunks:
    for t in c:
        val = (mapping[t[0]] << 4) | (mapping[t[1]] << 2) | mapping[t[2]]
        b64_str += b64_chars[val]

print("Base64:", b64_str[:100])
b64_str += "=" * ((4 - len(b64_str) % 4) % 4)

try:
    decoded = base64.b64decode(b64_str)
    print("Decoded:", decoded[:100])
    with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer5.bin", "wb") as f:
        f.write(decoded)
except Exception as e:
    print(e)
