with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer1.txt", "r") as f:
    data = f.read().strip()

mapping = {'A': 0, 'C': 1, 'G': 2, 'T': 3}

res = bytearray()
for i in range(0, len(data), 4):
    if i + 3 < len(data):
        val = (mapping[data[i]] << 6) | (mapping[data[i+1]] << 4) | (mapping[data[i+2]] << 2) | mapping[data[i+3]]
        res.append(val)

print(res[:100])
if b"CIT{" in res:
    print("Found CIT{")
