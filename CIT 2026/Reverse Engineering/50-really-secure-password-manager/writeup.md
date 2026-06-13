# Really Secure Password Manager — Writeup

- Category: Reverse Engineering
- Value: 992
- Author: ronnie

## Challenge

> I built this new password manager I think it should be pretty secure

## Recon

The binary is a statically linked ELF64 with symbols intact.
`getPass()` just asks for an account name, calls `generatePassword(account)`, and prints the returned string as that account's password.

`generatePassword()` is only half the story.
It deterministically builds a 16-character candidate from `std::hash(account)` and `mt19937`, then passes that candidate into `validate()`.
For the `flag` account, the raw generated candidate is just `0oOIIuVsyoYRRTXb`, so the interesting logic is entirely inside `validate()`.

`auth()` is also weaker than it looks.
It only checks whether `getlogin()` returns the hardcoded username `notronnie`.
The harder part is that `validate()` lives in the separate `RWE` segment at `0xa80000` and performs a pile of environment checks before it will return the real password.

Tracing the VM path with `gdb` shows the relevant checks:

- `getpwnam("notronnie")` must succeed.
- The passwd home directory must match `getenv("HOME")`.
- That home directory must exist and be owned by the current UID.
- `ttyname(0)` and `ttyname(1)` must resolve to the same real PTY path.
- That PTY path must exist on disk and pass a final `stat()` check.

That explains why simple auth bypasses still return `ERROR_NOT_AUTHENTICATED`.
It is not enough to flip the `authenticated` byte; the VM still wants a coherent `notronnie` user, matching `HOME`, and a real `devpts` node owned by the current user.

## Solve

The easiest solve is to let the binary run unchanged and fake only the environment-facing libc calls with `gdb`:

1. Force `authenticated = 1` right before `generatePassword()` runs.
2. Hook `getpwnam()` and return a synthetic passwd entry for `notronnie`, but use the current process UID/GID and a temp home directory.
3. Set `HOME` to that temp directory and drop `.pm_token` with the expected contents `notronnie_local_token_v1`.
4. Hook `getlogin_r()` so the VM sees `notronnie`.
5. Hook `ttyname()` so both fd `0` and fd `1` resolve to a real `/dev/pts/*` node owned by the current user.

Once those checks line up, querying the `flag` account returns the real password instead of the error string:

```text
RET=CIT{mT5zpHOlzIG3}
```

The included solver automates exactly that `gdb` setup and prints the flag.

## Flag

```text
CIT{mT5zpHOlzIG3}
```

## Files

- [scripts/solve.py](scripts/solve.py)
- [solution/flag.txt](solution/flag.txt)
