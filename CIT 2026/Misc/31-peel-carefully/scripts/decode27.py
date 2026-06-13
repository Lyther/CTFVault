import base64

mapping = {
    'GGA': 0, 'GGC': 1, 'GGG': 2, 'GGT': 3, 'GTA': 4, 'GTC': 5,
    'TCG': 6, 'TCT': 7, 'TGA': 8, 'TGC': 9, 'TGG': 10, 'TGT': 11,
    'TTA': 12, 'TTC': 13, 'TTG': 14, 'TTT': 15
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

res = bytearray()
for c in chunks:
    if len(c) == 2:
        val = (mapping[c[0]] << 4) | mapping[c[1]]
        res.append(val ^ 0xFF)

print("XORed string:", res.decode('ascii', errors='replace'))

try:
    decoded = base64.a85decode(res)
    print("Ascii85 decoded:", decoded)
except Exception as e:
    print("Ascii85 error:", e)

try:
    decoded = base64.b85decode(res)
    print("Base85 decoded:", decoded)
except Exception as e:
    print("Base85 error:", e)
