with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/challenge.txt", "r") as f:
    data = f.read().strip()

words = data.split(' ')
bin_str = ""
for w in words:
    for c in w:
        if c == '-':
            bin_str += '1'
        elif c == '.':
            bin_str += '0'

print("Length:", len(bin_str))
res = bytearray()
for i in range(0, len(bin_str), 8):
    if i + 8 <= len(bin_str):
        res.append(int(bin_str[i:i+8], 2))

print(res[:50])
if b"CIT{" in res:
    print("Found CIT{")
