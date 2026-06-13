# bembembem — Writeup

- Category: Stego
- Value: 988

## Challenge

> Здесь точно есть флаг, но придётся пройти через Мурино, Молочное и возможно встретить котость
>
> ---
>
> There is definitely a flag here, but you'll have to go through Murino, Molochnoe, and you might encounter a "cat-ness" along the way.

## Recon

The file is a one-hour MP4 with audio and video, but the useful part is its tail. `exiftool` reports a suspicious warning about truncated data near the end of the file, and the top-level MP4 structure confirms a small `uuid` atom followed by extra bytes after the last valid atom.

The `uuid` payload starts with:

```text
Drun/v1
# decode: base64 -> zlib inflate -> utf-8
```

Decoding that block reveals the hidden note. The important parts are:

- look at the spectrogram around the 42nd minute, above 10 kHz
- the spectrogram contains the ZIP password
- the MP4 tail after the last atom is XORed with the metadata key `vid_md5`

The `vid_md5` value in the MP4 metadata is:

```text
6899efc8f52bffb08c5ac45deee24f64
```

## Solve

Take the bytes after the last valid MP4 atom and XOR them with the repeating ASCII key `6899efc8f52bffb08c5ac45deee24f64`. That produces a valid encrypted ZIP archive containing:

- `flag.txt`
- `readme.txt`

The spectrogram password turned out to be:

```text
K0t05t
```

The case matters. With that password, extracting `flag.txt` yields the final flag.

## Flag

```text
KubSTU{3nj0y_1h_0f_M3ll57r0y_m3m3s}
```

## Files

- [51_bembembem.mp4](./files/51_bembembem.mp4)
- [solve.py](./scripts/solve.py)
