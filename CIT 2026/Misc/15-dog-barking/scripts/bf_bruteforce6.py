import itertools

clusters = [
    "A",
    "DE",
    "A",
    "A",
    "A",
    "A",
    "CE",
    "DFDE",
    "B",
    "A",
    "DFE",
    "A",
    "A",
    "DDE",
    "A",
    "A",
    "CE",
    "B",
    "A",
    "CE",
    "A",
    "CE",
    "A",
    "CE",
    "A",
    "A",
    "B",
    "A",
    "CE",
    "CE",
    "DDE",
    "DE",
    "A",
    "DE",
    "DE",
    "B",
    "A",
    "DCE",
    "CE",
    "A",
    "A",
    "A",
    "DE",
    "A",
    "B",
    "A",
    "A",
    "DFDE",
    "DE",
    "A",
    "DE",
    "A",
    "A",
    "B",
    "A",
    "DDE",
    "DFE",
    "DE",
    "A",
    "A",
    "DE",
    "A",
    "B",
    "A",
    "DFE",
    "DE",
    "A",
    "DE",
    "A",
    "DE",
    "CE",
    "B",
    "A",
    "CE",
    "CE",
    "A",
    "CE",
    "A",
    "A",
    "CE",
    "B",
    "A",
    "CE",
    "DCE",
    "A",
    "CE",
    "DFDE",
    "DE",
    "A",
    "B",
    "A",
    "DFE",
    "DE",
    "A",
    "A",
    "DFE",
    "DE",
    "CE",
    "B",
    "A",
    "CE",
    "A",
    "CE",
    "CE",
    "DDE",
    "DFE",
    "DE",
    "B",
    "A",
    "DE",
    "CE",
    "CE",
    "A",
    "CE",
    "A",
    "CE",
    "B",
    "A",
    "CE",
    "DDE",
    "DE",
    "A",
    "A",
    "A",
    "A",
    "B",
    "A",
    "CE",
    "A",
    "CE",
    "CE",
    "DDE",
    "DFE",
    "DE",
    "B",
    "A",
    "DE",
    "CE",
    "CE",
    "A",
    "CE",
    "A",
    "A",
    "B",
    "A",
    "CE",
    "CE",
    "A",
    "CE",
    "A",
    "A",
    "A",
    "B",
    "A",
    "A",
    "DFE",
    "DE",
    "A",
    "A",
    "DFE",
    "DE",
    "B",
    "A",
    "DE",
    "A",
    "DE",
    "CE",
    "CE",
    "DDE",
    "DFE",
    "B",
    "A",
    "DE",
    "DE",
    "CE",
    "A",
    "CE",
    "CE",
    "DDE",
    "B",
    "A",
    "DDE",
    "DFE",
    "DE",
    "A",
    "A",
    "DE",
    "A",
    "B",
    "A",
    "A",
    "DDE",
    "DFE",
    "A",
    "A",
    "A",
    "A",
    "B",
    "A",
    "CE",
    "CE",
    "A",
    "CE",
    "CE",
    "DFE",
    "A",
    "B",
    "A",
    "DDE",
    "DFE",
    "A",
    "A",
    "DFDE",
    "DE",
    "DE",
    "B",
    "A",
    "DCE",
    "A",
    "DCE",
    "CE",
    "CE",
    "DDE",
    "DE",
    "B",
    "A",
    "DE",
    "DE",
    "CE",
    "A",
    "CE",
    "A",
    "A",
    "B",
    "A",
    "DE",
    "CE",
    "CE",
    "A",
    "A",
    "CE",
    "A",
    "B",
    "A",
    "A",
    "DE",
    "CE",
    "A",
    "A",
    "DE",
    "CE",
    "B",
    "A",
    "A",
    "DE",
    "CE",
    "A",
    "A",
    "DCE",
    "CE",
    "B",
    "A",
    "CE",
    "CE",
    "DFDE",
    "DE",
    "DE",
    "A",
    "DE",
]

unique_clusters = list(set(clusters))
bf_chars = "><+-.,[]"


def run_bf(code):
    tape = [0] * 30000
    ptr = 0
    i = 0
    out = bytearray()

    jumps = {}
    temp_stack = []
    for pos, c in enumerate(code):
        if c == "[":
            temp_stack.append(pos)
        elif c == "]":
            if temp_stack:
                start = temp_stack.pop()
                jumps[start] = pos
                jumps[pos] = start
            else:
                jumps[pos] = len(code)  # Jump to end if unmatched ]
    for pos in temp_stack:
        jumps[pos] = len(code)  # Jump to end if unmatched [

    steps = 0
    while i < len(code):
        steps += 1
        if steps > 100000:
            return out

        c = code[i]
        if c == ">":
            ptr += 1
            if ptr >= 30000:
                return out
        elif c == "<":
            ptr -= 1
            if ptr < 0:
                return out
        elif c == "+":
            tape[ptr] = (tape[ptr] + 1) & 0xFF
        elif c == "-":
            tape[ptr] = (tape[ptr] - 1) & 0xFF
        elif c == ".":
            out.append(tape[ptr])
        elif c == ",":
            tape[ptr] = 0
        elif c == "[":
            if tape[ptr] == 0:
                i = jumps[i]
                if i == len(code):
                    return out
        elif c == "]":
            if tape[ptr] != 0:
                i = jumps[i]
                if i == len(code):
                    return out
        i += 1
    return bytes(out)


for p in itertools.permutations(bf_chars):
    mapping = dict(zip(unique_clusters, p))
    code = "".join(mapping[c] for c in clusters)

    out = run_bf(code)
    if b"CIT{" in out:
        print(f"Found! Mapping: {mapping}")
        print(f"Output: {out.decode('ascii', 'ignore')}")
        break
