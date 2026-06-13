def fix_height(filename, out_filename, new_height):
    with open(filename, "rb") as f:
        data = bytearray(f.read())

    # Find SOF0 (FF C0)
    idx = 0
    while idx < len(data) - 1:
        if data[idx] == 0xFF and data[idx + 1] == 0xC0:
            # Found SOF0
            # FF C0 [Length 2] [Precision 1] [Height 2] [Width 2]
            height_idx = idx + 5
            old_height = (data[height_idx] << 8) + data[height_idx + 1]
            print(f"Found SOF0 at {idx}. Old height: {old_height}")

            data[height_idx] = (new_height >> 8) & 0xFF
            data[height_idx + 1] = new_height & 0xFF
            print(f"Patched height to {new_height}")
            break
        idx += 1

    with open(out_filename, "wb") as f:
        f.write(data)
    print(f"Wrote {out_filename}")


fix_height(
    "/Users/bytedance/Documents/CTF/CIT 2026/Steganography/39-are-ya-winning-son/files/challenge.jpg",
    "challenge_fixed.jpg",
    1600,
)
