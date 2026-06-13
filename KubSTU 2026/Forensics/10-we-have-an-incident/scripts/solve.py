#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "python-evtx",
# ]
# ///

from __future__ import annotations

import pathlib
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET

from Evtx.Evtx import Evtx

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "10_We_have_an_incident.rar"

NS = {"e": "http://schemas.microsoft.com/win/2004/08/events/event"}
HR_SYSMON = (
    "HR/C/Windows/System32/winevt/logs/Microsoft-Windows-Sysmon%4Operational.evtx"
)
HR_PS = "HR/C/Windows/System32/winevt/logs/Windows PowerShell.evtx"
AD_PS = "AD/C/Windows/System32/winevt/logs/Windows PowerShell.evtx"

PRIVESC = "ESC1"
DOCUMENT = "Резюме.docm"
TOOLS = ("Certify.exe", "Rubeus.exe", "mimikatz.exe", "wlmss.exe")


def extract_members(target_dir: pathlib.Path) -> dict[str, pathlib.Path]:
    members = [HR_SYSMON, HR_PS, AD_PS]
    subprocess.run(
        ["bsdtar", "-xf", str(CHALLENGE), "-C", str(target_dir), *members],
        check=True,
    )
    return {member: target_dir / member for member in members}


def iter_events(path: pathlib.Path):
    with Evtx(str(path)) as log:
        for record in log.records():
            root = ET.fromstring(record.xml())
            ts = root.find("./e:System/e:TimeCreated", NS).attrib["SystemTime"]
            event_id = int(root.findtext("./e:System/e:EventID", namespaces=NS))
            data = {
                item.attrib.get("Name", ""): item.text or ""
                for item in root.findall("./e:EventData/e:Data", NS)
            }
            yield ts, event_id, data


def find_privesc(hr_sysmon: pathlib.Path) -> str:
    for _, event_id, data in iter_events(hr_sysmon):
        if event_id != 1:
            continue
        cmd = data.get("CommandLine", "")
        if (
            "Certify.exe" in cmd
            and "/template:VulnerableUserSAN" in cmd
            and "/altname:admin" in cmd
        ):
            return PRIVESC
    raise RuntimeError("Failed to confirm the AD CS abuse chain")


def collect_malware(hr_sysmon: pathlib.Path) -> list[str]:
    first_seen: dict[str, str] = {}
    wanted = {name.lower(): name for name in TOOLS}

    for ts, event_id, data in iter_events(hr_sysmon):
        if event_id != 1:
            continue
        event_time = data.get("UtcTime", ts)
        image = pathlib.PureWindowsPath(data.get("Image", "")).name
        cmd = data.get("CommandLine", "")
        if image == "WINWORD.EXE" and DOCUMENT in cmd:
            first_seen[DOCUMENT] = min(event_time, first_seen.get(DOCUMENT, event_time))
        if not image:
            continue
        key = image.lower()
        if key not in wanted:
            continue
        name = wanted[key]
        first_seen[name] = min(event_time, first_seen.get(name, event_time))

    expected = (DOCUMENT, *TOOLS)
    missing = [name for name in expected if name not in first_seen]
    if missing:
        raise RuntimeError(f"Missing malware timestamps for: {', '.join(missing)}")

    return [name for name, _ in sorted(first_seen.items(), key=lambda item: item[1])]


def collect_exfil(hr_ps: pathlib.Path, ad_ps: pathlib.Path) -> list[str]:
    first_seen: dict[str, str] = {}

    for ts, _, data in iter_events(hr_ps):
        command = data.get("", "")
        if (
            "ReadAllBytes" not in command
            or "TcpClient('192.168.100.54',9000)" not in command
        ):
            continue
        match = re.search(r'\$file="([^"]+)"', command)
        if not match:
            continue
        name = pathlib.PureWindowsPath(match.group(1)).name
        first_seen[name] = min(ts, first_seen.get(name, ts))

    for ts, _, data in iter_events(ad_ps):
        command = data.get("", "")
        if (
            "ReadAllBytes" not in command
            or "TcpClient('192.168.100.54',9001)" not in command
        ):
            continue
        match = re.search(r'\$file="([^"]+)"', command)
        if not match:
            continue
        name = pathlib.PureWindowsPath(match.group(1)).name
        first_seen[name] = min(ts, first_seen.get(name, ts))

    if not first_seen:
        raise RuntimeError("No exfiltration events found")

    return [name for name, _ in sorted(first_seen.items(), key=lambda item: item[1])]


def build_flag(privesc: str, malware: list[str], exfil: list[str]) -> str:
    return f"KubSTU{{{privesc}:{'_'.join(malware)}:{'_'.join(exfil)}}}"


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="kubstu-incident-") as tmpdir:
        paths = extract_members(pathlib.Path(tmpdir))
        privesc = find_privesc(paths[HR_SYSMON])
        malware = collect_malware(paths[HR_SYSMON])
        exfil = collect_exfil(paths[HR_PS], paths[AD_PS])

    print(build_flag(privesc, malware, exfil))


if __name__ == "__main__":
    main()
