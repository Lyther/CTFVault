#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

from __future__ import annotations

import base64
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "8_KUBSTU_Financial_Report_2025.pdf"


def extract_hidden_audit_data(pdf_text: str) -> str:
    start = pdf_text.index("/HiddenAuditData (") + len("/HiddenAuditData (")
    end = pdf_text.index(")\n>>\n>>\nstartxref", start)
    return pdf_text[start:end]


def decode_base64_candidates(payload: str) -> str:
    pattern = re.compile(r"([A-Za-z0-9+/=]{20,})")

    for match in pattern.finditer(payload):
        token = match.group(1)
        padded = token + "=" * ((4 - len(token) % 4) % 4)

        try:
            decoded = base64.b64decode(padded, validate=False)
        except Exception:
            continue

        if b"KubSTU{" in decoded:
            return decoded.decode("utf-8")

    raise RuntimeError("flag not found in HiddenAuditData")


def main() -> None:
    pdf_text = CHALLENGE.read_text(encoding="latin1")
    payload = extract_hidden_audit_data(pdf_text)
    flag = decode_base64_candidates(payload)
    print(flag)


if __name__ == "__main__":
    main()
