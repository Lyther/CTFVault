# The non-M string STILL has 'M' in it!
# Why? Because some codons are 'ATG', which translates to 'M'.
# But we already filtered out 'ATG' when we created the `codons` list!
# Let's filter out 'ATG' and then translate.
codon_table = {
    'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
    'GTA': 'V', 'GTC': 'V',
    'TCG': 'S', 'TCT': 'S',
    'TGA': '_', 'TGC': 'C', 'TGG': 'W', 'TGT': 'C',
    'TTA': 'L', 'TTC': 'F', 'TTG': 'L', 'TTT': 'F'
}

with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer1.txt", "r") as f:
    data = f.read().strip()

triplets = [data[i:i+3] for i in range(0, len(data), 3)]
codons = [t for t in triplets if t != "ATG"]

translated = "".join(codon_table.get(t, '?') for t in codons)
print("Translated:", translated)
print("Length:", len(translated))
print("Unique:", set(translated))

# 440 amino acids.
# 8 unique amino acids!
# C, G, F, W, L, _, S, V.
# 8 unique amino acids = 3 bits per amino acid!
# 440 * 3 = 1320 bits.
# 1320 / 8 = 165 bytes.

# Let's try to find a mapping from the 8 amino acids to 3-bit values (0-7)
# such that the resulting bits decode to a string containing "CIT{".
import itertools

aas = list(set(translated))

for perm in itertools.permutations(range(8)):
    mapping = dict(zip(aas, perm))
    
    bits = ""
    for aa in translated:
        bits += f"{mapping[aa]:03b}"
        
    res = bytearray()
    for i in range(0, len(bits), 8):
        if i + 8 <= len(bits):
            res.append(int(bits[i:i+8], 2))
            
    if b"CIT{" in res:
        print(f"Found CIT{{ with mapping {mapping}")
        print(res)
        break
