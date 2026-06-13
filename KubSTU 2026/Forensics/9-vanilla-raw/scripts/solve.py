#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

import pathlib
import re
import subprocess
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "9_memory.rar"


def extract_memory() -> pathlib.Path:
    temp_dir = pathlib.Path(tempfile.mkdtemp(prefix="vanilla-raw-"))
    subprocess.run(
        [
            "bsdtar",
            "-xf",
            str(CHALLENGE),
            "-C",
            str(temp_dir),
        ],
        check=True,
    )
    memory = temp_dir / "memory.raw"
    if not memory.exists():
        raise ValueError("memory.raw was not extracted")
    return memory


def find_nonzero_region(memory: pathlib.Path) -> tuple[int, int]:
    chunk_size = 1024 * 1024
    first = None
    last = None

    with memory.open("rb") as handle:
        offset = 0
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break

            if any(chunk):
                if first is None:
                    for index, byte in enumerate(chunk):
                        if byte:
                            first = offset + index
                            break

                for index in range(len(chunk) - 1, -1, -1):
                    if chunk[index]:
                        last = offset + index
                        break

            offset += len(chunk)

    if first is None or last is None:
        raise ValueError("no non-zero region found")

    return first, last + 1


def extract_flag(memory: pathlib.Path, start: int, end: int) -> str:
    with memory.open("rb") as handle:
        handle.seek(start)
        blob = handle.read(end - start)

    for lane in range(4):
        candidate = blob[lane::4]
        match = re.search(rb"KubSTU\{[^}]+\}", candidate)
        if match:
            return match.group(0).decode()

    raise ValueError("flag not found in any 4-byte lane")


def main() -> None:
    memory = extract_memory()
    start, end = find_nonzero_region(memory)
    print(extract_flag(memory, start, end))


if __name__ == "__main__":
    main()
