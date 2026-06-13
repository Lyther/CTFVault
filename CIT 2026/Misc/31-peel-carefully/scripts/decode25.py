import collections

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

aa_pairs = []
for c in chunks:
    if len(c) == 2:
        aa_pairs.append(codon_table[c[0]] + codon_table[c[1]])

def find_pattern(pattern):
    n = len(pattern)
    for i in range(len(aa_pairs) - n + 1):
        sub = aa_pairs[i:i+n]
        mapping = {}
        valid = True
        for j in range(n):
            if pattern[j] in mapping:
                if mapping[pattern[j]] != sub[j]:
                    valid = False
                    break
            else:
                if sub[j] in mapping.values():
                    valid = False
                    break
                mapping[pattern[j]] = sub[j]
        if valid:
            print(f"Found '{pattern}' at {i}: {sub}")
            print(f"Mapping: {mapping}")

find_pattern("the flag is cit{")
find_pattern("flag is cit{")
find_pattern(" cit{")
