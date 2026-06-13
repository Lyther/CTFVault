# credentials

- 作問: ramdos
- ジャンル: Forensics
- 難易度: Lv.3
- スコア: 142.59
- 提出回数上限: 100回

間違えて配布ファイルをフラグ入りで commit しちゃった！
でも大丈夫！次のコマンドで履歴から「完全に」削除したから、この配布ファイルを配ってもフラグは絶対にバレないはず。

```shell
git filter-branch --index-filter "git rm -rf --cached --ignore-unmatch flag.txt" --prune-empty -- --all
```

- 配布ファイル: <https://files.cpctf.space/credentials-54943ad60ea5d6f6b102c1bd31524cd9452e6e1202bef16cf9e544718b2aa638.zip>

## ヒント（解放済み）

`git log --all` や `git reflog` に、履歴が残っていないでしょうか。

## Attachment

- `credentials/` (git repo: `.git/`, `main.py`)
- `credentials-54943ad60ea5d6f6b102c1bd31524cd9452e6e1202bef16cf9e544718b2aa638.zip` (original distribution)
