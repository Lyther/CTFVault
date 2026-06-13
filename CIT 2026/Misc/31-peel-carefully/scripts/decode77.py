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

for perm in itertools.permutations(remaining_hex):
    mapping = known_mapping.copy()
    for i, c in enumerate(remaining_codons):
        mapping[c] = perm[i]
        
    hex_str = "".join(mapping[c] for c in codons)
    try:
        b = bytes.fromhex(hex_str)
        # Decode ROT47
        decoded = ""
        for x in b:
            if 33 <= x <= 126:
                decoded += chr(33 + ((x - 33 + 47) % 94))
            else:
                decoded += chr(x)
                
        # Check if it's base64 encoded
        try:
            dec = base64.b64decode(decoded + "===")
            if b"CIT{" in dec:
                print("Found CIT{ in base64 decoded ROT47 bytes!")
                print(dec)
                break
        except:
            pass
            
        try:
            dec = base64.b32decode(decoded + "======")
            if b"CIT{" in dec:
                print("Found CIT{ in base32 decoded ROT47 bytes!")
                print(dec)
                break
        except:
            pass
    except:
        pass
