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
    'TCT': 'B'
}

# Let's see the frequencies of the remaining codons
for c in set(codons):
    if c not in mapping:
        print(f"{c}: {codons.count(c)}")

# We can try to guess the remaining mapping by ensuring the hex string decodes to printable ASCII
# A hex string of length 440 decodes to 220 bytes.
# The bytes should be printable ASCII.
# The first digit of a printable ASCII byte is usually 2, 3, 4, 5, 6, 7.
# The second digit can be anything.
# Let's see the first digits (even indices in codons).
first_digits = set(codons[i] for i in range(0, len(codons), 2))
print("First digits:", first_digits)

# Let's print the known hex string
hex_str = ""
for c in codons:
    hex_str += mapping.get(c, "?")

print(hex_str)
