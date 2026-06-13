# Very Exciting

`server.py` rolls a custom 8-byte-output stream PRNG (`BoringRandom`) keyed by `(secret_key, iv)` and uses it as a one-time-pad to encrypt the flag.

The protocol then offers an oracle:

1. Print `exciting_iv` and `enc_flag = flag XOR keystream(secret_key, exciting_iv)`.
2. Read your bytes `your_favorite` (must not equal `enc_flag`).
3. Read your `very_exciting_iv` (16 bytes, **no further check**).
4. Print `enc_your_favorite = your_favorite XOR keystream(secret_key, very_exciting_iv)`.

Since `very_exciting_iv` may equal `exciting_iv`, just reuse it. With `your_favorite = "\x00" * len(enc_flag)`, the oracle returns the keystream directly:

```text
your_favorite      = 00 00 ... 00       # all zeros
very_exciting_iv   = exciting_iv        # same key+iv → same keystream
enc_your_favorite  = keystream
flag               = enc_flag XOR keystream
```

The `your_favorite == exciting_flag` check is bypassed trivially because `enc_flag` is not all-zero.

`solve.py` implements this end-to-end against `nc 133.88.122.244 32007`.

Flag:

```text
CPCTF{SAMe_01d_STReam_1s_A1WaYs_b0r1ng}
```
