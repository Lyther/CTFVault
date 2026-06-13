with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer1.txt", "r") as f:
    data = f.read().strip()

triplets = [data[i:i+3] for i in range(0, len(data), 3)]
codons = [t for t in triplets if t != "ATG"]

mapping = {
    'TGG': '4', 'TGC': '3', 'GGT': '9', 'TTC': '5', 'TGT': '7', 'TCT': 'B',
    'TTA': '2', 'TGA': '6', 'GGG': '0', 'TCG': 'C', 'GGA': '0', 'TTG': 'A',
    'TTT': 'F', 'GTC': 'D', 'GGC': 'E', 'GTA': '8'
}

hex_str = ""
for c in codons:
    hex_str += mapping.get(c, "?")

print(hex_str)

# Let's decode the hex string
try:
    print(bytes.fromhex(hex_str))
except Exception as e:
    print(e)
