# Mobile Waf — Writeup

- Category: Misc
- Value: 530
- Author: t.me/thankspluxury

## Challenge

> На наш вуз в последнее время очень много запросов поступает, и мне кажется, что они подозрительные.
>
> Подключаемся к сервису по `nc` и видим:
>
> ```text
> === WAF Challenge ===
> You need to correctly classify 100 HTTP requests as malicious or safe.
> For each request, respond with:
>   - 'Block' if the request is malicious
>   - 'Allow' if the request is safe
> Type 'Start' to begin:
> ```
>
> **Задача.** Классифицировать 100 HTTP-запросов подряд без ошибок.
>
> Формат флага: `KubSTU(...)`

## Recon

Сервис действительно отдаёт 100 HTTP-запросов подряд и ждёт ответ `Block` или `Allow`.
Я собрал живые примеры и проверил их напрямую через много новых подключений.

Быстро стало видно, что задача устроена не как нормальная WAF-сигнатурная классификация, а как ручная угадайка по внутренней логике автора.

## Solve

Удалось восстановить много правил и добраться до `79/100`, но задача оказалась плохо спроектированной для честного black-box решения.

Примеры противоречивых кейсов:

- `GET /api/test?id=1' OR '1'='1` -> `SAFE`
- `GET /admin?id=1' OR '1'='1` -> `MALICIOUS`
- `GET /api/data?script=<script>alert('test')</script>` -> `SAFE`
- `GET /page?name=<script>alert('XSS')</script>` -> `MALICIOUS`
- `GET /api/load?file=../../config.json` -> `SAFE`
- `GET /files/....//....//etc/passwd` -> `MALICIOUS`
- `POST /api/query` with parameterized body
  `{"sql":"SELECT * FROM users WHERE id = ?","params":[123]}` -> `SAFE`
- `POST /api/query` with raw injected SQL
  `{"query":"SELECT * FROM users WHERE id = 1' OR '1'='1","type":"sql"}` -> `MALICIOUS`

То есть сервис местами оценивает не сам запрос, а придуманную автором бизнес-логику эндпоинта.
Без исходников или полного датасета это превращается в перебор редких исключений, а не в решение задачи.

На этом я остановился: всё разумное, что можно было сделать как внешний участник, уже сделано.

## Flag

```text
TBD
```
