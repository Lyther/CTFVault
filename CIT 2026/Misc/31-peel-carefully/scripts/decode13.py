import base64

codon_table = {
    'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
    'GTA': 'V', 'GTC': 'V',
    'TCG': 'S', 'TCT': 'S',
    'TGA': '*', 'TGC': 'C', 'TGG': 'W', 'TGT': 'C',
    'TTA': 'L', 'TTC': 'F', 'TTG': 'L', 'TTT': 'F'
}

aa_list = sorted(list(set(codon_table.values())))
aa_to_int = {aa: i for i, aa in enumerate(aa_list)}

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

b64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
b64_str = ""
for c in chunks:
    if len(c) == 2:
        aa1 = codon_table[c[0]]
        aa2 = codon_table[c[1]]
        val = aa_to_int[aa1] * 8 + aa_to_int[aa2]
        b64_str += b64_chars[val]

print("Base64:", b64_str[:100])
b64_str += "=" * ((4 - len(b64_str) % 4) % 4)

try:
    decoded = base64.b64decode(b64_str)
    print("Decoded:", decoded[:100])
    with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer4.bin", "wb") as f:
        f.write(decoded)
except Exception as e:
    print(e)
