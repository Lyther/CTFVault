import itertools

codon_table = {
    'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
    'GTA': 'V', 'GTC': 'V',
    'TCG': 'S', 'TCT': 'S',
    'TGA': '*', 'TGC': 'C', 'TGG': 'W', 'TGT': 'C',
    'TTA': 'L', 'TTC': 'F', 'TTG': 'L', 'TTT': 'F'
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

aa_seq = []
for c in chunks:
    if len(c) == 2:
        aa_seq.append(codon_table[c[0]])
        aa_seq.append(codon_table[c[1]])

aas = list(set(aa_seq))

for perm in itertools.permutations(range(8)):
    mapping = dict(zip(aas, perm))
    
    bits = ""
    for aa in aa_seq:
        bits += f"{mapping[aa]:03b}"
        
    res = bytearray()
    for i in range(0, len(bits), 8):
        if i + 8 <= len(bits):
            res.append(int(bits[i:i+8], 2))
            
    if b"CIT{" in res:
        print(f"Found CIT{{ with mapping {mapping}")
        print(res)
        break
    
    # Also check if it's a known file format
    if res.startswith(b"\x89PNG") or res.startswith(b"PK\x03\x04") or res.startswith(b"BZh"):
        print(f"Found file format with mapping {mapping}")
        print(res[:20])
        with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer3.bin", "wb") as f:
            f.write(res)
        break
