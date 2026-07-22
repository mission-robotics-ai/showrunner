# Sample Collateral

Real signage and social cards from a real event, kept here so the next host has something to look at — and something to copy — instead of starting from a blank page.

## The basics every in-person event needs

Every event needs these nine things printed or posted somewhere. Miss one and you'll hear about it from a hacker at 9am.

- **Check-in sign** — the first thing a nervous attendee looks for when they walk in the door. If they can't find it in three seconds, they hover awkwardly near the entrance instead of finding their team.
- **Main hero sign** — the photo backdrop and the "you're in the right place" signal. This is what ends up in every attendee's first post about your event, so it's doing marketing work whether you planned for that or not.
- **Bathroom directionals** — the most-asked question at every event, full stop. Make several; one sign at the one fork in the hallway isn't enough once the building fills up.
- **Directional / wayfinding arrows** — stairs, overflow rooms, anywhere the venue doesn't self-explain. Build these as variants of one template (up / left / up-left / right) rather than one-off signs per doorway — see how `s01` does it below.
- **WiFi sign** — always with the password as a loud `TK` placeholder in the source file, never a real password committed anywhere. Fill it in at render time, not in git.
- **Community / group-chat QR sign** — decode-verify the QR before it goes to print. A QR that doesn't scan under venue lighting is worse than no sign at all.
- **Schedule / run-of-show poster** — one glance answers "what's happening now and what's next" without anyone needing to ask staff.
- **Station / bay number signs** — teams need addresses. "Bay 3" is a real piece of information once you have more than a handful of teams; don't make people count doorways.
- **Staff-only / no-entry** — anywhere the public shouldn't wander. Doesn't have to be scary, just clear about what's on the other side.

**The B&W-laser doctrine:** every sign in here should also work as a plain black-and-white printout — high contrast, big type, letter paper, any office printer, no color toner required. If your venue's printer jams or someone needs one more sign at midnight, you should be able to print it from a laptop and a Staples run. `print/s01-noarrow-bw.html` / `.png` is the reference example — same layout, ink-only.

## About these samples

These come from a real 3-day robotics hackathon (~80 hackers, in San Francisco). Two ways to use them:

- **Look at the PNGs** to see how the finished pieces read — hierarchy, contrast, how much white space survives at print size.
- **Edit the HTML + CSS sources** with the [art-dept](../art-dept/) system to make your own. Swap the copy, keep the bones.

The brand tokens (fonts, colors, logo treatment) baked into these files are one event's choices, not a house style — swap them for your own before you ship anything. See `print/kit.css` and `social/card-brand.css` for where those choices live.

## What's in each folder

- **`print/`** — signage: HTML source + PNG preview, paired by filename. `kit.css` and `assets/` hold everything the HTML files need to re-render (fonts, AprilTag markers, sponsor logos, QR codes).
- **`social/`** — announcement + winners social cards (OG + square), plus `card-brand.css`, the single-source-of-truth stylesheet. See `social/README.md`.
