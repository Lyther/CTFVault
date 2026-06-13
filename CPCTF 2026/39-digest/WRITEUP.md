# digest

The pcap contains a complete HTTP Digest Authentication exchange, so the server's rate limit does not matter. We can brute-force the password offline.

From the capture:

```text
username = cpctf
realm    = Restricted
method   = GET
uri      = /
nonce    = +pHR2klPBgA=dea9c5d3f34f861b03f0be19a41069cf29603de5
nc       = 00000001
cnonce   = 1afdf6a5de6ae0bc
qop      = auth
response = b71427f528886528c5144cd259a83d97
```

For Digest-MD5 with `qop=auth`:

```text
HA1 = MD5(username:realm:password)
HA2 = MD5(method:uri)
response = MD5(HA1:nonce:nc:cnonce:qop:HA2)
```

The challenge says the password is exactly 8 decimal digits, so we only need to test `00000000` through `99999999` offline against the captured transcript.

`HA2` is fixed:

```text
MD5("GET:/") = 71998c64aea37ae77020c49c00f73fa8
```

I used a small native brute-force program with OpenSSL MD5 and 12 threads. That recovered:

```text
37512859
```

Then authenticating to the current endpoint:

```text
https://digest.web.cpctf.space/
```

with username `cpctf` and password `37512859` returns:

```text
CPCTF{d1g3st_4uth_15_4_ch4ll3ng3}
```

Flag:

```text
CPCTF{d1g3st_4uth_15_4_ch4ll3ng3}
```

`crack.c` performs the offline password search, and `fetch_flag.py` fetches the live flag page with the recovered credentials.
