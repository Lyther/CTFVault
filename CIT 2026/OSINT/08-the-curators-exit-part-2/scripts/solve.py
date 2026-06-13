#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Curator's Exit Part 2 — UNSOLVED.

The previous guess CIT{ch3ck_th3_OSM_t4gs} (from the OSM node's `flag=*`
tag and changeset comment) is the answer to the SIBLING challenge
Cartographer's Secret (id 21), not this one. Leaving this script as a
reproducer for that OSM trail + a tally of everything already tried.
"""

from __future__ import annotations
import pathlib

HERE = pathlib.Path(__file__).resolve().parent.parent
OSM_HISTORY = HERE / "other" / "osm_node_13735855418_history.xml"
CHANGESETS = HERE / "other" / "osm_vitrinefox_changesets.xml"

REJECTED_FLAGS = [
    # OSM / decoy
    "CIT{ch3ck_th3_OSM_t4gs}",      # = Cartographer's Secret (#21)
    "CIT{N0t_ev3ryth1ng_i$_s3cur3}",  # decoy PDF content
    # Location guesses from reverse-image of tweet photo → Anchiano
    "CIT{Anchiano}", "CIT{Vinci}", "CIT{Vinci_Italy}", "CIT{Vinci_Tuscany}",
    "CIT{Tuscany}", "CIT{Anchiano_Italy}", "CIT{Montalbano}",
    "CIT{Casa_Natale_di_Leonardo}",
    "CIT{Casa_Natale_di_Leonardo_da_Vinci}",
    "CIT{Casa-Natale-di-Leonardo-da-Vinci}",
    "CIT{casa_natale_di_leonardo_da_vinci}",
    "CIT{Casa_Natale_Leonardo}",
    "CIT{Leonardo_da_Vinci}", "CIT{Birthplace_of_Leonardo}",
    "CIT{Biblioteca_Leonardiana}", "CIT{Museo_Leonardiano}",
    # Mona Lisa theft parallel
    "CIT{Vincenzo_Peruggia}", "CIT{Peruggia}", "CIT{Mona_Lisa}",
]


def main() -> None:
    print("UNSOLVED. Rejected candidates:")
    for f in REJECTED_FLAGS:
        print(" -", f)
    print()
    print("Background artefacts in other/:")
    for p in sorted((HERE / "other").iterdir()):
        print(" -", p.name)


if __name__ == "__main__":
    main()
