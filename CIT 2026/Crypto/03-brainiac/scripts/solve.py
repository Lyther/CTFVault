#!/usr/bin/env python3
"""Brainfuck interpreter for CIT 2026 - Brainiac."""

from pathlib import Path


def run_bf(code: str) -> bytes:
    tape = [0] * 30000
    ptr = 0
    i = 0
    out = bytearray()
    loop_stack: list[int] = []
    while i < len(code):
        c = code[i]
        if c == ">":
            ptr += 1
        elif c == "<":
            ptr -= 1
        elif c == "+":
            tape[ptr] = (tape[ptr] + 1) & 0xFF
        elif c == "-":
            tape[ptr] = (tape[ptr] - 1) & 0xFF
        elif c == ".":
            out.append(tape[ptr])
        elif c == "[":
            if tape[ptr] == 0:
                depth = 1
                while depth:
                    i += 1
                    if code[i] == "[":
                        depth += 1
                    elif code[i] == "]":
                        depth -= 1
            else:
                loop_stack.append(i)
        elif c == "]":
            if tape[ptr] != 0:
                i = loop_stack[-1]
            else:
                loop_stack.pop()
        i += 1
    return bytes(out)


def main() -> None:
    src = Path(__file__).resolve().parent.parent / "files" / "challenge.txt"
    print(run_bf(src.read_text()).decode())


if __name__ == "__main__":
    main()
