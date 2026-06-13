# Damaged Report

Contest note: CTF jeopardy challenge. The target is a flag, not an ACM-style output.

The `.fmt` file is a preloaded TeX format. Running it inside the provided Docker image immediately shows that the format has sabotaged tokenization:

```sh
docker run --rm --platform linux/amd64 \
  -v "$PWD:/work" -w /work --entrypoint sh kininakuni/atexoder -c '
  cp D4mag3d_rep0rt.fmt /tmp/d4.fmt
  tex -interaction=nonstopmode --fmt=/tmp/d4.fmt solve.tex 2>&1
'
```

Two quick probes reveal the important parts:

- `\help{1}` prints: `the flag is stored in the control sequence named flag.`
- `\help{2}` / `\help{3}` / `\help{4}` say to use `\csn`, `\endcsn`, and `\low`.

Directly writing `\flag` does **not** access the real control sequence. In this format:

- `a` is an active character that expands to `\print (a is a active char.)`
- `g` is also active and expands to `\print (protected.)`

So `\flag` is tokenized as `\fl` + active `a` + active `g`, and the visible dummy path expands to `CPCTF{Dummy!}`.

The intended bypass is to synthesize the literal letters `a` and `g` as normal letter tokens. `\low` is an alias for `\lowercase`, so uppercase `A` and `G` can be lowered inside the token list passed to `\csn...\endcsn`:

```tex
\low{\csn flAG\endcsn}
```

After `\low`, TeX sees:

```tex
\csn flag\endcsn
```

which constructs and executes the real control sequence `\flag`.

Minimal payload:

```tex
\low{\csn flAG\endcsn}
```

Running that prints:

```text
CPCTF{h4ve4G0oDTeXlif3}
```

Flag:

```text
CPCTF{h4ve4G0oDTeXlif3}
```
