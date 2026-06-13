# 1, 0, 7

`N` looks huge, but its decimal representation is not random at all:

```text
1111...1111000...000777...7777
```

Counting the blocks gives:

- `317` copies of `1`
- `95` copies of `0`
- `317` copies of `7`

So we can rewrite `N` as:

```text
N = 111...111 * 10^(95+317) + 777...777
  = R * 10^412 + 7R
  = R * (10^412 + 7)
```

where

```text
R = 111...111 = (10^317 - 1) / 9
```

That immediately gives the factorization:

```text
p = (10^317 - 1) / 9
q = 10^412 + 7
N = p * q
```

Both `p` and `q` are prime, so this is ordinary RSA after the disguised factorization.

Then:

```text
phi(N) = (p - 1)(q - 1)
d = e^(-1) mod phi(N)
m = c^d mod N
```

Finally convert `m` from an integer to bytes.

Recovered plaintext:

```text
CPCTF{N_1s_34sy_70_bRe4k_873b4982a}
```

Flag:

```text
CPCTF{N_1s_34sy_70_bRe4k_873b4982a}
```
