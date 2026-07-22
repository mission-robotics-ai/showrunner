# QR codes

## Generation

`scripts/qr.py make <url> <out.png> [--style dots]` — python `qrcode[pil]`.

Rules:
- **Error correction H**, always. Box size ≥20px so the source is print-resolution.
- Black on white with a generous quiet zone (border ≥4 modules). Never place on a busy or dark field without a white surround.
- Printed size ≥2.5in for wall signs; bigger if scanned from across a room.
- **Styled variant** (`--style dots`, CircleModuleDrawer): visually distinct from a standard QR — use it when two QR signs must not be confused with each other. Rounded modules occasionally trip weak detectors, so verification (below) is mandatory; if decode fails, increase module size or fall back to RoundedModuleDrawer and re-verify.

## Verification (mandatory, twice)

`scripts/qr.py verify <image> <expected-url>` — OpenCV `QRCodeDetector().detectAndDecode`.

Verify (1) the generated QR file, and (2) the **final placed render** (the full sign PNG/PDF page) — placement can shrink or recompress a QR into unscannability. The decoded string must equal the intended URL exactly, including query params.

## Placement

Frame QRs in a thin border box on white. Put the human-readable URL near the QR as fallback. One QR per sign — two QRs on one surface get scanned interchangeably.
