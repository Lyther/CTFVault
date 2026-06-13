# Capybara Secret — Writeup

- Category: Stego
- Value: 100
- Author: @van_1pi

## Challenge

> Капибара-хранитель спрятала послание в своём портрете. Говорят, что секрет виден лишь тем, кто умеет смотреть глубже поверхности. Найдите скрытое сообщение.
>
> The guardian capybara hid a message in her portrait. They say the secret is visible only to those who can look beyond the surface. Find the hidden message.

## Recon

The JPEG itself has no appended files or obvious pixel-layer trickery, so the first useful place to look is metadata.

`exiftool` shows an `XP Comment` field:

```text
XhoFGH{J0J_1aperq1oyr_pnclon6n}
```

That string already has the right shape for a flag but does not start with `KubSTU`, so it is likely lightly encoded.

## Solve

Applying ROT13 to the `XP Comment` value gives:

```text
KubSTU{W0W_1ncred1ble_capyba6a}
```

That is the final flag.

## Flag

```text
KubSTU{W0W_1ncred1ble_capyba6a}
```

## Files

- [49_challenge.jpg](files/49_challenge.jpg)
- [solve.py](scripts/solve.py)
