# Slide decks (Google Slides API)

Build and edit decks programmatically via `batchUpdate`; probe via page thumbnails. Applies to any Slides MCP/API access.

## Mechanics

- **Units:** EMU. 914400/inch, 12700/pt. Standard wide deck: 12191675 × 6858000.
- Build each slide as: full-bleed background RECTANGLE (solid fill, `outline.propertyState: NOT_RENDERED`), then TEXT_BOXes and images with explicit size + transform. Style text with `updateTextStyle` (use FIXED_RANGE with hand-counted indices for mixed styling — count characters carefully), paragraphs with `updateParagraphStyle`.
- **Fonts:** Google Fonts names work as `fontFamily` (verify by probing — a silent fallback looks like the wrong font, not an error).
- **Images must be publicly fetchable URLs** — a public git repo's raw URLs work (confirm `content-type: image/*` with curl; SVGs are not accepted, rasterize first).
- **Never rescale a placed image via `updatePageElementTransform`** — the API's stored size/scale interaction collapses images unpredictably. To resize: `deleteObject` + `createImage` at the new size. (Learned by shipping four invisible headshots.)
- Circle-cropped headshots: pre-crop with `scripts/image_tools.py circle` (center-square, alpha mask) — Slides can't mask via API.

## Probe discipline

After every batch: fetch a large page thumbnail, download the PNG, **look at it**. Check: fonts resolved, nothing clipped/overlapping, images actually rendering (not dots/blanks), QRs present and scannable-size. Fix and re-probe before reporting.

## Live-edit etiquette

Decks get edited by humans mid-event. Re-fetch presentation state before structural edits; insert by index relative to current state, not remembered state; never delete or reorder slides you didn't create; when a duplicate-work race happens (two writers), fetch state, keep one copy, delete yours.
