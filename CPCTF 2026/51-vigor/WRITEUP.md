# viGor (Rev, soramea)

**Flag:** `CPCTF{Br4ck3ts_7ouch_My_H34rt}`

## Recon

- Linux x86-64 Go binary, stripped, name "viGor" ⇒ Vigenère-style cipher.
- Strings show `Enter flag:`, `Wrong length`, `m\xf0I`, and an `ldpath` `/home/skyia/ctf/…/main.go`.
- The program is *not* a flag checker — it **computes and prints** whatever the user's input decodes to. The right input makes it print the flag.

## The main function (at `0x484900`)

1. `fmt.Print("Enter flag: ")`
2. Read line via `bufio.Reader.ReadBytes('\n')`, trim `\n`.
3. `utf8.RuneCountInString(input) == 3` — exactly 3 runes required (otherwise "Wrong length").
4. For each rune, the loop at `0x484b13` requires the UTF-8 bytes to start with `F0 9F`. This pins the input to three 4-byte emojis (`F0 9F xx yy`).
5. Tail-call the transform at `0x484520`.

## The transform (`0x484520`)

Two loops:

**Loop A** — build `user[6]`: walk the input 4 bytes at a time, append `bytes[i+2], bytes[i+3]` to a slice. So `user = [e1b2, e1b3, e2b2, e2b3, e3b2, e3b3]` (bytes 3 and 4 of each emoji's UTF-8).

**Loop B** — for `i = 0 … 29`:

```
out[i] = consts[i] ^ key[i] ^ user[i % 6]
```

- `consts` is the 30-entry table stacked at `[rsp+0x40]…[rsp+0x128]` (see `mov qword [rsp+0xXX], …` at `0x484573`+).
- `key` is the 30-byte blob at `0x4a31ee` (`E2 8C 89 E2 8F 9C E2 9D B3 EF B8 98 E2 A6 8B E2 8E A6 E2 9D B0 E2 A6 88 E2 8E 9F E2 8C A9` — the raw UTF-8 of a string of bracket-like Unicode symbols).
- The `0xAAAAAAAAAAAAAAAB` sequence with the `sar`/`lea`/`shl` is the usual signed division magic — here it computes `i % 6`.
- The built slice is printed via `fmt.Fprintln` at `0x484854` with no equality check.

## Invert

Because the first 6 output bytes must be `CPCTF{`, recover `user[0..5]` directly:

```python
consts = [4,108,82,23,81,74, 5,95,31,45,75, 6,51,101,76,116,121,126,
          36,69,119, 14,71,122, 15,13, 51,49,96,121]
key = bytes.fromhex('e28c89e28f9ce29db3efb898e2a68be28ea6e29db0e2a688e28e9fe28ca9')
user = [consts[i] ^ key[i] ^ b'CPCTF{'[i] for i in range(6)]
# -> [0xa5, 0xb0, 0x98, 0xa1, 0x98, 0xad]
```

Pack back into `F0 9F xx yy` triples:

- `F0 9F A5 B0` → 🥰 (U+1F970)
- `F0 9F 98 A1` → 😡 (U+1F621)
- `F0 9F 98 AD` → 😭 (U+1F62D)

Input `🥰😡😭` at the prompt and the program prints `CPCTF{Br4ck3ts_7ouch_My_H34rt}`.

## Full solver

```python
consts = [4,108,82,23,81,74, 5,95,31,45,75, 6,51,101,76,116,121,126,
          36,69,119, 14,71,122, 15,13, 51,49,96,121]
key = bytes.fromhex('e28c89e28f9ce29db3efb898e2a68be28ea6e29db0e2a688e28e9fe28ca9')
user = [consts[i] ^ key[i] ^ b'CPCTF{'[i] for i in range(6)]
flag = bytes(consts[i] ^ key[i] ^ user[i % 6] for i in range(30))
print(flag.decode())          # CPCTF{Br4ck3ts_7ouch_My_H34rt}
print(''.join(chr(0x1F000 | ((user[2*i] & 0x3F) << 6) | (user[2*i+1] & 0x3F))
              for i in range(3)))  # 🥰😡😭
```
