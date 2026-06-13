import itertools

with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer1.txt", "r") as f:
    data = f.read().strip()

chars = ['A', 'C', 'G', 'T']

for perm in itertools.permutations([0, 1, 2, 3]):
    mapping = dict(zip(chars, perm))
    
    res = bytearray()
    for i in range(0, len(data), 4):
        if i + 3 < len(data):
            val = (mapping[data[i]] << 6) | (mapping[data[i+1]] << 4) | (mapping[data[i+2]] << 2) | mapping[data[i+3]]
            res.append(val)
            
    if b"CIT{" in res:
        print(f"Found CIT{{ with mapping {mapping}")
        print(res)
        break
        
    # Check if it's base64 encoded
    import base64
    try:
        dec = base64.b64decode(res + b"===")
        if b"CIT{" in dec:
            print(f"Found CIT{{ in base64 with mapping {mapping}")
            break
    except:
        pass

