# Janken Master (Crypto, Nzt3)

**Flag:** `CPCTF{M45TER_of_riGGed_d1Ce}`

## Setup

- You pick a seed (int). Server does `seed ^= 0x1234567890abcdef1234567890abcdef` and feeds it to **Xoroshiro128+**.
- 99 NPCs each play `rng.next() % 3` (0=Rock, 1=Scissors, 2=Paper).
- You pick a hand. You get the flag **only if you are the *sole* winner** — i.e. the field contains exactly two distinct hands, yours beats theirs, and **no NPC shares your hand**.

## The bug

Xoroshiro128+ has a classic degenerate state: **state `[0, 0]` is an absorbing fixed point.** Every step outputs `0`, and the state never escapes.

Give the seed that XORs to zero:

```python
seed_input = 0x1234567890abcdef1234567890abcdef
```

After `seed ^= const`, the internal `s = [0, 0]`, so every one of the 99 `rng.next()` calls returns `0`, and `0 % 3 = 0`. All 99 NPCs throw **Rock**.

Now pick **Paper (2)**: Paper beats Rock, no NPC shares your hand → sole winner.

## Exploit

```bash
python3 -c 'print(0x1234567890abcdef1234567890abcdef); print(2)' \
  | nc 133.88.122.244 32212
```

```text
NPC hands: Rock=99, Scissors=0, Paper=0
Congratulations! You are the SOLE winner!
Here is your reward: CPCTF{M45TER_of_riGGed_d1Ce}
```
