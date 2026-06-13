# You gotta run, run, run, run, run — Writeup

- Category: Forensics
- Value: 990
- Author: boom

## Challenge

> Waiter, waiter! More persistence mechanisms please!!
>
> Yet another persistence mechanism seems to have been setup. It's funny because I remember the user saying everytime they logged into their system, something just felt odd when they'd see some sort of black box flash on their screen. There must be a name associated with what this is..
>
> **SHA1:** `cc0060d01e8dc3fe69a8ca888c203bc9e57959e1`
>
> **FLAG FORMAT:** `CIT{XXXXXXXXXXXX}`

## Recon

The attachment is a Windows user hive: `ntuser.dat`.
The hint about a black box flashing on logon points straight at user logon persistence:

- `Run`
- `RunOnce`
- `StartupApproved`

Using a registry parser on the hive, the interesting key is:

```text
SOFTWARE\Microsoft\Windows\CurrentVersion\Run
```

## Solve

Dumping that key gives:

```text
OneDrive     "C:\Users\kurt\AppData\Local\Microsoft\OneDrive\OneDrive.exe" /background
AzureTenant  "C:\Users\kurt\AppData\Roaming\fj3493.exe"
```

`OneDrive` is normal.
`AzureTenant` is the malicious-looking autorun value, and that value name is what the challenge asks for.

Wrap it in the flag format:

```text
CIT{AzureTenant}
```

## Flag

```text
CIT{AzureTenant}
```

## Files

- [challenge.dat](files/challenge.dat)
- [solve.py](scripts/solve.py)
- [run-key.txt](other/run-key.txt)
- [strings-hits.txt](other/strings-hits.txt)
