# Anomaly 2

- 作問: Naru820
- ジャンル: Crypto
- 難易度: Lv.3
- スコア: 128.50
- 提出回数上限: 100回

あの大人気問題がいろいろ 2 倍になって再登場！

- [chal.py](https://files.cpctf.space/Anomaly_2/chal_11b2c160203be5ff1faff97d47a20145736f862d4f6560638060d42b1131b49f.py)
- [output.txt](https://files.cpctf.space/Anomaly_2/output.txt)

## ヒント（解放済み）

`rsa_encryption` 関数の実装にはバグがあります。
具体的には、本来 `c = pow(m, e, n)` とするべきところを、`c = pow(n, e, m)` としてしまっています。よって、以下の式が成立します。

*c*<sub>1</sub> = *n*<sub>1</sub><sup>*e*<sub>1</sub></sup> (mod *m*), *c*<sub>2</sub> = *n*<sub>2</sub><sup>*e*<sub>2</sub></sup> (mod *m*)

よって、*n*<sub>1</sub><sup>*e*<sub>1</sub></sup> − *c*<sub>1</sub>, *n*<sub>2</sub><sup>*e*<sub>2</sub></sup> − *c*<sub>2</sub> はともに *m* の倍数であることがわかります。

## Attachment

- `chal_11b2c160203be5ff1faff97d47a20145736f862d4f6560638060d42b1131b49f.py`
- `output.txt`
