import base64

with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer1.txt", "r") as f:
    data = f.read().strip()

triplets = [data[i:i+3] for i in range(0, len(data), 3)]

# Generate all 64 codons in alphabetical order
bases = ['A', 'C', 'G', 'T']
codons = [b1+b2+b3 for b1 in bases for b2 in bases for b3 in bases]

b64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
mapping = dict(zip(codons, b64_chars))

b64_str = "".join(mapping[t] for t in triplets)
print(b64_str[:100])

# Add padding if necessary
b64_str += "=" * ((4 - len(b64_str) % 4) % 4)

try:
    decoded = base64.b64decode(b64_str)
    print(decoded[:100])
except Exception as e:
    print(e)
