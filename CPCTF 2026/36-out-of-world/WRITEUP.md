# Out of World

The binary looks like it does nothing because `main` only calls `getenv("CTF_SECRET_KEY")`, checks the result, and prints `See you!` if the check fails.

The check routine does this:

1. require the environment variable to exist,
2. require its length to be `0x18 = 24`,
3. for each byte, verify `input[i] ^ 0x23 == table[i]`.

The table is stored in `.data` at `0x4050`:

```text
77 6b 6a 70 7c 6a 70 7c 70 76 73 66 71 7c 70 66
60 71 66 77 7c 68 66 7a
```

So the hidden environment value is just that table XORed with `0x23`:

```text
THIS_IS_SUPER_SECRET_KEY
```

If the check passes, another routine decrypts the flag. It takes the 41-byte blob at `0x4020` and computes:

```text
flag[i] = enc[i] ^ key[i mod 24] ^ 0x45
```

Using the recovered key gives:

```text
CPCTF{c4n_y0u_f1nd_3nv1r0nm3n7_v4r1abl35}
```

Flag:

```text
CPCTF{c4n_y0u_f1nd_3nv1r0nm3n7_v4r1abl35}
```
