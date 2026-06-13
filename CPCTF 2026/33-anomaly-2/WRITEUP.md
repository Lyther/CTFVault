# Anomaly 2

The challenge code does not do RSA encryption at all:

```py
def rsa_encryption(flag):
    m = bytes_to_long(flag.encode())
    e = 3
    p, q = getPrime(512), getPrime(512)
    n = p * q
    c = pow(n, e, m)
    return (n, e, c)
```

So for each sample we get

```text
c = n^3 mod m
```

which means

```text
n^3 - c = k m
```

for some integer `k`.

We are given two independent pairs `(n1, c1)` and `(n2, c2)` for the same plaintext `m`, so:

```text
m | (n1^3 - c1)
m | (n2^3 - c2)
```

Therefore:

```text
m | gcd(n1^3 - c1, n2^3 - c2)
```

Computing that gcd gives:

```text
g = gcd(n1^3 - c1, n2^3 - c2) = 2m
```

So the plaintext integer is just:

```text
m = g / 2
```

Converting `m` back to bytes gives:

```text
CPCTF{7h3_n3x7_574710n_15_Kukud0}
```

Flag:

```text
CPCTF{7h3_n3x7_574710n_15_Kukud0}
```
