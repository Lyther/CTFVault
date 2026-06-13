# Mobile Waf

- ID: 13
- Category: Misc
- Value: 530
- Solves: 218
- Type: dynamic
- Author: t.me/thankspluxury

## Description

На наш вуз в последнее время очень много запросов поступает, и мне кажется, что они подозрительные. Подключаемся к сервису по `nc` и видим:

```
=== WAF Challenge ===
You need to correctly classify 100 HTTP requests as malicious or safe.
For each request, respond with:
  - 'Block' if the request is malicious
  - 'Allow' if the request is safe
Type 'Start' to begin:
```

**Задача.** Классифицировать 100 HTTP-запросов подряд без ошибок.

Формат флага: `KubSTU(...)`

nc 109.69.22.21:1337
nc 5.35.82.129:1337

---

Our university has been receiving a lot of requests lately, and I think they look suspicious. We connect to the service via `nc` and see:

```
=== WAF Challenge ===
You need to correctly classify 100 HTTP requests as malicious or safe.
For each request, respond with:
  - 'Block' if the request is malicious
  - 'Allow' if the request is safe
Type 'Start' to begin:
```

**Task.** Classify 100 HTTP requests in a row without errors.

Flag format: `KubSTU(...)`

nc 109.69.22.21:1337
nc 5.35.82.129:1337
