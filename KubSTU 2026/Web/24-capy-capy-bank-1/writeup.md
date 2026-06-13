# Writeup: CAPY-CAPY Bank 1

## Flag

`KubSTU{1d0r_b4nk4_d4l_d0stup_k_chuzh1m_sch3t4m}`

## TL;DR

Two distinct cookies, **same** secret (`facetoface`):

- `access_token_cookie` — Flask‑JWT‑Extended HS256, payload chooses the user via
  `sub`. Crackable from rockyou in seconds.
- `session` — Flask itsdangerous-signed JSON; the bank stores the **list of
  valid transaction signatures** server‑side as `pending_signatures` *inside
  this very cookie*. So the "одноразовая криптоподпись" the bank asks for is
  just a key in a dict the user signs and gives back to itself.

Forge JWT for `mgalankov@4274` (user_id 4) and forge a `session` whose
`pending_signatures` already contains the signature you're about to submit →
PIN check is fully bypassed. Buy the `Флаг от CTF задания` from `/flag_shop`
with a fresh offer-token from the Telegram bot, and the bot DMs you the flag.

## Recon

```text
http://5.35.88.34/        Flask / Werkzeug 2.3.7 / Python 3.9.25
/login                    POST {username, password}     → access_token_cookie (JWT HS256)
/register                 POST … → assigns username "<initial><translit_surname>@<4 random digits>"
/dashboard                shows balance, ACC<user_id>, recent tx, links to:
                          /transfer  /partners  /pending_transactions
/partners                 3 cards; "Флаг в каждый дом" is locked behind CAPY+
/flag_shop                CAPY+ only → POST /buy_flag {product_id, token}
/transfer                 step 1: POST {to_account, amount, description}
                          step 2: POST /api/get_signature {pin_code, …}
                                  → {date, time, timestamp, signature(16 hex)}
                          step 3: POST /transfer with the four transaction_*
                                  fields → /receipt/<id>
                          OR     POST {skip_pin: 1, …} → /pending_transactions
                                  → /verify_transaction/<id> needs the 16-hex sig
```

Two important observations from playing with the signature endpoint:

1. **Signatures are deterministic per timestamp regardless of amount /
   recipient / description.** Same `timestamp` → identical `signature`.
2. **Receipts show the same offer-token reused multiple times.**

These two together feel like the real bug, but the actual hole is uglier:
the signature is just a Flask-session lookup key.

## Crack #1 — JWT secret (`access_token_cookie`)

```sh
echo "$JWT" > /tmp/jwt.hash
john --format=HMAC-SHA256 --wordlist=/tmp/rockyou.txt /tmp/jwt.hash
# facetoface (?)
```

Decoded payload:

```json
{"fresh":false, "iat":…, "jti":…, "type":"access",
 "sub":"23816", "nbf":…, "exp":…,
 "username":"osidorov@3170"}
```

Forge `sub:"4"` and you're inside `mgalankov@4274` (ACC004, balance ≈ 1 373 810 ₽,
ten existing FLAG_SHOP purchases). But every transfer still wants a
server-issued signature, and Mikhail's PIN is unknown.

## Crack #2 — Flask `SECRET_KEY` (the `session` cookie)

```sh
flask-unsign --decode --cookie '<session>'
# {'pending_signatures': {}}
flask-unsign --unsign --cookie '<session>' --wordlist /tmp/rockyou.txt --no-literal-eval
# [+] Found secret key after 186112 attempts
# b'facetoface'
```

After calling `/api/get_signature` once, the cookie expands to:

```json
{
  "pending_signatures": {
    "6df96de1378327cd": {
      "amount": "1",
      "description": "",
      "expires_at": 1777748286,
      "issued_at":  1777747986,
      "timestamp":  1777747986,
      "to_account": "ACC100",
      "user_id":    23816
    }
  }
}
```

So the "cryptographic signature" the bank verifies is **just a key in a JSON
dict that lives entirely in the user-controlled cookie**. We resign the
cookie ourselves with whatever entry we want, then submit `/transfer` with
the matching `transaction_signature` — the lookup hits, the PIN check is
never invoked.

## Exploit

1. Get a fresh offer-token from `@flagi_and_bagi_for_kubstubot`
   (`/start` → `/token`).
2. Run `solution/exploit.sh <offer_token>` — it forges the JWT + session,
   submits the buy, and prints the success flash.
3. Send `/purchases` to the same Telegram bot — the bot DMs the flag string.

Why it works: `user_id` inside the forged session entry is `4`, which matches
Mikhail (forged JWT `sub:"4"`); `to_account: "FLAG_SHOP"` and
`amount: "1000.0"` match what the buy is debiting; the offer-token is the
fresh one from the bot so FLAG_SHOP issues a flag tied to the buyer's
Telegram chat (you).

## Story → bug mapping

The "перевод, которого Михаил не делал" in the brief is exactly this: an
attacker who never knew Mikhail's password, PIN or one-time signature debits
his account by:

- forging Mikhail's JWT (sub=4) — same `facetoface` secret as the cookie,
- forging a Flask session that pre-populates the "issued signatures" dict,
  bypassing both `/api/get_signature` and the PIN check entirely,
- submitting `/transfer` whose body matches the forged dict entry.

Flag confirms it: `KubSTU{1d0r_b4nk4_d4l_d0stup_k_chuzh1m_sch3t4m}` —
*"IDOR в банке дал доступ к чужим счетам."*
