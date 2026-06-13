import base64

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

ordered_codons = [
    'GGA', 'GGC', 'GGG', 'GGT', 'GTA', 'GTC',
    'TCG', 'TCT', 'TGA', 'TGC', 'TGG', 'TGT',
    'TTA', 'TTC', 'TTG', 'TTT'
]

mapping = {c: (i - 6) % 16 for i, c in enumerate(ordered_codons)}

res = bytearray()
for c in chunks:
    if len(c) == 2:
        val = (mapping[c[0]] << 4) | mapping[c[1]]
        res.append(val)

print("Base64 string:", res.decode('ascii'))

try:
    decoded = base64.b64decode(res)
    print("Decoded:", decoded)
    with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer6.bin", "wb") as f:
        f.write(decoded)
except Exception as e:
    print("Error:", e)
