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
            if not temp_stack:
                return b""
            start = temp_stack.pop()
            jumps[start] = pos
            jumps[pos] = start
    if temp_stack:
        return b""

    steps = 0
    while i < len(code):
        steps += 1
        if steps > 100000:
            return b""

        c = code[i]
        if c == ">":
            ptr += 1
        elif c == "<":
            ptr -= 1
            if ptr < 0:
                return b""
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
        elif c == "]":
            if tape[ptr] != 0:
                i = jumps[i]
        i += 1
    return bytes(out)


print(
    run_bf(
        "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.",
    ),
)
