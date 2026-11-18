# Tuesday 17 November 2026 — the world's news in one picture

[![make.fun](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117)

One-page newspaper front page summarising the world news of Tuesday
17 November 2026: 43 stories, 6 continents — 3 lead stories with drawn
diagrams (Kerch Bridge, Strait of Hormuz, Quad summit in Manila), 10 more
stories in a grid, a world map with numbered pins, and a numbered
"Also on Tuesday 17 November" list (stories 14–43).

A six-number stat strip on top anchors the day at a glance: 11,000+ Ebola
cases in DR Congo, Nvidia's $115.8bn quarter, the Dow down 849, 1,441 drones
Russia says it downed, 2m+ barrels on the tanker Iran says it hit, and
Voyager 1 crossing one light-day from Earth.

## Entry

`main.py` (Python 3.13, standard library only) copies the pre-rendered
`entry.png` to `/output/entry.png`. No network. The copy is byte-for-byte,
so repeated runs produce identical output — the program prints the SHA-256
of what it wrote so the two runs can be compared.

`entry.png` was drawn by the author with `gen.py` (PIL only, no network,
fully deterministic). See `NOTES.md` for the story list, layout decisions,
and the side-by-side check against the three reference front pages.

## Licence

MIT — see `LICENSE`.
