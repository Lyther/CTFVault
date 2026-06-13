# Your Car Called — Writeup

- Category: Misc
- Value: 1000
- Author: hypnos

## Challenge

> something about check engine lights
>
> `nc 23.179.17.92 5670`

## Recon

The service speaks like an `ELM327` OBD-II adapter. After the usual setup:

```text
ATZ
ATE0
```

it identifies itself as:

```text
ELM327 v1.5
ISO 15765-4 (CAN 11/500)
```

So this is a car diagnostics emulator, and the obvious thing to query is stored trouble codes with service `03`.

## Solve

Querying mode `03` returns:

```text
008
0: 43 03 03 01 04 20 01
1: 71
```

Those bytes decode cleanly to:

```text
P0301
P0420
P0171
```

That phone-number interpretation looks tempting, but it is a decoy.

The real solve is to talk to the ECU directly. Turn headers on, stay on CAN protocol `6`, set the transmit header to the engine ECU, and query a hidden DID:

```text
ATH1
ATS0
ATL0
ATSP6
ATSH7E0
22F1A5
```

That returns a multi-frame response from `7E8`:

```text
7E8 021
7E8 0: 62F1A54349547B
7E8 1: 6D795F30746833
7E8 2: 725F6334725F31
7E8 3: 735F615F63346E
7E8 4: 5F6275737D
```

Hex-decoding the payload after `62 F1 A5` gives the real flag:

```text
CIT{my_0th3r_c4r_1s_a_c4n_bus}
```

The VIN query `0902` also returns a plausible Honda VIN, which confirms the service is emulating a real car ECU, but it is not needed for the flag.

## Flag

```text
CIT{my_0th3r_c4r_1s_a_c4n_bus}
```

## Files

- [scripts/solve.py](/Users/bytedance/Documents/CTF/CIT%202026/Misc/59-your-car-called/scripts/solve.py)
- [scripts/full_dump.py](/Users/bytedance/Documents/CTF/CIT%202026/Misc/59-your-car-called/scripts/full_dump.py)
- [solution/flag.txt](/Users/bytedance/Documents/CTF/CIT%202026/Misc/59-your-car-called/solution/flag.txt)
- [other/service_dump.txt](/Users/bytedance/Documents/CTF/CIT%202026/Misc/59-your-car-called/other/service_dump.txt)
- [other/live_session.txt](/Users/bytedance/Documents/CTF/CIT%202026/Misc/59-your-car-called/other/live_session.txt)
