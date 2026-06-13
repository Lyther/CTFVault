# Tunnel? — Writeup

- Category: Forensics
- Value: 951
- Author: @Alkimor1

## Challenge

> Наш отдел ИБ зафиксировал подозрительную активность на одном из рабочих компьютеров. Похоже, злоумышленник смог вынести какие-то данные, используя нестандартный канал связи.
>
> Our information security department detected suspicious activity on one of the work computers. It appears that an attacker was able to exfiltrate some data using a non-standard communication channel.

## Recon

The packet capture contains a lot of noisy traffic, but one host stands out: `192.168.1.50` sends a short burst of DNS queries to `8.8.4.4`.

Those queries all use the same domain suffix:

```text
*.exfiltrate.kubstu-ctf.ru
```

Most labels look like random base32/base64-style chunks, but some are much more structured:

```text
v00.4b75
v01.6253
v02.5455
...
v20.7d
```

## Solve

The `vNN.xxxx` labels are ordered fragments. The `NN` part is the fragment index, and the `xxxx` part is hex-encoded text.

Sorting those fragments by index and decoding the hex gives:

```text
4b75 62 53 54 55 7b 64 30 6e 74 5f 74 72 75 35 74 5f 74 68 33 5f 64 6e 35 5f 71 75 33 72 31 33 35 5f 76 31 61 5f 68 33 78 7d
```

That decodes directly to the flag.

## Flag

```text
KubSTU{d0nt_tru5t_th3_dn5_qu3r135_v1a_h3x}
```

## Files

- [files/29_Krasnodar.pcap](files/29_Krasnodar.pcap)
- [scripts/solve.py](scripts/solve.py)
- [solution/flag.txt](solution/flag.txt)
