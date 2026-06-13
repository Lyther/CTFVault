with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer6.bin", "rb") as f:
    data = f.read()

try:
    print(data.decode('utf-8'))
except Exception as e:
    print(e)
