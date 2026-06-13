# "Your Car Called" — complete probe notes

## Challenge
- API: `https://ctf.cyber-cit.club/api/v1/challenges/59`
- Name: `Your Car Called`
- Category / Value: Misc, 1000 pts (dynamic)
- Author: `hypnos`
- Description: *"something about check engine lights"*
- Files / hints / tags: **none**
- Conn: `nc 23.179.17.92 5670`

## Service identification
- Ircama-style ELM327 v1.5 emulator, ISO 15765-4 CAN 11/500 (`ATDPN`=`A6`)
- Default Ircama VIN is `WP0ZZZ99ZTS390000` (Porsche) — this instance is re-seeded with Honda data, so the VIN/DTCs were chosen on purpose.

## AT commands
| cmd | response | standard meaning |
|-----|----------|------------------|
| `ATI` | `ELM327 v1.5` | identifier |
| `AT@1` | `ELM327 v1.5` | device description |
| `AT@2` / `AT@3` | `?` | custom id slots (empty) |
| `ATDP` | `ISO 15765-4 (CAN 11/500)` | display protocol |
| `ATDPN` | `A6` | protocol number (Auto, protocol 6) |
| `ATRV` | `14.2V` | read battery voltage |
| `ATBI` / `ATWS` | `?` | not implemented |
| `ATST` | `OK` | set timeout |
| `ATH1` / `ATS1` / `ATL1` / `ATCAF1` | `OK` | formatting |
| `ATMA` | `?` | not implemented (important: can't monitor all) |

## Responding OBD-II data
Every response comes from CAN ID `7E8` (engine ECU, standard).

| req | response | decoded |
|-----|----------|---------|
| `0100` | `41 00 BE 3F A8 13` | supported 01-20 bitmap claims 01,03,04,05,06,07,0B,0C,0D,0E,0F,10,11,13,15,1C,1F,20 — but only 05/0C/0D/11 actually respond |
| `0105` | `41 05 5C` | coolant 92-40 = **52 °C** |
| `010C` | `41 0C 1B 20` | RPM 0x1B20 / 4 = **1736** |
| `010D` | `41 0D 52` | speed = **82 km/h** |
| `0111` | `41 11 4D` | throttle 0x4D / 2.55 ≈ **30 %** |
| `0120` | `41 20 80 00 00 01` | supported 21-40 bitmap claims PID 21 and 40 — neither actually responds |
| `03` | `43 03 03 01 04 20 01 71` | 3 DTCs: **P0301, P0420, P0171** |
| `04` | `44` | clear DTCs OK |
| `0902` | `49 02 01 ` + `31 48 47 43 4D 38 32 36 33 33 41 30 30 34 33 35 32` | VIN = **`1HGCM82633A004352`** (2003 Honda Accord LX, Marysville Ohio) |

## Dead ends (all return NO DATA / `?`)
- Mode 02 freeze frame (every `XX YY` combo)
- Mode 05, 06, 07, 08, 0A (permanent DTCs)
- Mode 09 PIDs 00, 01, 03, 04, 06, 08, 0A, 0B, 0C, 0D, 0E, 0F
- Mode 19 (UDS readDTCInformation) all subfunctions
- Mode 22 (UDS ReadDataByIdentifier) — F190, F18C, F17C, F18B, F195, F197, F199, F1A0, plus many others
- Mode 10 (UDS sessionControl), 27 (SecurityAccess), 2E (WriteDataById), 31 (routineControl), 3E (TesterPresent)
- Vendor modes 0B, 0C, 0D, 0E, 0F, 21, 23…30
- Header manipulation (`ATSH` 7E0..7EF / 7DF / 7C0 / 750 / 710; `ATCRA` similarly) — every header mirrors the same replies
- `ATMA` (monitor all frames) not implemented — can't sniff idle CAN traffic

## Rejected flag attempts
- Phone number: `301-420-0171` / `3014200171` / `(301) 420-0171` / `301.420.0171` / `301_420_0171` / `+1-301-420-0171` / `13014200171` / `1-301-420-0171`
- DTC strings: `P0301_P0420_P0171` / `P0301-P0420-P0171` / `P0301P0420P0171` / `P0171_P0301_P0420` / `0301_0420_0171` / `030104200171`
- VIN: `1HGCM82633A004352` / `HGCM82633A004352` / `004352` / `4352`
- Concepts: `check_engine_light` / `Check_Engine_Light` / `check-engine-light` / `malfunction_indicator_lamp` / `MIL` / `ch3ck_3ng1n3` / `ch3ck_3ng1n3_l1ght` / `cylinder_1_misfire` / `misfire_catalyst_lean` / `lean_misfire`
- Sensor values: `52_1736_82_30` / `5217368230`
- Meta: `hypnos` / `ELM327`

## Observations worth another look
- The 4 *actually responding* data PIDs are `0x05, 0x0C, 0x0D, 0x11`. As decimal: 5, 12, 13, 17. First 3 letters-of-alphabet: **E, L, M** — matches `ELM` in `ELM327`. PID 17 = `Q` breaks the pattern (but may be a red herring or secondary signal).
- Raw PID data bytes concatenated (`5C 1B 20 52 4D`) include two printable ASCII letters: **`R`** (0x52) and **`M`** (0x4D), plus `\` (0x5C), `ESC` (0x1B), space (0x20). Letters only = `RM`.
- VIN check digit validates; nothing suspicious about the VIN structurally.

## Reproducibility
- [scripts/full_dump.py](../scripts/full_dump.py) — basic probe
- [scripts/solve.py](../scripts/solve.py) — pre-existing script (parses DTCs -> emits `CIT{301-420-0171}` which was rejected)
- [other/service_dump.txt](service_dump.txt) — probe output
- [other/service_dump_headers_on.txt](service_dump_headers_on.txt) — same probe with `ATH1 ATS1 ATL1 ATCAF1`
- [other/live_session.txt](live_session.txt) — manual session log
