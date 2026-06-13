# CapyAgro Crop Rescue — local artifacts

```text
solution/
├─ flag.txt                    KubSTU(Sav3d_th3_CapyArg0S3ct0r)
├─ exploit.sh                  end-to-end reproducer (registers, finds CapyAgro
│                              sector id from /capyagro, IDORs the adjust API)
└─ artifacts/
   ├─ index.html               public landing page
   ├─ login.html / register.html
   ├─ dashboard.html           user's own sectors (logged-in capture)
   ├─ capyagro.html            read-only monitoring page that exposes the
   │                           target CapyAgro-owned sector id
   ├─ static_config.js         leaks `X-API-Key: test_key_123` and lists endpoints
   ├─ static_style.css
   ├─ api_sector.json          GET /api/sector/<id> response (is_capyagro=true,is_own=false)
   ├─ api_capyagro_sectors.json
   ├─ api_adjust_response.json POST /api/sector/<id>/adjust → contains the flag
   └─ test_user.txt            the throwaway account used during capture
```

## TL;DR vulnerability

`POST /api/sector/<id>/adjust` skips the ownership check; any logged-in user with the
public `X-API-Key: test_key_123` (advertised in `/static/config.js`) can set
`{temp,humidity}` on a sector flagged `is_capyagro: true, is_own: false`. When all such
sectors are returned to the normal range the server replies with the flag.
