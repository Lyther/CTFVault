# Cartographer's Secret — Writeup

- **Category:** OSINT · **Points:** 977 · **Author:** elemental
- **Flag:** `CIT{ch3ck_th3_OSM_t4gs}`
- **Depends on:** [The Curator's Exit — Part 1](../07-the-curators-exit/writeup.md) for identifying the `vitrinefox` / Remy Beauvillier persona and [Follow the Flock](../20-follow-the-flock/writeup.md) for learning that "flock" in this chain means **Flock Safety ALPR cameras mapped on OpenStreetMap**.

## Decoding the hint

> I swear I've looked everywhere…
> Maybe I'm not looking closely enough.

Once the Part 1 trail has oriented you on the `vitrinefox` / Flock Safety / OSM ecosystem, "look more closely" is a nudge to inspect **tag-level metadata** on an OSM feature, not page content. Every OSM node/way/relation has a bag of `key=value` tags that are plaintext and publicly queryable but aren't rendered on the map tiles or visible in DeFlock's pin popups.

## Finding the node

Exactly **one** OSM node in the challenge's geographic area (Greater New Haven / West Haven, CT) carries a `flag=*` tag with a `CIT{…}` value:

```overpassql
[out:json];
node["man_made"="surveillance"]["manufacturer"="Flock Safety"]["flag"](41,-73.5,42,-72);
out tags;
```

Response:

```json
{
  "id": 13735855418,
  "lat": 41.2909719,
  "lon": -72.9636546,
  "tags": {
    "camera:type": "fixed",
    "direction": "45;90;135;0",
    "flag": "CIT{ch3ck_th3_OSM_t4gs}",
    "man_made": "surveillance",
    "manufacturer": "Flock Safety",
    "manufacturer:wikidata": "Q108485435",
    "surveillance": "public",
    "surveillance:type": "ALPR",
    "surveillance:zone": "traffic"
  }
}
```

That node is a Flock Safety ALPR pole at the edge of the University of New Haven campus (Allingtown district, West Haven, CT). Viewable directly at <https://www.openstreetmap.org/node/13735855418>.

The `flag=*` value reads literally as *"check the OSM tags"*.

## Flag

```text
CIT{ch3ck_th3_OSM_t4gs}
```

## Reproduce

```sh
curl 'https://overpass-api.de/api/interpreter?data=[out:json];node(13735855418);out%20tags;'
```

## Relationship with sibling challenges

- **Follow the Flock** (OSINT, 828 pts) does **not** use this node — its flag is `CIT{State_Street_New_Haven_CT}`, from the "smell like pizza" clue pointing at State Street in New Haven proper (Modern Apizza / NHPD Rekor ALPRs). Treating the unique `flag=`-tagged node as the answer to both challenges is the classic trap.
- **Cartographer's Secret** (this one) *is* the tagged node — read `flag=*` directly.

## Notes

- Live OSM data can change; if the `flag=*` tag disappears after a cleanup edit, recover the intent from this writeup or the changeset history of node 13735855418.
- Do **not** vandalize real OSM for CTF credit — read tags only.

## References

- [OSM node 13735855418](https://www.openstreetmap.org/node/13735855418)
- [Overpass API documentation](https://overpass-api.de/)
- [DeFlock — community ALPR map built on OSM](https://deflock.org/)
- [OSM Wiki: `surveillance:type=ALPR`](https://wiki.openstreetmap.org/wiki/Tag:surveillance:type%3DALPR)
