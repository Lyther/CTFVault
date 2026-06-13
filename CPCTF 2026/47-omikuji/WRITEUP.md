# Omikuji

`omikuji` は not stripped の ELF で、`main` と `omikuji(std::string)` がそのまま残っています。

`main` を逆アセンブルすると、文字列を 1 文字ずつ `std::string` に `push_back` してから `omikuji()` に渡しています。つまりフラグ本体は乱数生成より前に完成済みです。

例えば `objdump -Mintel -d -C omikuji` の `main` では、こういう即値列が並びます。

```text
mov esi, 0x43  ; C
mov esi, 0x50  ; P
mov esi, 0x43  ; C
mov esi, 0x54  ; T
mov esi, 0x46  ; F
mov esi, 0x7b  ; {
...
mov esi, 0x7d  ; }
```

これをそのまま ASCII に戻すと:

```text
CPCTF{D3r_4173_wurf317_n1ch7}
```

`omikuji()` 側は `random_device` + `mt19937` で乱数を引き、運勢に応じてこの文字列の prefix を表示しているだけです。

- `rand == 2026` のときだけ全文を表示
- それ以外は `rand % 100` で分岐
- `substr(0, 10)`, `substr(0, 8)`, `substr(0, 6)`, `substr(0, 4)`, `substr(0, 2)` のどれかしか出さない

なので「運がよければフラグを教える」はミスディレクションで、実際には `main` を見れば終わりです。

Flag:

```text
CPCTF{D3r_4173_wurf317_n1ch7}
```
