# Yannella — Writeup

- Category: OSINT
- Value: 949 pts
- Author: by **ronnie**

## Challenge

> This challenge is dedicated to our late friend Anthony Yannella.
>
> Find the organization that gave Anthony an acknowledgment for responsibly disclosing a security vulnerability.
>
> Flag format:
> `CIT{name_of_organization}`

## Recon

Searching Anthony Yannella together with vulnerability disclosure acknowledgments leads to the Department of Energy Responsible Disclosure acknowledgments page.

The saved text version in [other/doe-acknowledgments.txt](other/doe-acknowledgments.txt) is the useful artifact because the direct HTML page is Cloudflare-protected. That text contains both the organization sentence and Anthony Yannella's name in the acknowledgments list.

## Solve

The page states that the listed researchers disclosed valid vulnerabilities to the `Department of Energy`, and `Anthony Yannella` appears in that list. Converting the organization name into the challenge's underscore format gives the flag below.

## Flag

```text
CIT{Department_of_Energy}
```

## Files

- [challenge.md](challenge.md)
- [README.md](README.md)
- [other/challenge-api.json](other/challenge-api.json)
- [other/doe-acknowledgments.html](other/doe-acknowledgments.html)
- [other/doe-acknowledgments.txt](other/doe-acknowledgments.txt)
- [other/evidence.md](other/evidence.md)
- [scripts/fetch-live-artifacts.sh](scripts/fetch-live-artifacts.sh)
- [scripts/solve.py](scripts/solve.py)
- [solution/flag.txt](solution/flag.txt)
