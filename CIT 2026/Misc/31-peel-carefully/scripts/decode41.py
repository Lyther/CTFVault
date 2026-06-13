with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer1.txt", "r") as f:
    data = f.read().strip()

triplets = [data[i:i+3] for i in range(0, len(data), 3)]
codons = [t for t in triplets if t != "ATG"]

for i in range(0, len(codons), 2):
    if codons[i] == 'TGA':
        print(f"TGA at {i}: {codons[i]} {codons[i+1]}")
