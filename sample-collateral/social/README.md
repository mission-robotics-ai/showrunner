# Social Cards

Announcement card (OG + square) and four winners-card options, all built off one shared stylesheet.

**`card-brand.css` is the single source of truth.** Every font, weight, case, color, and logo treatment used across these cards is defined there exactly once. The individual card files (`card-og.html`, `card-square.html`, `card-winners-*.html`) set layout and per-canvas font sizes only — they don't redefine typography or color. `card-winners.css` loads after `card-brand.css` and adds only the winners-specific pieces (place chips, podium row, results board) without touching the shared tokens.

If you're adapting these for your own event: change the values in `card-brand.css` once, and every card downstream picks it up. That's the whole point of splitting it out.

- `card-og.html` / `card-square.html` — the announcement card, two aspect ratios (1200×630 for link previews, 1080×1080 for feed posts). Rendered PNGs kept at 2x/flagship resolution since these are the cards that actually go out.
- `card-winners-og-optA/B.html`, `card-winners-square-optA/B.html` — two layout options each for OG and square, both post-event. Option B includes a full results board (prize amounts); option A is a simpler podium-only layout.
- `logos/` — only the marks these specific cards reference (sponsor + partner logos, both masked and bright variants of the Mission Robotics orb).
