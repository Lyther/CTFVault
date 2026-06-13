# Wingstop 2

- ID: 38
- Category: Fullpwn
- Value: 1000
- Author: bootstrap

## Status

- **Service down / environment removed before we could finish the chain.**
- RCE as `wingstop\bob` verified via CVE-2025-47812; `SeImpersonatePrivilege` enabled; GodPotato-ready `gp.b64` already planted in `C:\Users\Public` by a prior solver.
- Escalation chain staged in [scripts/w2_watch.py](scripts/w2_watch.py); if the instance is restored it'll drop the flag into `/tmp/w2_out/05_*` without further interaction.
- See [writeup.md](writeup.md) for full details.

## Description

Find flag2. Good luck!

`23.179.17.68`

> **Disclaimer**
>
> By accessing this challenge environment, you agree to use the provided instance solely for the purpose of solving the intended CTF challenge.
>
> Any activity outside the scope of the challenge is strictly prohibited, including but not limited to:
>
> - Using the system for personal projects or unrelated testing
> - Hosting services, files, or external content
> - Attempting to pivot, scan, or attack external systems
> - Establishing persistence, backdoors, or unauthorized access mechanisms other than those required to complete the challenge
> - Deploying or participating in botnets, command-and-control infrastructure, or any form of distributed attack tooling
> - Running cryptocurrency miners or using system resources for unauthorized computation
> - Interfering with the availability, performance, or integrity of the instance
>
> This is a shared, limited resource. Actions that degrade performance, abuse compute resources, or disrupt fair play may result in immediate disqualification.
>
> We reserve the right to monitor activity, revoke access, and reset or terminate the instance at any time in response to misuse.
