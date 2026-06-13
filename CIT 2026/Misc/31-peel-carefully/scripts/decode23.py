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

mapping = {
    'LG': ' ',
    'WG': 'e',
    'FS': 't',
    'CL': 'h',
    'CW': 'a',
    'CF': 'i',
    'CS': 's',
    'WV': 'n',
    'LS': 'o',
    'CC': 'r',
    'CG': 'd',
    'L*': 'l',
    'FW': 'u',
    'LF': 'm',
    '*G': 'c',
    'WC': 'g',
    'F*': 'y',
    'LL': 'p',
    'LV': 'f',
    'LC': 'v',
    'FF': 'b',
    '*V': 'k',
    'FG': 'w',
    'FC': 'x',
    'WW': 'j',
    'WF': 'q',
    'W*': 'z',
    'C*': '1',
    'WL': '2'
}

# Let's try to print it with known mappings, and ? for unknown
decoded = ""
for p in aa_pairs:
    if p in mapping:
        decoded += mapping[p]
    else:
        decoded += f"[{p}]"

print(decoded)
