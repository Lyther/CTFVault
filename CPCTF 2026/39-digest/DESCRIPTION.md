# digest

- 作問: ramdos
- ジャンル: Forensics
- 難易度: Lv.3
- スコア: 201.42
- 提出回数上限: 100回

パスワードは数字 8 桁だけど、サーバーにはレートリミットを掛けているから総当たりされることもないはず！
ちゃんとダイジェスト認証にしているから、pcap を公開しても安全、だよね？

- 添付ファイル: <https://files.cpctf.space/digest-f57ffe5f92e996f27bfaea5b8f21b051a9eab164d25f98a9a69a7e2d497dd0be.pcap>
- 接続先: <https://digest.web.cpctf.space/>

## 4/17 21:25 追記

接続先が <https://digest.web.cpctf.space/> に変更されました。pcap の内容は http のままになっていますが、無視して <https://digest.web.cpctf.space/> に接続してください。

## ヒント（解放済み）

Digest 認証の `response` フィールドは `H(H(A1):nonce:nc:cnonce:qop:H(A2))` で計算されます（`H(A1)` と `H(A2)` の定義は RFC 7616 を参照してください）。
pcap に含まれる情報から、パスワードを、ひいては `H(A1)` の値を総当たりできそうです…

## Attachment

- `digest-f57ffe5f92e996f27bfaea5b8f21b051a9eab164d25f98a9a69a7e2d497dd0be.pcap`
- `crack.c`, `crack` (helper brute-forcer)
- `fetch_flag.py`
