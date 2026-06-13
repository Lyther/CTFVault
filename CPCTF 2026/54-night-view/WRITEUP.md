# Night View (OSINT, Naru820)

**Status:** Solved

**Flag:** `CPCTF{333413426}`

## Answer

- OpenStreetMap object: `way 333413426`
- Building: `msb Tamachi 田町ステーションタワーN`

## Why this was the right one

- The real breakthrough was the blog post `http://likearamen.xii.jp/article/191312451.html`.
- Its first photo is the same viewpoint as the challenge image, just wider and clearer.
- Nearby posts on the same blog explicitly place the author's weekday lunch / work radius in `田町 / 芝浦`, which killed the old `豊洲` origin theory.
- Once the search area was reduced to the actual workplace neighborhood, the remaining tall, office-plausible `way` objects were basically `田町タワー`, `msb Tamachi 田町ステーションタワーS`, and `msb Tamachi 田町ステーションタワーN`.
- The correct one was `msb Tamachi 田町ステーションタワーN`, `way 333413426`.

## What the photo shows

- Rainbow Bridge is visible in the background.
- The photo is taken from a high indoor viewpoint through glass.
- The lower half includes canals, office blocks, elevated roads, and dense waterfront towers.

## Successful submission

| Flag | Building / object |
|---|---|
| `CPCTF{333413426}` | `msb Tamachi 田町ステーションタワーN` |

## Failed submissions so far

Submitted in chronological order.

