# The Battle of the Strongest — local artifacts

```text
solution/
├─ flag.txt                    KubSTU(Y0u_ar3_champ10n)
├─ exploit.sh                  registers, places a bet, drives the global
│                              like counter to that bet, waits out the round,
│                              prints the win banner from /dashboard
└─ artifacts/
   ├─ login.html               /login UI (register + login forms, JS)
   ├─ home.html                logged-in /
   ├─ dashboard.html           bet form + history table
   ├─ static_style.css
   ├─ api_timer.json           round + remaining seconds
   ├─ api_likes.json           current global like count
   ├─ api_user_liked.json
   ├─ api_music_list.json
   └─ test_user.txt
```

## TL;DR vulnerability

`/api/like` and `/api/unlike` are *per call*, not per user — one account can drive
the global like counter to any value before the round-end check. Place a bet of N,
hammer like N times, win → `/dashboard` renders the flag inside `.flag-box`.
