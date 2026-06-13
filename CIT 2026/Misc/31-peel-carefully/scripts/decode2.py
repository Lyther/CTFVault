import itertools

with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer1.txt", "r") as f:
    data = f.read().strip()

chars = ['A', 'C', 'G', 'T']
for perm in itertools.permutations([0, 1, 2, 3]):
    mapping = dict(zip(chars, perm))
    
    # Try pairs or 4-tuples?
    # 4-tuples:
    try:
        res = bytearray()
        for i in range(0, len(data), 4):
            if i + 3 >= len(data):
                break
            val = (mapping[data[i]] << 6) | (mapping[data[i+1]] << 4) | (mapping[data[i+2]] << 2) | mapping[data[i+3]]
            res.append(val)
        
        # Check if printable ascii
        if all(32 <= b <= 126 or b in (9, 10, 13) for b in res):
            print(f"Permutation {perm}: {res[:50]}")
    except Exception as e:
        pass

