enc_key = bytes.fromhex("776b6a707c6a707c70767366717c7066607166777c68667a")
key = bytes(b ^ 0x23 for b in enc_key)

enc_flag = bytes.fromhex(
    "525d4f425c77752e784f6c306245703168735f227478316e21636125743b496c22622461757625357b",
)
flag = bytes(enc_flag[i] ^ key[i % len(key)] ^ 0x45 for i in range(len(enc_flag)))

print("CTF_SECRET_KEY=" + key.decode())
print(flag.decode())
