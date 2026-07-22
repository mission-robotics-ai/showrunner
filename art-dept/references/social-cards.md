# Social cards (OG / square / announce)

Same doctrine as signage, different templates and outputs: HTML card → headless Chrome screenshot at exact pixel dimensions → probe → ship.

## Conventions

- **Standard sizes:** OG 1200×630 (render 2× at 2400×1260 for crispness), square 1080×1080 (2160×2160). Screenshot with `--window-size` at the render scale; the HTML sets a fixed-size body.
- **One brand CSS file** shared by all card templates (tokens, host lockup, sponsor strip, label styles). New card types compose from it — never fork tokens per card.
- **Host lockups and sponsor strips** are components: mark + wordmark pairs sized optically, labeled groups with hairline dividers, `align-items: flex-start` so group labels share a baseline.
- Per-person cards (judges, speakers): keep a **card-data file** per subject (verified name, role line with verification notes, photo path, handles) — cards render from data, and unverified claims ("Founder"? "CEO"?) get flagged in the data file, not silently printed.
- **Editorial loop:** for copy-bearing cards, run the worker–validator pattern — builder drafts, an editor pass submits structured rewrite feedback, director takes the last look. Same probe gates on the rendered PNG.

## Probe

Look at the rendered PNG at full size: text not clipped at the fixed dimensions, images loaded (no broken-image squares), safe margins for platform crops (X/LinkedIn crop edges of OG images).
