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

aa_order = ['*', 'C', 'F', 'G', 'L', 'S', 'V', 'W']
aa_to_int = {aa: i for i, aa in enumerate(aa_order)}

b64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

res = ""
for c in chunks:
    if len(c) == 2:
        val = aa_to_int[codon_table[c[0]]] * 8 + aa_to_int[codon_table[c[1]]]
        res += b64_chars[val]

print(res[:100])
import base64
try:
    print(base64.b64decode(res + "==")[:100])
except Exception as e:
    print(e)
