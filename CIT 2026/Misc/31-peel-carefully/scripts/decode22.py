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

unique_pairs = list(set(aa_pairs))
chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
pair_to_char = {p: chars[i] for i, p in enumerate(unique_pairs)}
text = "".join(pair_to_char[p] for p in aa_pairs)

print("Text length:", len(text))
print("Unique chars:", len(set(text)))

freqs = {c: text.count(c) for c in set(text)}
ic = sum(f * (f - 1) for f in freqs.values()) / (len(text) * (len(text) - 1))
print(f"IC: {ic}")

print(text)
