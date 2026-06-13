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

second_codons = set(c[1] for c in chunks if len(c) == 2)
first_codons = set(c[0] for c in chunks if len(c) == 2)
print("Second codons:", second_codons)
print("Intersection:", first_codons.intersection(second_codons))
