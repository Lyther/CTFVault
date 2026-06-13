codon_table = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
    'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W',
}

with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer1.txt", "r") as f:
    data = f.read().strip()

triplets = [data[i:i+3] for i in range(0, len(data), 3)]
translated = "".join(codon_table.get(t, '?') for t in triplets)

# Extract every amino acid that is NOT 'M'
# Wait, let's just take every other amino acid, starting from index 0.
# The sequence is C M C G M C F M W G M C L M L _ M ...
# So the non-M amino acids are at even indices.
non_m = translated[0::2]
print("Non-M amino acids:", non_m[:100])

# What if we map these amino acids to base64?
# There are 9 unique amino acids: C, G, F, W, L, _, S, V.
# Let's see the unique amino acids.
print("Unique:", set(non_m))

# Wait, the amino acids are C, G, F, W, L, _, S, V.
# That's 8 unique amino acids! (Wait, 8 unique amino acids).
# Let's count them:
import collections
print("Counts:", collections.Counter(non_m))

# 8 unique amino acids means we can map them to 3-bit values!
# 3 bits per amino acid.
# How many amino acids?
print("Length:", len(non_m))
# 329 amino acids.
# 329 * 3 = 987 bits.
# 987 / 8 = 123.375 bytes. Not a multiple of 8.

# Wait, what if we map the codons themselves?
# There are 16 unique codons (excluding ATG).
# 16 unique codons = 4 bits per codon!
# Let's list the 16 unique codons again.
codons = [t for t in triplets if t != "ATG"]
print("Unique codons:", len(set(codons)))
