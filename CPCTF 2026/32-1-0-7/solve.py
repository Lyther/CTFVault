from pathlib import Path


def main() -> None:
    lines = (
        Path(
            "107107_b38e4b4bcd49c22b496049abb867695331cdc0f7542dd59288b3597e1b8e4119.txt",
        )
        .read_text()
        .splitlines()
    )
    n = int(lines[0].split("=", 1)[1])
    e = int(lines[1].split("=", 1)[1])
    c = int(lines[2].split("=", 1)[1])

    p = (10**317 - 1) // 9
    q = 10**412 + 7
    assert p * q == n

    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    m = pow(c, d, n)

    h = hex(m)[2:]
    if len(h) % 2:
        h = "0" + h
    print(bytes.fromhex(h).decode())


if __name__ == "__main__":
    main()
