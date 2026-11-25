# The World in One Page — 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/abeteh9ai/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/abeteh9ai/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

## What this is

A single front page that sums up **Tuesday, 24 November 2026** in one
picture. Six stories, all from that day's wire reports:

- Nvidia reinstates Jensen Huang as chief executive; shares jump 31%.
- Ukraine says it sank the Russian warship Merkury off Libya.
- NATO vows to defend space after reports of a Russian nuclear satellite.
- The COP31 climate summit ends without a deal.
- The International Court of Justice rules Myanmar committed genocide
  against the Rohingya.
- Democrats win the US House by the largest margin in decades.

Three more items sit in the "In Brief" strip at the bottom. The date,
the headlines and the facts are all readable inside the image itself.

## How it works

`render.py` draws the page with Pillow and DejaVu fonts — every letter
and every picture is code, not a screenshot, and it uses no media logos.
`main.py` (Python 3.13, standard library only) validates the bundled
`entry.png` (1024×1024, under 1 MiB) and copies it to the output
directory. Both runs write the same bytes; there is no network.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

Built for [make.fun](https://make.fun/r/18yfz1fh) — join with referral
code `18yfz1fh`.
