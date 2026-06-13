# MCPocalypse — local artifacts

```text
solution/
├─ flag.txt                          KubSTU(mcp_h4s_n0_4uth_4nd_1_l0v3_1t)
├─ exploit.py                        end-to-end reproducer:
│                                    1) GET /api/backup, decrypt with leaked key,
│                                       parse `Node.Secret` from app.ini
│                                    2) open SSE on /mcp with X-Node-Secret,
│                                       grab sessionId
│                                    3) JSON-RPC `tools/call restart_nginx`
│                                       on /mcp_message — flag returned
└─ artifacts/
   ├─ capytech_homepage.html              CapyTech static front page (155.212.186.115:8888)
   ├─ nginx_ui_index.html                 Nginx UI index (212.8.228.176:9000)
   ├─ index-FsG_frCq.js                   Nginx UI client bundle (~2 MB)
   ├─ api_backup_full.bin                 raw response (headers + zip body)
   ├─ api_backup.headers                  decoded response headers
   ├─ api_backup.zip                      outer (encrypted) backup zip
   ├─ X-Backup-Security.txt               base64 AES-256-CBC key:iv from header
   ├─ decrypted/
   │   ├─ hash_info.txt                   plaintext manifest (timestamp, version 2.3.1)
   │   ├─ nginx-ui.zip                    plaintext nginx-ui dump (app.ini, database.db)
   │   └─ nginx.zip                       plaintext nginx config dump
   └─ decrypted_source/
       ├─ nginx-ui/
       │   ├─ app.ini                     ←— leaks JwtSecret + Node.Secret
       │   └─ database.db                 SQLite — admin user, hashed password, etc.
       └─ nginx/                          full /etc/nginx tree as backed up
           ├─ app.ini                     redundant copy with `RestartCmd = cat /flag.txt`
           ├─ nginx.conf
           ├─ conf.d/                     active server blocks (capyflag.conf, …)
           ├─ etc/nginx-ui/app.ini        same secret leak from inside the snapshot
           └─ tmp/readflag.sh             helper script the challenge author ships
```

## TL;DR vulnerabilities

1. **Unauth backup leak.** `GET /api/backup` returns the encrypted backup AND
   includes the per-backup AES key+IV in the response header
   `X-Backup-Security: <key_b64>:<iv_b64>`. AES-256-CBC + PKCS#7. Decrypt
   `nginx-ui.zip` and `nginx.zip` from the outer zip → leak `app.ini` →
   recover `Node.Secret` and confirm `[nginx] RestartCmd = cat /flag.txt`.

2. **Node-secret auth bypass.** `internal/middleware/middleware.go::AuthRequired()`
   returns `c.Next()` whenever the request carries a non-empty
   `X-Node-Secret` matching `settings.NodeSettings.Secret`. With the secret
   from step 1 we walk straight past auth. Open SSE on `/mcp` (which then
   issues a sessionId), POST `initialize` + `notifications/initialized` +
   `tools/call name=restart_nginx` to `/mcp_message?sessionId=…`. The
   `RestartCmd` shell-out runs `cat /flag.txt` and the result comes back over
   the SSE channel.

   (Side note: in this Nginx UI build `/mcp_message` is mounted with
   `IPWhiteList()` only — *no* `AuthRequired()` — but you still need a live
   sessionId, which only `/mcp` hands out. The backup leak gives us the
   secret needed to open `/mcp`.)
