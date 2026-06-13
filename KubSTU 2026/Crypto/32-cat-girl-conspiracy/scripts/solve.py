#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

import hashlib
import pathlib
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "32_64_what_could_this_mean.zip"
HASH_LIST = "what_could_this_mean.txt"


def main() -> None:
    with zipfile.ZipFile(CHALLENGE) as archive:
        hash_stream = archive.read(HASH_LIST).decode("ascii").strip()
        digest_to_path = {
            hashlib.sha256(archive.read(name)).hexdigest(): name
            for name in archive.namelist()
            if name.endswith(".jpg")
        }

    flag = "".join(
        digest_to_path[hash_stream[i : i + 64]].split("/", 1)[0]
        for i in range(0, len(hash_stream), 64)
    )
    print(flag)


if __name__ == "__main__":
    main()
