# Fiducials (AprilTags) as design language

Real, functional fiducials — never decorative fakes. If your event's design system wants machine-readable marks (robotics-themed signage, a wayfinding system a robot or a scanner reads), use genuine codes so any detector returns a valid ID.

## Sourcing

Official pre-rendered tags: `https://raw.githubusercontent.com/AprilRobotics/apriltag-imgs/master/tag36h11/tag36_11_XXXXX.png` (10×10px PNGs, zero-padded 5-digit ID). tag36h11 is the standard family.

## The blur trap (learned the hard way)

The source PNGs are 10×10 pixels. CSS `image-rendering: pixelated` keeps them crisp in **screenshots**, but **PDF output embeds the tiny original and viewers/printers smooth it** — tags ship blurry and detection fails. **Pre-upscale every tag 64× with nearest-neighbor** (`scripts/image_tools.py upscale <in> <out> 64`) before rendering. Bit-identical codes, print-crisp edges. Zoom-probe the shipping PDF to confirm hard square edges.

## Conventions that make tags functional

- **One ID scheme, documented:** e.g. tag ID = bay number for location signs; ID = 100 + sign number for everything else. A robot (or a person with a scanner) that reads a sign then knows *which* sign.
- One tag per sign, fixed corner, consistent size — like a printer's registration mark.
- Always monochrome, matte (gloss glare kills detection), with a white quiet zone.
- Never blow a tag up as wall art; never more than one per surface.
