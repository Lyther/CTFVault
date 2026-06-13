with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer1.txt", "r") as f:
    data = f.read().strip()

triplets = [data[i:i+3] for i in range(0, len(data), 3)]
codons = [t for t in triplets if t != "ATG"]

target_hex = "4349547B"

def find_pattern(pattern, seq):
    n = len(pattern)
    for i in range(len(seq) - n + 1):
        sub = seq[i:i+n]
        mapping = {}
        valid = True
        for j in range(n):
            if pattern[j] in mapping:
                if mapping[pattern[j]] != sub[j]:
                    valid = False
                    break
            else:
                if sub[j] in mapping.values():
                    valid = False
                    break
                mapping[pattern[j]] = sub[j]
        if valid:
            print(f"Found '{pattern}' at {i}: {sub}")
            print(f"Mapping: {mapping}")

find_pattern(target_hex, codons)
