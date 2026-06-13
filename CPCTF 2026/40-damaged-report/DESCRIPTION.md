# Damaged Report

- 作問: Alph_Suima
- ジャンル: Misc
- 難易度: Lv.4
- スコア: 292.21
- 提出回数上限: 100回

我々の協力者、コードネーム "K" から緊急の報告書が届いた。彼は筋金入りの TeX 愛好家で、通信には必ず彼独自の TeX フォーマットファイルを使用する。

- <https://files.cpctf.space/l0v3_t3x/D4mag3d_rep0rt.fmt>
- Docker image: <https://hub.docker.com/r/kininakuni/atexoder>

## ヒント（解放済み）

`a`, `g` のカテゴリーコードが 13 に割り振られているので、そのままでは `\flag` を呼び出すことは出来ません。
`.fmt` ファイルを解析すると、`help` という文字列が見られるので、`\help` に対して、`\show` プリミティブを使うことを検討するのは如何でしょうか？

## Attachment

- `D4mag3d_rep0rt.fmt`
- `solve.tex`
