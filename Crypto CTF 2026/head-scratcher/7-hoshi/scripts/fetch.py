#!/usr/bin/env python3
"""Fetch one Hoshi instance and save public data for offline solving."""
import json, re, sys
from pathlib import Path
from pwn import remote, context

context.log_level = "info"

def fetch(host="91.107.252.0", port=31117):
    r = remote(host, port)
    r.recvuntil(b"[Q]uit")
    r.sendline(b"b")
    data = r.recvuntil(b"[Q]uit").decode()
    ys = list(map(int, re.findall(r"BPT_\d+ = (\d+)", data)))
    r.sendline(b"e")
    data2 = r.recvuntil(b"[Q]uit").decode()
    xs = list(map(int, re.findall(r"EPT_\d+ = (\d+)", data2)))
    r.close()
    return {"ys": ys, "xs": xs}

if __name__ == "__main__":
    d = fetch()
    out = Path("instance.json")
    out.write_text(json.dumps(d, indent=2))
    print("saved", out, len(d["ys"]), len(d["xs"]))
    print(d)
