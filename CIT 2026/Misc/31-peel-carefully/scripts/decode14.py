import collections

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

mapping = {
    'GGA': 0, 'GGC': 1, 'GGG': 2, 'GGT': 3, 'GTA': 4, 'GTC': 5,
    'TCG': 6, 'TCT': 7, 'TGA': 8, 'TGC': 9, 'TGG': 10, 'TGT': 11,
    'TTA': 12, 'TTC': 13, 'TTG': 14, 'TTT': 15
}

res = bytearray()
for c in chunks:
    if len(c) == 2:
        val = (mapping[c[0]] << 4) | mapping[c[1]]
        res.append(val)

# Let's print the hex values of the first 20 bytes
print(" ".join(f"{b:02x}" for b in res[:20]))
