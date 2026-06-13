# Not enough part 1

- ID: 4
- Category: Crypto
- Value: 100
- Solves: 355
- Type: dynamic
- Author: @ST47IC4

## Description

Во время дампа системы часть параметров оказалась повреждена: от `p` сохранились только часть бит, последние 72 бита были потеряны. Затем из восстановленных параметров был получен ключ путём хеширования секрета (ещё уцелело это, по-моему, AES-GCM?).

Формат флага: `KubSTU{...}`

---

During a system dump, some parameters were corrupted: the last 72 bits of `p` were lost. Then, from the recovered parameters, a key was derived by hashing the secret (I think it was AES-GCM?).

Flag format: `KubSTU{...}`

## Files

- `output.txt` (vendored as `files/4_output.txt`)
