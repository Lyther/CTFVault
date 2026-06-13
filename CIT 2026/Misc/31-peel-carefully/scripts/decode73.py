with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer1.txt", "r") as f:
    data = f.read().strip()

triplets = [data[i:i+3] for i in range(0, len(data), 3)]
codons = [t for t in triplets if t != "ATG"]

# We know:
# TGG -> 4
# TGC -> 3
# GGT -> 9
# TTC -> 5
# TGT -> 7
# TCT -> B
# TTA -> 2
# TGA -> 6

# We also noticed:
# 43 49 54 7B 39 39 -> CIT{99
# So:
# 43 -> C -> TGG TGC
# 49 -> I -> TGG GGT
# 54 -> T -> TTC TGG
# 7B -> { -> TGT TCT
# 39 -> 9 -> TGC GGT
# 39 -> 9 -> TGC GGT

# Let's map all codons to hex digits based on their position in the hex string!
# We know the hex string is 440 characters long.
# Let's write a script to find the best mapping of the 16 codons to 16 hex digits (0-9, A-F)
# such that the resulting hex string decodes to printable ASCII.
import string
import itertools

# The 16 unique codons
unique_codons = list(set(codons))

# We already know some mappings:
known_mapping = {
    'TGG': '4',
    'TGC': '3',
    'GGT': '9',
    'TTC': '5',
    'TGT': '7',
    'TCT': 'B',
    'TTA': '2',
    'TGA': '6'
}

remaining_codons = [c for c in unique_codons if c not in known_mapping]
remaining_hex = [h for h in "0123456789ABCDEF" if h not in known_mapping.values()]

# We want to find a permutation of remaining_hex
# such that the decoded bytes are printable ASCII.
# Or even better, it's a known file format or English text.
# Let's just try all permutations.
import math

def score(b):
    # Score based on printable ASCII
    s = 0
    for x in b:
        if 32 <= x <= 126 or x in (9, 10, 13):
            s += 1
    return s

best_score = 0
best_mapping = None
best_bytes = None

for perm in itertools.permutations(remaining_hex):
    mapping = known_mapping.copy()
    for i, c in enumerate(remaining_codons):
        mapping[c] = perm[i]
        
    hex_str = "".join(mapping[c] for c in codons)
    try:
        b = bytes.fromhex(hex_str)
        s = score(b)
        if s > best_score:
            best_score = s
            best_mapping = mapping
            best_bytes = b
            print(f"New best score: {s}")
            print(b)
    except:
        pass

