#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

from __future__ import annotations

import os
import pathlib
import re
import shutil
import stat
import subprocess
import tempfile
import textwrap

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "reallysecurepasswordmanager"
FLAG_RE = re.compile(r"RET=(CIT\{[^}\r\n]+\})")
TOKEN = "notronnie_local_token_v1"


def find_real_tty() -> pathlib.Path:
    pts_dir = pathlib.Path("/dev/pts")
    uid = os.getuid()
    candidates: list[pathlib.Path] = []

    if not pts_dir.is_dir():
        raise RuntimeError("`/dev/pts` is missing. Run this solver on Linux.")

    for path in pts_dir.iterdir():
        if path.name == "ptmx":
            continue

        try:
            st = path.stat()
        except OSError:
            continue

        if not stat.S_ISCHR(st.st_mode):
            continue
        if st.st_uid != uid:
            continue

        candidates.append(path)

    if not candidates:
        raise RuntimeError(
            "No `/dev/pts/*` device owned by the current uid was found. "
            "Run the solver inside a real PTY.",
        )

    return sorted(
        candidates,
        key=lambda path: int(path.name) if path.name.isdigit() else path.name,
    )[-1]


def build_gdb_script(home_dir: pathlib.Path, tty_path: pathlib.Path) -> str:
    uid = os.getuid()
    gid = os.getgid()

    return (
        textwrap.dedent(
            f"""
        set pagination off
        set confirm off
        set environment HOME {home_dir}

        break *0x4092ac
        commands
          silent
          set {{unsigned char}}0x602c40 = 1
          continue
        end

        break *0x537bd0
        commands
          silent
          set {{char[16]}}0x60b000 = "notronnie"
          set {{char[8]}}0x60b020 = "x"
          set {{char[8]}}0x60b040 = ""
          set {{char[{len(str(home_dir)) + 1}]}}0x60b060 = "{home_dir}"
          set {{char[16]}}0x60b090 = "/bin/bash"
          set {{long long}}0x60b100 = 0x60b000
          set {{long long}}0x60b108 = 0x60b020
          set {{int}}0x60b110 = {uid}
          set {{int}}0x60b114 = {gid}
          set {{long long}}0x60b118 = 0x60b040
          set {{long long}}0x60b120 = 0x60b060
          set {{long long}}0x60b128 = 0x60b090
          return (void*)0x60b100
          continue
        end

        break *0x538410
        commands
          silent
          set {{char[16]}}$rdi = "notronnie"
          return (int)0
          continue
        end

        break *0x534a20
        commands
          silent
          set {{char[{len(str(tty_path)) + 1}]}}0x60b200 = "{tty_path}"
          return (char*)0x60b200
          continue
        end

        break *0x4092b1
        commands
          silent
          set $obj = $rbp-0x40
          set $ptr = *(char**)$obj
          printf "RET=%s\\n", $ptr
          quit
        end

        run < {home_dir.parent / "input.txt"}
        quit
        """,
        ).strip()
        + "\n"
    )


def extract_flag() -> str:
    if shutil.which("gdb") is None:
        raise RuntimeError("`gdb` is required to solve this challenge.")
    if not CHALLENGE.is_file():
        raise RuntimeError(f"Challenge binary not found: {CHALLENGE}")

    tty_path = find_real_tty()

    with tempfile.TemporaryDirectory(prefix="rspm-") as tmp_dir_name:
        tmp_dir = pathlib.Path(tmp_dir_name)
        binary_path = tmp_dir / CHALLENGE.name
        home_dir = tmp_dir / "home"
        token_path = home_dir / ".pm_token"
        input_path = tmp_dir / "input.txt"
        gdb_path = tmp_dir / "solve.gdb"

        shutil.copy2(CHALLENGE, binary_path)
        os.chmod(binary_path, 0o755)
        home_dir.mkdir(mode=0o700)
        token_path.write_text(TOKEN, encoding="utf-8")
        os.chmod(token_path, 0o600)
        input_path.write_text("3\nflag\n", encoding="utf-8")
        gdb_path.write_text(build_gdb_script(home_dir, tty_path), encoding="utf-8")

        result = subprocess.run(
            ["gdb", "-q", str(binary_path), "-x", str(gdb_path)],
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )

    output = result.stdout + result.stderr
    match = FLAG_RE.search(output)
    if match is None:
        raise RuntimeError(f"Failed to recover the flag.\n{output}")

    return match.group(1)


def main() -> None:
    print(extract_flag())


if __name__ == "__main__":
    main()
