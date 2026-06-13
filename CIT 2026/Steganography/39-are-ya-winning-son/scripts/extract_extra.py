def find_extra_bytes(filename):
    with open(filename, "rb") as f:
        data = f.read()

    # Find SOS marker (0xFF 0xDA)
    sos_idx = data.find(b"\xff\xda")
    if sos_idx == -1:
        print("No SOS marker found")
        return

    # The scan header is variable length, but we can just look for the EOI marker
    eoi_idx = data.rfind(b"\xff\xd9")
    if eoi_idx == -1:
        print("No EOI marker found")
        return

    print(f"SOS at {sos_idx}, EOI at {eoi_idx}")

    # Let's just try to extract the last 8462 bytes before EOI
    extra = data[eoi_idx - 8462 : eoi_idx]
    with open("extra.bin", "wb") as f:
        f.write(extra)
    print("Wrote extra.bin")

    # Print first few bytes
    print("First 32 bytes:", extra[:32].hex())
    print("Last 32 bytes:", extra[-32:].hex())


find_extra_bytes(
    "/Users/bytedance/Documents/CTF/CIT 2026/Steganography/39-are-ya-winning-son/files/challenge.jpg",
)
