# Writeup: City that doesn't exist

## Flag

`KubSTU{2312206762_20.12.2018}` *(submitted post-comp; not verified by the
platform — KubSTU 2026 was over by the time this was solved)*

- **2312206762** — INN of `ООО «ДЕТСТВО+»`, the legal entity that operated
  the Minopolis franchise inside OZ Mall Krasnodar.
- **20.12.2018** — application filing date for Rospatent trademark
  registration №723853, brand `MINOPOLIS`.

## Brief

> В одном из крупнейших торговых центров юга России работал детский
> тематический парк — лицензионный клон иностранной концепции. В 2019 году
> парк внезапно сменил название. Официальных заявлений не последовало.
>
> Твоя задача — установить юридическое лицо, которое управляло клоном, и
> найти дату подачи заявки на регистрацию товарного знака через реестр
> интеллектуальной собственности РФ.

## Identification chain

1. **"Largest shopping centre in southern Russia + children's themed park +
   licensed clone of a foreign concept + renamed in 2019."**
   That set of constraints points at *Minopolis* in OZ Mall, Krasnodar.
   Minopolis was an Austrian "kids' city" franchise (children play adult
   professions for play-money). The Krasnodar park was repeatedly described
   in trade press as `австрийский проект` ("Austrian project"). It opened
   in December 2014.

2. **"Renamed in 2019, no official statements."**
   The same OZ Mall venue later operates under the brand **ZkidZ City**.
   Yuga (regional news) explicitly notes that ZkidZ City *"раньше назывался
   Минополис"* — previously called Minopolis. So the rename is real and
   undocumented officially; only the new owner's marketing acknowledged it.

3. **Operator legal entity (the INN).**
   Two candidates surface in registry searches:

   - `ООО «ТПКО МИНОПОЛИС КРАСНОДАР»` — *excluded* from EGRUL on
     **20 October 2014**, i.e. **before** the park opened in December 2014.
     This entity therefore cannot be the operator and is a decoy.
   - `ООО «ДЕТСТВО +»` — Krasnodar, address `ул. Крылатая, 2`,
     **INN 2312206762**, OGRN 1132312009719. Job postings and CVs on
     hh.ru / Superjob explicitly tie `ООО «ДЕТСТВО+»` to "Minopolis OZ Mall"
     as the employer. Spark-Interfax card:
     <https://spark-interfax.ru/krasnodarski-krai-krasnodar/ooo-detstvo-inn-2312206762-ogrn-1132312009719-4251e8a95f734319a712c185c34bbc66>

   So the operating entity is `ООО «ДЕТСТВО+»`, INN **2312206762**.

4. **Trademark filing date (the second half of the flag).**
   Rospatent's open registry has trademark **№723853** for the wordmark
   `MINOPOLIS`. The card lists `Дата подачи заявки` =
   **20.12.2018**. (The mark was published in 2019, which lines up neatly
   with the Krasnodar venue's 2019 rename to ZkidZ City — somebody else
   had moved on the brand.)

## Sources

- Spark-Interfax card for ООО «ДЕТСТВО+» (INN 2312206762):
  <https://spark-interfax.ru/krasnodarski-krai-krasnodar/ooo-detstvo-inn-2312206762-ogrn-1132312009719-4251e8a95f734319a712c185c34bbc66>
- Yuga / Malls.Ru coverage of the Minopolis → ZkidZ City rename in OZ Mall:
  <https://www.malls.ru/rus/news/48838.shtml>
- Rospatent trademark registry №723853 (`MINOPOLIS`).

## Why the decoy matters

The whole challenge hinges on noticing that there were *two* registered
entities with `Minopolis` in their name in the area, and the older one with
the more obvious name (`ТПКО МИНОПОЛИС КРАСНОДАР`) was already dead before
the park even opened. Submitting that INN would burn an attempt for nothing.
The actual operator never had `Minopolis` in its legal name at all — it's
the bland `ДЕТСТВО+` ("Childhood+") that paid the salaries.
