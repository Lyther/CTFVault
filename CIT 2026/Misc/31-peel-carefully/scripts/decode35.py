import string

with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer1.txt", "r") as f:
    data = f.read().strip()

triplets = [data[i:i+3] for i in range(0, len(data), 3)]
codons = [t for t in triplets if t != "ATG"]

mapping = {
    'TGG': '4',
    'TGC': '3',
    'GGT': '9',
    'TTC': '5',
    'TGT': '7',
    'TCT': 'B',
    'TTA': '2',
    'TGA': '6'
}

hex_str = ""
for c in codons:
    hex_str += mapping.get(c, "?")

print(hex_str)

# Find remaining mappings
# We can look at the bigrams of hex digits and see what makes sense.
# For example, `2?` is `20` (space). `TTA GGG` is very common, so `GGG` is `0`.
# `TTA GGT` is `29` ('). Wait, `GGT` is `9`. So `29` is `)`.
# `TTA TCT` is `2B` (+).
# `TTA GGC` is `2?`.
# Let's see the most common pairs.
import collections
pairs = [hex_str[i:i+2] for i in range(0, len(hex_str), 2)]
print(collections.Counter(pairs).most_common(20))
