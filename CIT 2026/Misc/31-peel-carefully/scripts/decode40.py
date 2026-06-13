import collections

with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer1.txt", "r") as f:
    data = f.read().strip()

triplets = [data[i:i+3] for i in range(0, len(data), 3)]
codons = [t for t in triplets if t != "ATG"]

mapping = {
    'TTC': '5',
    'TGA': '1',
    'TGG': '3',
    'GGG': '0',
    'TGT': '6',
    'TCG': 'C'
}

# We can guess the rest of the mapping by looking at the hex string.
# A base64 string contains characters A-Z, a-z, 0-9, +, /.
# In hex, these are 41-5A, 61-7A, 30-39, 2B, 2F.
# So the first digit of each byte must be 2, 3, 4, 5, 6, 7.
# We know 3=TGG, 5=TTC, 6=TGT.
# The remaining first digits are 2, 4, 7.
# Let's see the first digits in the codons.
first_digits = set(codons[i] for i in range(0, len(codons), 2))
print("First digits:", first_digits)
for c in first_digits:
    if c not in mapping:
        print(f"Unknown first digit: {c}")

