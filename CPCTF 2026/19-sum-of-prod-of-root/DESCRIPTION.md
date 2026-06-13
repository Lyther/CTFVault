# Sum of Prod of Root

- 作問: alyth_sol
- ジャンル: PPC
- 難易度: Lv.3
- スコア: 344.19
- 提出回数上限: 100回

[yukicoder へのリンク](https://yukicoder.me/problems/13164)

## 注意

この問題に回答する際は生成AI等を用いてはいけません。

## 問題文

正整数 *N* が与えられます。次の値を 998244353 で割った余りを出力してください。

\[ \sum_{i=1}^{N} \prod_{k=1}^{\infty} \left\lfloor i^{1/k} \right\rfloor \]

## 制約

- 1 ≤ *N* ≤ 10<sup>18</sup>
- 入力は全て整数

## ヒント（解放済み）

*k* が小さいときは ⌊*i*<sup>1/*k*</sup>⌋ は *i* が増加すると頻繁に値が変わりますが、逆に *k* が大きいときは ⌊*i*<sup>1/*k*</sup>⌋ の値は *i* が増加してもあまり値が変化しません。
