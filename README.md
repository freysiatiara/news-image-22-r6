# The World in One Day — Sunday 22 November 2026

A one-page broadsheet that sums up the world's news of **Sunday 22 November
2026** in a single 1024×1024 image, entered in make.fun's
*news-image-20261122* competition.

## What the page carries

- **36 stories across 7 regions**, every one an event that happened, or was
  first reported, on Sunday 22 November 2026 (UTC) — plus a date-check box
  naming the other days' stories deliberately left out.
- **Three illustrated leads**: Russia's 186-drone night over Ukraine (161
  downed), COP31's final text landing at dawn in Antalya without naming
  fossil fuels, and Iran's claim of two US radars hit in Bahrain against
  Bahrain's denial — each tagged REPORTED / ONGOING / CLAIM so a contested
  claim is never printed as settled fact.
- **Twelve more pictured stories** (Hong Kong's Election Committee, India's
  record 720/9 in Wellington, Verstappen in Las Vegas, Sparta II still
  burning, and more), a hero-numbers strip, a UTC timeline of the day, a
  dotted world map whose pins match the story numbers, and 21 further
  stories in a compact sourced list.

Every story carries its source wire on the page. Scenes are original drawn
illustrations of reported events, not photographs.

## How it runs

- `main.py` (Python 3, standard library only) copies the committed
  `entry.png` to the output directory (`$MAKEFUN_OUTPUT_DIR`, `$OUTPUT_DIR`,
  or `/output`). It runs identically every time.
- `draw.py` is the generator that drew `entry.png` with Pillow; it is
  deterministic — re-running it reproduces the committed PNG byte for byte.
  It is a build tool only and is not needed by the entry program.

## License

MIT — see `LICENSE`.
