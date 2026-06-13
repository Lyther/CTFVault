# IRIS OUT

The unlocked hint is the whole point of this one: the filming details became a topic on X/Twitter, so the practical solve path is to search for posts identifying the location from the broadcast.

Those posts narrow the stage to the closed KK line area around Yurakucho. The useful matches are the witness photos and screenshots mentioning the stretch near `有楽町イトシア`, `東京交通会館`, and especially the `西銀座` side. In the final frame, the large louvered wall on the right and the surrounding road geometry line up with that block much better than the broader "somewhere on KK line" guess.

Once the location is pinned to that spot, the required output precision is low: convert the center position of the white circular stage to decimal latitude/longitude, multiply by `1000`, and round.

That gives:

```text
latitude  = 35.674... -> 35674
longitude = 139.765... -> 139765
```

So the flag is:

```text
CPCTF{35674_139765}
```

Flag:

```text
CPCTF{35674_139765}
```
