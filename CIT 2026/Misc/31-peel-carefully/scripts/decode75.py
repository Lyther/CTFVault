import itertools
import base64

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
remaining_hex = [h for h in "0123456789ABCDEF" if h not in known_mapping.values()]

def try_decode(b):
    try:
        dec = base64.b64decode(b)
        if b"CIT{" in dec:
            return dec
    except:
        pass
    try:
        dec = base64.b32decode(b)
        if b"CIT{" in dec:
            return dec
    except:
        pass
    return None

for perm in itertools.permutations(remaining_hex):
    mapping = known_mapping.copy()
    for i, c in enumerate(remaining_codons):
        mapping[c] = perm[i]
        
    hex_str = "".join(mapping[c] for c in codons)
    try:
        b = bytes.fromhex(hex_str)
        # What if it's XORed?
        # We know it ends with "CIT{99"
        # Wait, if it ends with CIT{99, it's already ASCII!
        if b"CIT{" in b:
            print("Found CIT{ in raw bytes!")
            print(b)
            break
    except:
        pass
