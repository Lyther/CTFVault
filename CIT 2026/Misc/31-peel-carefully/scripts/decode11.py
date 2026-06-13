import collections

with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer1.txt", "r") as f:
    data = f.read().strip()

triplets = [data[i:i+3] for i in range(0, len(data), 3)]
chunks = []
curr = []
for t in triplets:
    if t == "ATG":
        if curr: chunks.append(curr)
        curr = []
    else:
        curr.append(t)
if curr: chunks.append(curr)

pairs = [tuple(c) for c in chunks if len(c) == 2]

# Let's map pairs to characters A-Z, a-z
unique_pairs = list(set(pairs))
chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
pair_to_char = {p: chars[i] for i, p in enumerate(unique_pairs)}
text = "".join(pair_to_char[p] for p in pairs)

with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer3_subst.txt", "w") as f:
    f.write(text)

print(text[:100])
