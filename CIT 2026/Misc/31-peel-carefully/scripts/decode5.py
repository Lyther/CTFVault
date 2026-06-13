codons = ['GGA', 'GGC', 'GGG', 'GGT', 'GTA', 'GTC', 'TCG', 'TCT', 'TGA', 'TGC', 'TGG', 'TGT', 'TTA', 'TTC', 'TTG', 'TTT']
mapping = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
for c in codons:
    val = (mapping[c[0]] << 4) | (mapping[c[1]] << 2) | mapping[c[2]]
    print(f"{c}: {val:02x}")
