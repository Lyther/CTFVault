# Writeup: Brainiac

## Flag

`CIT{Wh@t_in_th3_w0rld_i$_th1s_l@ngu@g3}`

## Solve

`challenge.txt` is a Brainfuck program — only `+ - < > . [ ]` are used and
it opens with the canonical `++++++++++[>+>+++>+++++++>++++++++++<<<<-]`
multiplier loop that seeds four cells (10, 30, 70, 100) with magnitudes
close to printable ASCII ranges.

Running it through a standard 8-bit wrap-around interpreter prints the
flag directly.

```console
$ python3 scripts/solve.py
CIT{Wh@t_in_th3_w0rld_i$_th1s_l@ngu@g3}
```

## Notes

The challenge description advertises
`SHA1: 33746b3052f748a9d41f030d2be4f196d02453cb`, which does not match
`sha1("CIT{Wh@t_in_th3_w0rld_i$_th1s_l@ngu@g3}")`. The Brainfuck output
is the string the scoreboard accepts; the published SHA1 is either over a
different canonicalization of the flag or stale.
