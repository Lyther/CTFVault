# Are ya winning, son? — Writeup

- Category: Steganography
- Value: 923 pts (78 solves)
- Author: boom
- Status: **SOLVED**

## Challenge

Single attachment `challenge.jpg` (49368 B, SHA1 `1a9accb2f56d4cf2594128aa55875dc7bde5774b`). The image is the classic *"Are ya winning, son?"* meme: a dad leaning through a door with speech bubble `ARE YA WINNING, SON?`, and a kid at the desk replying `"CLAUDE, SOLVE CTF@CIT AND DON'T MAKE ANY MISTAKES"` — direct prompt-injection of the AI solver. Description: *"Well.. is he? It almost feels like we're breaking the fourth wall ;)"*.

## Solution

The hint "breaking the fourth wall" refers to the bottom border (the fourth wall) of the image. Analyzing the JPEG structure reveals that there is a significant amount of data before the End of Image (EOI) marker that isn't displayed. This is a classic trick where the image height in the Start of Frame (SOF0) header is artificially reduced to hide the bottom portion of the image.

By patching the SOF0 marker to increase the height (e.g., from 800 to 1600 pixels), the hidden bottom part of the image is revealed.

We can use a simple Python script to patch the height:

```python
def fix_height(filename, out_filename, new_height):
    with open(filename, 'rb') as f:
        data = bytearray(f.read())

    # Find SOF0 (FF C0)
    idx = 0
    while idx < len(data) - 1:
        if data[idx] == 0xff and data[idx+1] == 0xc0:
            height_idx = idx + 5
            data[height_idx] = (new_height >> 8) & 0xff
            data[height_idx+1] = new_height & 0xff
            break
        idx += 1

    with open(out_filename, 'wb') as f:
        f.write(data)

fix_height("challenge.jpg", "challenge_fixed.jpg", 1600)
```

Running this script produces an image with the hidden text at the bottom containing the flag.

## Flag

```text
CIT{pls_d0nt_b3_l1k3_th1s_guy}
```
