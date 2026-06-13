import collections

mapping = {
    'GGA': '(', 'GGC': ')', 'GGG': '*', 'GGT': '+', 'GTA': ',', 'GTC': '-',
    'TCG': '6', 'TCT': '7', 'TGA': '8', 'TGC': '9', 'TGG': ':', 'TGT': ';',
    'TTA': '<', 'TTC': '=', 'TTG': '>', 'TTT': '?'
}

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

text = ""
for c in chunks:
    for t in c:
        text += mapping[t]

print(text[:100])
with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer3_ascii.txt", "w") as f:
    f.write(text)
