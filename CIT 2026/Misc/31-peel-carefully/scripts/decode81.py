import itertools

with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer1.txt", "r") as f:
    data = f.read().strip()

triplets = [data[i:i+3] for i in range(0, len(data), 3)]
codons = [t for t in triplets if t != "ATG"]

known_mapping = {
    'TGG': '4',
    'TGC': '3',
    'GGT': '9',
    'TTC': '5',
    'TGT': '7',
    'TCT': 'B',
    'TTA': '2',
    'TGA': '6'
}

unique_codons = list(set(codons))
remaining_codons = [c for c in unique_codons if c not in known_mapping]
remaining_hex = [h for h in "0123456789abcdef" if h.upper() not in known_mapping.values() and h not in known_mapping.values()]

def score(b):
    s = 0
    for x in b:
        if 32 <= x <= 126 or x in (9, 10, 13):
            s += 1
    return s

best_score = 0
best_mapping = None
best_bytes = None

for perm in itertools.permutations(remaining_hex):
    mapping = known_mapping.copy()
    for i, c in enumerate(remaining_codons):
        mapping[c] = perm[i]
        
    hex_str = "".join(mapping[c] for c in codons)
    try:
        b = bytes.fromhex(hex_str)
        s = score(b)
        if s > best_score:
            best_score = s
            best_mapping = mapping
            best_bytes = b
            print(f"New best score: {s}")
            print(b)
            if b"CIT{" in b:
                print("FOUND CIT{")
    except:
        pass

