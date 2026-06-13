# Bitwise Scramble (Crypto, Ida-ji)

**Flag:** `CPCTF{B1twis3_r0t4t10n!_3tim3s}`

## Setup

- Flag → `bytes_to_long` → decimal string → must be **75 digits**.
- Split into three 25-digit halves; zip each digit with the matching key digit (`"0123456789012109876543210"`).
- Each half uses a different-looking bitwise mixer:

  ```python
  enc_f = (f | k) & (f ^ k)
  enc_s = (s & k) ^ (s | k)
  enc_t = t ^ ((t | k) & k)
  ```

- Each result is formatted with `format(x, 'x')` and concatenated.

## Collapse the mixers

All three are just XOR in disguise:

| Expression | Simplification |
|---|---|
| `(f \| k) & (f ^ k)` | `f ^ k`  — `f^k` only sets differing bits, which are always ⊆ `f\|k` |
| `(s & k) ^ (s \| k)` | `f ^ k`  — common ⊕ either = symmetric difference |
| `t ^ ((t \| k) & k)` | `t ^ k`  — `k ⊆ t\|k`, so `(t\|k) & k = k` |

Hence the cipher is `enc_digit = f ^ k` written as one hex char (0-9a-f — since XOR of two decimal digits can hit 15).

Since both plaintext and key digits are in `0..9`, XOR is its own inverse and the recovery is unambiguous.

## Solver

```python
from Crypto.Util.number import long_to_bytes

enc = "10aa77170b38758c146245779086332e5e8237430f362d317310124333b999b890043152135"
key = "0123456789012109876543210"

digits = ""
for part in (enc[0:25], enc[25:50], enc[50:75]):
    for i, c in enumerate(part):
        digits += str(int(c, 16) ^ int(key[i]))

print(long_to_bytes(int(digits)))
# b'CPCTF{B1twis3_r0t4t10n!_3tim3s}'
```
