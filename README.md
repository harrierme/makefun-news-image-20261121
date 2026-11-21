# The World in One Day — Saturday, 21 November 2026

A one-page newspaper front page summing up the world news of Saturday
21 November 2026 in a single image: Russia's overnight strike on Ukraine
with missiles landing in Poland, the AI-led market sell-off that pushed
the S&P 500 into correction, tankers hit near the Strait of Hormuz,
a pancreatic-cancer pill trial — plus 56 more stories from every region.

## The image

`entry.png` (1024×1024, PNG) holds 60 stories, each of which happened or
was first reported on 21 November 2026:

- masthead with the date, 60 stories, 7 regions, 15 fields
- 4 illustrated lead stories and 14 illustrated cards, every one tagged
  with region, field, a CONFIRMED / REPORTED / CLAIM / OFFICIAL label and
  a named source
- a world map with 18 numbered pins matching the lead and card stories
- "The day in numbers" and "The day in UTC" panels
- 42 more stories in a numbered brief list
- a DATE CHECK box naming the big stories deliberately left out because
  they belong to another day (ICJ Myanmar ruling, Anthropic debut,
  Shenzhen summit, Kerch Bridge, Nvidia quarter) or have not happened yet

All illustrations are drawn with Pillow — no photographs.

## How it is built

`build-entry.py` draws `entry.png` from the researched story list in
`stories.md` (date, region, field, source and trust label per story).
The graded program is `main.ts` (Node 22, standard library only): it
copies the finished image to `$MAKEFUN_OUTPUT_DIR/entry.png`
(or `/output/entry.png`), so both graded runs write byte-identical
output with no network access.

Run it locally:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Re-draw the image:

```sh
python3 build-entry.py
```

## Files

- `main.ts` — the entrypoint; copies `entry.png` to the output dir
- `entry.png` — the image the judge sees (1024×1024 PNG)
- `build-entry.py` — the script that draws `entry.png`
- `stories.md` — the researched story list with sources and DATE CHECK
- `LICENSE` — MIT
