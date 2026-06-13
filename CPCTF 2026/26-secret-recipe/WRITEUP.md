# Secret Recipe

The pcap captures plain HTTP traffic from `192.168.3.3` to a Python `SimpleHTTPServer` on `192.168.3.10:8000`. Reassembling the four TCP streams (`scapy`, sort by `seq`, slice after `\r\n\r\n`) recovers the four served bodies:

- `index.html` — recipe page, includes `<img src="./image.jpg">` under the section `秘密のコツ`.
- `styles.css` — page styling (irrelevant).
- `image.jpg` — JPEG of a soy-sauce bottle plus a handwritten paper.
- `404.html` — for `/favicon.ico`.

EXIF / JPEG markers are clean, so the flag is just the handwritten note in `image.jpg`. Crop to the lower-right region and upscale (`PIL`, LANCZOS x8) until readable:

```text
CPCTF{5l)j-sov(7}
```

Apply the substitution rules from the problem:

- `(`, `)`, `l` are visually ambiguous with `1` → replace with `1`
- `-` is not in the flag → it must be `_`

```text
5  l  )  j  _  s  o  v  (  7
5  1  1  j  _  s  o  v  1  7
```

Flag:

```text
CPCTF{511j_sov17}
```
