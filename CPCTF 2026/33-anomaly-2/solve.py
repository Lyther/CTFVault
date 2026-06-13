from math import gcd
from pathlib import Path


def to_bytes(n: int) -> bytes:
    h = hex(n)[2:]
    if len(h) % 2:
        h = "0" + h
    return bytes.fromhex(h)


def main() -> None:
    vals = {}
    for line in Path("output.txt").read_text().splitlines():
        k, v = line.split(" = ", 1)
        vals[k] = int(v)

    x1 = pow(vals["n1"], vals["e1"]) - vals["c1"]
    x2 = pow(vals["n2"], vals["e2"]) - vals["c2"]
    g = gcd(x1, x2)

    for d in range(1, 100):
        if g % d:
            continue
        m = g // d
        b = to_bytes(m)
        if b.startswith(b"CPCTF{") and b.endswith(b"}"):
            print(b.decode())
            return

    raise SystemExit("flag not found")


if __name__ == "__main__":
    main()
