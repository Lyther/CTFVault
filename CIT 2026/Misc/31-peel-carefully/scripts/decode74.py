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
remaining_hex = [h for h in "0123456789ABCDEF" if h not in known_mapping.values()]

for perm in itertools.permutations(remaining_hex):
    mapping = known_mapping.copy()
    for i, c in enumerate(remaining_codons):
        mapping[c] = perm[i]
        
    hex_str = "".join(mapping[c] for c in codons)
    try:
        b = bytes.fromhex(hex_str)
        # Check if it's base64 encoded
        import base64
        try:
            dec = base64.b64decode(b)
            if b"CIT{" in dec:
                print("Found CIT{ in base64 decoded bytes!")
                print(dec)
        except:
            pass
        
        # Check if it's base32 encoded
        try:
            dec = base64.b32decode(b)
            if b"CIT{" in dec:
                print("Found CIT{ in base32 decoded bytes!")
                print(dec)
        except:
            pass
            
        # Check if it's a known file format
        if b.startswith(b"\x89PNG") or b.startswith(b"PK\x03\x04") or b.startswith(b"BZh") or b.startswith(b"\x1f\x8b") or b.startswith(b"7z\xbc\xaf\x27\x1c"):
            print("Found file format!")
            print(b[:20])
            
        # Check if it's ASCII text
        if all(32 <= x <= 126 or x in (9, 10, 13) for x in b):
            print("Found pure ASCII text!")
            print(b)
    except:
        pass
