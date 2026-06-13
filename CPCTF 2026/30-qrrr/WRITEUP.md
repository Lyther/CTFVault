# QRRRRRRRRRR (Misc, quarantineee)

**Flag:** `CPCTF{z3r0_l3ngth_h1dd3n_d4t4}`

## Observation

Feed the PNG to every common QR decoder (zbar / pyzbar, OpenCV, qreader) — **all refuse**. Format info, finder patterns, timing and alignment all look valid though, so the raw bit layout isn't broken.

- Version 3 (29×29), EC level **Q**, mask **3** (top-right format info matches exactly).
- Sample the 29×29 grid, apply mask 3, snake-read → 70 codewords.
- De-interleave into two RS(35, 17) blocks and run RS decode → **zero errors** in both blocks. So the data codewords are intact; the encoder's RS/mask/placement are all fine.

Combined data stream (block1 ‖ block2, 34 bytes):

```text
40 04 35 04 35 44 67 b7 a3 37 23 05 f6 c3 36 e6 77
46 85 f6 83 16 46 43 36 e5 f6 43 47 43 47 d0 ec 11
```

## The bug — hinted by the flag

Parsing as a standard QR byte-mode stream:

- bits `[0:4]` = `0100` → **mode = byte**.
- bits `[4:12]` = `00000000` → **char count = 0** ← this is the lie.

A compliant decoder sees `cc=0`, emits `""` and stops. But the encoder didn't truncate — it wrote the full flag right after the (zeroed) char-count indicator. Skip the field and byte-align from bit 4:

```python
bits = ''.join(f'{b:08b}' for b in data)
payload = bits[4:]  # strip the 4-bit mode; ignore the fake cc
out = bytes(int(payload[i:i+8], 2) for i in range(0, (len(payload)//8)*8, 8))
```

→ `\x00CPCTF{z3r0_l3ngth_h1dd3n_d4t4}\x0e\xc1`

The leading `\x00` is the char-count indicator's 8 bits of zero; the trailing bytes are padding fragments. In between is the flag.

## Full solver

```python
import numpy as np
from PIL import Image
from reedsolo import RSCodec

arr = np.array(Image.open("qr.png").convert("L"))
N = 29
grid = np.array([[1 if arr[40+r*10+5, 40+c*10+5]==0 else 0
                  for c in range(N)] for r in range(N)])

fn = np.zeros((N,N), bool)
for r in range(9):
    for c in range(9):         fn[r,c]=True
    for c in range(N-8, N):    fn[r,c]=True
for r in range(N-8, N):
    for c in range(9):         fn[r,c]=True
for i in range(N):
    fn[6,i]=True; fn[i,6]=True
for r in range(20,25):
    for c in range(20,25):     fn[r,c]=True

um = grid.copy()
for r in range(N):
    for c in range(N):
        if not fn[r,c] and (r+c)%3==0: um[r,c]^=1

bits=[]; col=N-1; d=-1
while col>0:
    if col==6: col-=1
    for i in range(N):
        r = (N-1-i) if d==-1 else i
        for dc in (0,1):
            c = col-dc
            if not fn[r,c]: bits.append(um[r,c])
    col-=2; d=-d

cw = [int(''.join(map(str, bits[i:i+8])), 2) for i in range(0, 70*8, 8)]
b1, b2 = bytes(cw[0::2][:17] + cw[34::2]), bytes(cw[1::2][:17] + cw[35::2])
rs = RSCodec(18, nsize=35)
d1 = rs.decode(b1)[0]; d2 = rs.decode(b2)[0]
stream = ''.join(f'{b:08b}' for b in bytes(d1)+bytes(d2))
payload = stream[4:]  # drop mode, ignore char-count
flag_bytes = bytes(int(payload[i:i+8], 2) for i in range(0, (len(payload)//8)*8, 8))
print(flag_bytes)
# -> b'\x00CPCTF{z3r0_l3ngth_h1dd3n_d4t4}\x0e\xc1'
```
