# Follow the Flock — Writeup

- **Category:** OSINT · **Points:** 828 · **Author:** elemental
- **Flag:** `CIT{State_Street_New_Haven_CT}`

## Decoding the description

> "Man these damn seagulls keep following me around… always in a flock, obnoxious sirens blaring. And they smell like pizza. Feels like I'm being watched everywhere I go…"

| Clue | Reading |
|---|---|
| "always in a flock" / "watched everywhere" | ALPR / surveillance camera (Flock Safety brand or generic "flock of cameras") |
| "obnoxious sirens blaring" | police-operated camera (sirens = cops) |
| "smell like pizza" | a city in CT famous for pizza style → **New Haven** ("apizza") |
| Author's published hint | "this specific city in Connecticut is known for its style of Pizza" |
| Organizer's hint | "you know you need to look for a camera. what else does the description give you?" |

So: a police ALPR camera in New Haven, on a street associated with pizza.

## Where the pizza is

The most famous New-Haven-style pizzerias all sit on a short list of streets:

| Pizzeria | Address |
|---|---|
| Frank Pepe Pizzeria Napoletana | 157 Wooster Street |
| Sally's Apizza | 237 Wooster Street |
| **Modern Apizza** | **874 State Street** |

[deflock.org](https://deflock.org/) shows New Haven Police Department ALPRs blanketing the city, including poles on **State Street** near Modern Apizza.

## Flag

```text
CIT{State_Street_New_Haven_CT}
```

## What threw us off

There is *one* OSM node in CT carrying a `flag=CIT{...}` tag — node [13735855418](https://www.openstreetmap.org/node/13735855418), a Flock Safety ALPR pole at 41.2909719, -72.9636546 on the University of New Haven campus in **West Haven**. That tag (`CIT{ch3ck_th3_OSM_t4gs}`) is the answer to the sibling challenge **Cartographer's Secret**, *not* this one. Reading "Flock" too literally and trusting only that tagged node sends you to the wrong city; the pizza clue points unambiguously at **New Haven** proper, and the "obnoxious sirens" detail confirms a police-deployed (Rekor/NHPD) camera rather than the unaffiliated UNH-area Flock pole.

## Sibling challenge

Once you've located node 13735855418, decode its OSM tags to read **`CIT{ch3ck_th3_OSM_t4gs}`** for *Cartographer's Secret*.

## Reproduce

```sh
# Confirmed-correct submission via the platform's challenge attempt API
curl 'https://ctf.cyber-cit.club/api/v1/challenges/attempt' \
  -H 'content-type: application/json' \
  -b "session=<your-session>" -H "csrf-token: <your-csrf>" \
  --data-raw '{"challenge_id":20,"submission":"CIT{State_Street_New_Haven_CT}"}'
```
