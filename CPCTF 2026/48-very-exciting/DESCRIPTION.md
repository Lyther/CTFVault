# Very Exciting

- 作問: Nzt3
- ジャンル: Crypto
- 難易度: Lv.2
- スコア: 97.07
- 提出回数上限: 100回

ワクワクする乱数をあなたにも使わせてあげます。

```shell
nc 133.88.122.244 32007
```

## ヒント（解放済み）

`main` 関数内で使われている `stream_excite` 関数に注目しましょう。
この関数では `nextrand` (8 bytes の乱数を生成する関数) を用いて生成した乱数列 `keystream` と `data` を XOR しています。
`keystream` は乱数生成器に与えた `key` と `iv` から生成されますが、`key` は非公開ですね。
公開されている情報だけから `keystream` を特定できないでしょうか。

## Attachment

- `server_5dd79bdc6f546c5f0a01a3568e6fe0bbd190887ff16eaf8c34613559c2c574e7.py` (original distribution)
- `server.py` (renamed copy)
