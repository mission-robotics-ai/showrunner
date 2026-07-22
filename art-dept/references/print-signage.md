# Print signage

## Conventions

- **One HTML file per sign**, sharing a kit CSS. `@page { size: <W>in <H>in; margin: 0 }`, body sized to the page, content inside a safe margin (~0.4in) — never rely on trimming. Full-bleed backgrounds extend to the edge; a thin white edge on dark signs is acceptable and invisible once hung.
- **Common page sizes:** 8.5×11 letter (portrait or landscape), 11×17 tabloid. Same-day print shops (self-serve/counter copy shops) handle both on cardstock/100lb cover with no lead time. Wide-format, foam-core, and banners need lead time — design around letter/tabloid when the clock is short.
- **A standard band** across the top of every sign (logo lockup left, functional mark right) makes a pile of signs read as one system. Footer rows are optional; cut them cleanly if the client prefers.
- **Sign IDs** (S01, S02…) in filenames and specs keep revision conversations exact.
- **Tent cards:** design a portrait letter sheet as two halves, top half rotated 180°, dashed FOLD rule across the middle; score, fold, done.
- **Wayfinding arrows:** one filled SVG path (shaft rect unioned with solid triangle head), never stroked V-heads or text glyphs — strokes leave seams and specks at print size; glyphs inherit font weight. Rotate one path for direction variants. Match stroke weight to the headline stems.

## Render pipeline

`scripts/render.sh <name> <W_in> <H_in>` → headless Chrome print-to-PDF plus a full-page PNG preview. Edit HTML → re-run → re-probe. Never touch up a PDF.

## Quantities and stocks

Bake quantities into per-stock merged run files (see `references/pdf-runs.md`). The print plan the human carries lists: file → paper stock → "print 1 copy." Mixed orientations in one PDF are fine — the shop prints the file on the stock.

## Field notes

- Lamination glare can defeat phone-camera QR scans — don't laminate QR signs untested.
- Painter's tape for venue walls; command strips for glass; tape all four corners of tabloid sheets or they curl.
- Keep blank spares of each stock for the inevitable "one more over here."
- When signs are cut from a kit, move them to a `cut/` dir instead of deleting — clients reverse cuts.
