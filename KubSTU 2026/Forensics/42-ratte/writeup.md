# Ratte — Writeup

- Category: Forensics
- Value: 958
- Author: @Alkimor1

## Challenge

> Вы — специалист по расследованию инцидентов. В вашу компанию поступил дамп сетевого трафика (pcap-файл), перехваченный с одного из сегментов корпоративной сети в момент подозрительной активности. Проанализируйте, что же тут не так
>
> You are an incident response specialist. Your company received a network traffic dump (pcap file) intercepted from one of the corporate network segments during suspicious activity. Analyze what's wrong here.

## Recon

The capture is full of noisy one-packet HTTP, DNS, FTP, SSH, and TLS traffic between `10.0.0.5` and several hosts. Most of that traffic does not even form real sessions: it is just standalone packets with fake-looking requests such as `GET /index.html` and DNS queries for `google.com`.

The actual outlier is a short one-way stream:

```text
10.0.0.5:49152 -> 10.0.0.15:1337
```

It contains 21 small packets. The first payload is:

```text
deadbeef42
```

The trailing byte `42` is the XOR key used for the rest of the channel.

## Solve

Every following packet has this layout:

```text
cc ?? len data...
```

The third byte is the payload length, and the remaining bytes are encrypted with XOR `0x42`.

Example:

```text
cc 53 02 09 37  ->  09 37 ^ 42 42  ->  4b 75  ->  "Ku"
```

Decoding all frames on `1337/tcp` after the `deadbeef42` marker gives the full flag.

## Flag

```text
KubSTU{n0_m0r3_gr3pp1ng_1n_th3_d4rk_v2}
```

## Files

- [files/42_Ratte.pcap](files/42_Ratte.pcap)
- [scripts/solve.py](scripts/solve.py)
- [solution/flag.txt](solution/flag.txt)
