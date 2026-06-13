# We have an incident!

- ID: 10
- Category: Forensics
- Value: 1000
- Solves: 2
- Type: dynamic
- Author: @Alkimor1

## Description

У нас в компании, кажется, произошёл инцидент, пока ничего не ясно, мы изолировали определённые машины от греха подальше. Команда реагирования плотно сотрудничает с вирусными аналитиками. Чтобы облегчить себе работу, нужно предоставить им ВПО, которые вы должны будете найти. Также есть подозрения, что производилась эксфильтрация. Выясните, что же произошло.

**Формат флага:** `KubSTU{Уязвимость элемента/атака,которая привела к эскалации привилегий:Список ВПО, включая их расширения:Данные, которые эксфильтровали}`

**Внимание!** Списки указывайте в порядке их временных меток запуска с учётом регистра, от раннего к позднему. В случае эксфильтрации также.

**Пример:** `KubSTU{polkit:PwnKit.exe_revershell.exe_WannaCry.exe:Конфданные.doc_users.db}`

---

It seems an incident has occurred at our company. Nothing is clear yet — we've isolated certain machines to be safe. The response team is working closely with virus analysts. To make their job easier, you need to provide them with the malware that you must find. There are also suspicions that data exfiltration took place. Find out what happened.

**Flag format:** `KubSTU{Vulnerability of the element/attack that led to privilege escalation:List of malware including their extensions:Exfiltrated data}`

**Note!** List items in chronological order of their launch timestamps (case-sensitive), from earliest to latest. Same applies to exfiltration.

**Example:** `KubSTU{polkit:PwnKit.exe_revershell.exe_WannaCry.exe:ConfidentialData.doc_users.db}`

## Files

- `We_have_an_incident.rar` (vendored as `files/10_We_have_an_incident.rar`)
