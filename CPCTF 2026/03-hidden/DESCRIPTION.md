# Hidden

- 作問: soramea
- ジャンル: Reversing
- 難易度: Lv.1
- スコア: 10.00
- 提出回数上限: 100回

隠された flag を見つけ出そう！

## ヒント（解放済み）

これは ELF 形式の実行ファイルです。まずは Linux 環境で実行してみましょう。(Windows なら WSL や、Mac なら docker を使うことが出来ます。Webshell を使ってもよいです。) 実行すると、「flag はこのファイルのどこかに隠されているよ！」といったメッセージが出てくるはずです。

linux には `strings` というコマンドがあり、これを使うとファイルの中の出力可能な文字列を表示してくれます。これを与えられたファイルに対して使用することで、flag を得ることができます。

## Attachment

- `hidden` (ELF binary)
- `hidden-4087512ab00b5ef09975f0fd6b78ae7021b6a1d4c0798ad47ecc0e45bccb4894.zip` (original distribution)
