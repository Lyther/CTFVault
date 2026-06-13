# ssh2

The server tells us that commands which directly print file contents are banned.

`ban.txt` contains:

```text
cat,tac,less,more,head,tail,nl,rev
```

After logging in, I enumerated the filesystem with `find` and found the target file:

```text
/flag/flag.txt
```

The blacklist only blocks a few command names. It does not prevent using other programs to open and print the file, so `python3` is enough:

```bash
python3 -c 'print(open("/flag/flag.txt").read())'
```

That prints:

```text
CPCTF{8ury_0n35_h34d_1n_7h3_54nd80x}
```

Flag:

```text
CPCTF{8ury_0n35_h34d_1n_7h3_54nd80x}
```
