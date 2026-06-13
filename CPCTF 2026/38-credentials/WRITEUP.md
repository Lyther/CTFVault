# credentials

The important mistake is that the distributed archive still contains the entire `.git` directory.

The author ran:

```bash
git filter-branch --index-filter "git rm -rf --cached --ignore-unmatch flag.txt" --prune-empty -- --all
```

but that does **not** guarantee that old objects disappear from the copied repository. In this archive, the rewritten branch exists, but the original commits are still present as loose objects and are also visible in the reflog:

```text
1b9465c initial commit
725b1cf delete flag from repository
ba5b001 filter-branch: rewrite
```

`git log --all` only shows the rewritten history, but the original commit object `1b9465c...` still exists. Its tree still contains `flag.txt`:

```text
$ git ls-tree -r 1b9465c
100644 blob 69bc24f565542f9064d1e28043419b746c00cd4b    flag.txt
100644 blob 5d3828624c60f4d94ab69499f08461f4bd4253f9    main.py
```

So we can read the blob directly:

```text
$ git cat-file -p 69bc24f565542f9064d1e28043419b746c00cd4b
CPCTF{n3ver_c0mmit_y0ur_cr3dential5}
```

Flag:

```text
CPCTF{n3ver_c0mmit_y0ur_cr3dential5}
```
