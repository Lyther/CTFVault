# Nut legends - Writeup

- Category: Network
- Value: 810
- Author: @MellinBurmont
- Status: Unsolved

## Challenge

> An anomaly has been detected in the network topology. Direct access to the target node is blocked at several layers of the OSI model. You are given an entry point (PC Cooper R.) and a single artifact -- an image file. Reconstruct the access chain and capture the flag.

## Recon

The vendored file is a Packet Tracer project, not a standalone image. I decoded [14_LightA.pkt](files/14_LightA.pkt) into [14_LightA.xml](files/14_LightA.xml) and reconstructed the lab:

- `COOPER R.`: `10.10.10.10/24`, gateway `10.10.10.1`
- `Mastif_0828`: router-on-a-stick with `Gi0/0.10 = 10.10.10.1/24` and `Gi0/0.20 = 10.20.20.1/24`
- `Switch0`: VLAN 10 access on `Fa0/1`, VLAN 20 access on `Fa0/2`, trunk on `Fa0/24`
- `Server#1`: `10.20.20.100/24`

The switch also has a custom description on `Fa0/10`:

```text
Linked_by_14mB4mb00zl3r
```

On the server side:

- HTTP is enabled and `index.html` says the key is archived in `copyrights`
- `copyrights.html` contains one deliberate anomaly inside the Cisco EULA text:

```text
kubstu(end_user_license_agreement)
```

- FTP is enabled with `cisco:cisco`
- The server file trees under `c:`, `ftp:`, `tftp:`, `http:`, and `ioe:` were enumerated
- No custom file containing a flag or second-stage instruction exists outside the HTTP hint pages and the embedded images

## Image Work

The Packet Tracer XML contains two separate JPEG blobs for the same drawing:

- [wozduhan-from-pkt.jpg](other/extracted-images/wozduhan-from-pkt.jpg)
- [cluster-bg.jpg](other/extracted-images/cluster-bg.jpg)

I also extracted the stock Cisco logo:

- [cscoptlogo177x111.jpg](other/extracted-images/cscoptlogo177x111.jpg)

The Cisco logo is a normal stock image and is not the carrier.

For the background portrait, I checked:

- metadata
- `strings`
- `binwalk`
- image diffs between the two embedded JPEGs
- RGB LSB renders
- OCR-oriented thresholding and edge passes

The RGB LSB render does show a non-random pattern: six clean `8x8` white blocks in the empty background above the head. Those are preserved in:

- [lsb-r.png](other/extracted-images/lsb-r.png)
- [lsb-g.png](other/extracted-images/lsb-g.png)
- [lsb-b.png](other/extracted-images/lsb-b.png)

I could not turn those markers into a readable code, QR, or text.

## Outguess

Because the carrier is JPEG and the hint points to a key, I tested outguess-style extraction.

The only candidate that produced a plausible header on both extracted JPEGs was:

```text
copyrights
```

Both images produced the same apparent outguess header:

```text
seed: 29105
len: 5625
```

The extracted payloads are here:

- [copyrights.noec.bin](other/outguess-extract/copyrights.noec.bin)
- [cluster-copyrights.noec.bin](other/outguess-extract/cluster-copyrights.noec.bin)

I verified the patched outguess build with a local round-trip test on the same carrier type. The final `OOB` warning is benign in non-ECC mode; known plaintext still extracts correctly. So `copyrights.noec.bin` is a real second-stage artifact, not just a broken extractor artifact.

The remaining problem is that the extracted `5625`-byte blob still does not identify as anything useful:

- no file magic
- no meaningful strings
- no clean raw-image interpretation
- no obvious XOR or RC4 recovery with the topology-derived tokens

I also tested the possibility that the payload was embedded with outguess ECC. That path did not produce a defensible recovery in this environment, and the challenge provides no additional clue for a next transform or key.

## Status

This is where I stopped.

There is enough evidence for a real first stage:

- Packet Tracer topology decoded
- HTTP hint found
- `copyrights` confirmed as the only plausible stego key
- second-stage blob extracted from both embedded JPEG variants

But there is no solid clue for what to do with the extracted blob next. At this point the challenge stops being a solve and turns into blind format/key guessing.

## Flag

```text
UNSOLVED
```

## Files

- [14_LightA.xml](files/14_LightA.xml)
- [wozduhan-from-pkt.jpg](other/extracted-images/wozduhan-from-pkt.jpg)
- [cluster-bg.jpg](other/extracted-images/cluster-bg.jpg)
- [lsb-r.png](other/extracted-images/lsb-r.png)
- [lsb-g.png](other/extracted-images/lsb-g.png)
- [lsb-b.png](other/extracted-images/lsb-b.png)
- [copyrights.noec.bin](other/outguess-extract/copyrights.noec.bin)
- [cluster-copyrights.noec.bin](other/outguess-extract/cluster-copyrights.noec.bin)
