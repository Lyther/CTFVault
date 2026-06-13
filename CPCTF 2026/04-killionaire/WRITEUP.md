# Killionaire

**Idea:** Betting game. Only `bet > coins` is rejected; negative `bet` is accepted. On a failed round the code does `coins -= bet`, so a negative bet turns into `coins += |bet|`.

**Solve:** One failed round with a large negative bet pushes `coins` past 1000 immediately (e.g. `printf '%d\n' -999999 | nc <host> <port>`).

**Flag:** `CPCTF{n3g4t1v3_v41u3_1s_m0re_p0w3rfu1_th4n_p0s1tiv3_va1u3}`