| # | Flag | Building / object |
|---|---|---|
| 1 | `CPCTF{929171294}` | 豊洲ベイサイドクロスタワー / Toyosu Bayside Cross |
| 2 | `CPCTF{1028685733}` | ブランズタワー豊洲 / Branz Tower Toyosu |
| 3 | `CPCTF{359694743}` | SKYZ / Skyz Toyosu |
| 4 | `CPCTF{509109979}` | ベイズタワー＆ガーデン / Bayz Tower & Garden |
| 5 | `CPCTF{1023801176}` | ラビスタ東京ベイ / La Vista Tokyo Bay |
| 6 | `CPCTF{197996777}` | The Tokyo Towers Mid Tower |
| 7 | `CPCTF{454866513}` | ドゥ・トゥールキャナル＆スパ ウエスト棟 |
| 8 | `CPCTF{1448346307}` | パークタワー晴海 |
| 9 | `CPCTF{383386516}` | プラウドタワー東雲キャナルコート |
| 10 | `CPCTF{174022611}` | パークタワー東雲 |
| 11 | `CPCTF{456191540}` | ビーコンタワーレジデンス |
| 12 | `CPCTF{174022709}` | アップルタワー東京キャナルコート (outer way) |
| 13 | `CPCTF{154125420}` | Wコンフォートタワーズイースト (outer way) |
| 14 | `CPCTF{174022605}` | Wコンフォートタワーウェスト (outer way) |
| 15 | `CPCTF{456191539}` | キャナルファーストタワー |
| 16 | `CPCTF{383387755}` | シティタワー有明 |
| 17 | `CPCTF{689591514}` | 湾岸タワーレックスガーデン |
| 18 | `CPCTF{149133622}` | Galleria Grande |
| 19 | `CPCTF{197996776}` | The Tokyo Towers Sea Tower |
| 20 | `CPCTF{956558501}` | パークタワー勝どきサウス |
| 21 | `CPCTF{1028684458}` | パークタワー勝どきミッド |
| 22 | `CPCTF{717183317}` | Kachidoki The Tower |
| 23 | `CPCTF{454866514}` | ドゥ・トゥールキャナル＆スパ イースト棟 |
| 24 | `CPCTF{463203575}` | キャピタルゲートプレイスザ・タワー |
| 25 | `CPCTF{381147498}` | ザ・パークハウス晴海タワーズ・ティアロレジデンス / Tiaro Residence |
| 26 | `CPCTF{381147497}` | クロノレジデンス / Kurono Residence |
| 27 | `CPCTF{385067058}` | ブリリア有明シティタワー |
| 28 | `CPCTF{1112419771}` | ブリリアタワー有明ミッドクロス |
| 29 | `CPCTF{2278014}` | Brillia Mare Ariake (relation) |
| 30 | `CPCTF{2324438}` | アップルタワー東京キャナルコート (relation) |
| 31 | `CPCTF{2324435}` | Wコンフォートタワーウェスト (relation) |
| 32 | `CPCTF{2324436}` | Wコンフォートタワーズイースト (relation) |
| 33 | `CPCTF{102379220}` | THE TOYOSU TOWER |
| 34 | `CPCTF{187753906}` | シティタワーズ豊洲 / City Towers Toyosu |
| 35 | `CPCTF{103614208}` | アーバンドックパークシティ豊洲Ａ棟 |
| 36 | `CPCTF{187753908}` | シティタワーズ豊洲ザ・ツインS棟 |
| 37 | `CPCTF{103614209}` | アーバンドックパークシティ豊洲Ｂ棟 |
| 38 | `CPCTF{605982329}` | シティタワーズ東京ベイイーストタワー |
| 39 | `CPCTF{605982324}` | シティタワーズ東京ベイセントラルタワー |
| 40 | `CPCTF{605982326}` | シティタワーズ東京ベイウエストタワー |
| 41 | `CPCTF{22918543}` | 豊洲センタービル |
| 42 | `CPCTF{22918544}` | 豊洲センタービル アネックス |
| 43 | `CPCTF{102519005}` | 豊洲IHIビル |
| 44 | `CPCTF{187753905}` | 豊洲キュービックガーデン |
| 45 | `CPCTF{187753924}` | 豊洲フロント |
| 46 | `CPCTF{310317375}` | 豊洲フォレシア |
| 47 | `CPCTF{103096478}` | シティコープ豊洲 |
| 48 | `CPCTF{155510003}` | ベイクレストタワー |
| 49 | `CPCTF{155510017}` | ワールドシティタワーズアクアタワー |
| 50 | `CPCTF{155509991}` | ワールドシティタワーズブリーズタワー |
| 51 | `CPCTF{155509996}` | ワールドシティタワーズ キャピタルタワー |
| 52 | `CPCTF{163551914}` | コスモポリス品川 |
| 53 | `CPCTF{155012544}` | City Tower Shinagawa / シティタワー品川 |
| 54 | `CPCTF{155012535}` | フェイバリッチタワー品川 |
| 55 | `CPCTF{208525510}` | ブランズタワー芝浦 |
| 56 | `CPCTF{119745269}` | プラウドタワー芝浦 |
| 57 | `CPCTF{187753921}` | unnamed `180 m` tower next to シティタワーズ豊洲ザ・ツインS棟 |
| 58 | `CPCTF{103096481}` | 日本ユニシス |
| 59 | `CPCTF{929171296}` | SMBC豊洲ビル |
| 60 | `CPCTF{509109510}` | パークホームズ豊洲ザレジデンス |
| 61 | `CPCTF{685396628}` | プラザタワー勝どき |
| 62 | `CPCTF{657940532}` | Plaza Kachidoki B |
| 63 | `CPCTF{179554456}` | Office Tower X |
| 64 | `CPCTF{179554451}` | Office Tower Y |
| 65 | `CPCTF{467706902}` | リバーポイントタワー |
| 66 | `CPCTF{467706903}` | シティフロントタワー |
| 67 | `CPCTF{467706905}` | スカイライトタワー |
| 68 | `CPCTF{547375747}` | ミッドタワーグランド |
| 69 | `CPCTF{467699845}` | コーシャタワー佃 |
| 70 | `CPCTF{467699840}` | イーストタワー２ |
| 71 | `CPCTF{467699842}` | イーストタワー10号棟 |
| 72 | `CPCTF{119563859}` | 聖路加タワー |
| 73 | `CPCTF{107771602}` | Toyosu Ciel Tower (outer way) |

## Notes

- `三井ガーデンホテル豊洲プレミア / Mitsui Garden Hotel Toyosu Premier` exists in OSM as `node 13129739070`, not as the building polygon.
- The building polygon at that location is still `way 929171294` (`Toyosu Bayside Cross`), which already failed.
