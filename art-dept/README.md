# Art Dept

An art-director loop for producing event collateral — signage, social cards, slide decks, sponsor slates, QR signs, asset hubs — with verification gates that catch the mistakes that only show up in the shipped file, not the preview.

**Who this is for:** anyone running an event (hackathon, conference, meetup, launch) who needs a batch of branded visual assets produced fast, correctly, and without the person doing final review having to answer vague design questions. It's written to be run by a person paired with an AI agent — any agent capable of writing HTML/CSS, running shell commands, and holding a long conversation. Nothing here is specific to one AI product or vendor.

The system's two promises: work progresses far before the reviewer sees it, and the reviewer approves by **picking between finished options**, never by answering abstract design questions.

## Roles

- **The client** — the person you're building for. Final taste authority.
- **The director** — the agent running this loop: intake, mockup, probing, bouncing defects, distribution.
- **The builder** — a second, persistent agent session (a subagent, a second chat window, a delegated worker — whatever your stack supports) that does the actual production work. It stays alive for the whole life of the kit so revision rounds are cheap.

If your agent setup doesn't support a separate builder session, the director can do the building itself — the loop still works, you just lose the context-isolation benefit.

## The loop

1. **Intake.** Pin down: asset family (see below), deadline, distribution targets (print shop? wall? web? deck?), and which facts are known vs missing. Read the project's brand sources (see Brand resolution) before designing anything.
2. **Mockup first.** Propose the *whole system* as one reviewable surface (a single HTML page, or whatever hosted-preview mechanism your agent has — a live-preview artifact, a local dev server, a shared doc): every asset, one visual language, real copy. Mark every missing fact with a loud `TK` chip. Anything unshippable (a phone number, a password) renders as a can't-ship-by-accident placeholder — visually loud, impossible to print unnoticed.
3. **Fact fill.** Pull facts from the project's canonical docs (schedules, sponsor lists, contact sheets) — never from memory, never invented. Facts only the client knows get asked for once, batched.
4. **Spawn ONE named builder** (e.g. `signage-builder`) and keep it alive for the kit's whole life. Every revision round goes back to that same builder session — it holds the entire kit in context, so iteration cost stays near zero. Never respawn per round; never do builder work in the main thread while a builder session exists.
5. **Build → probe → bounce.** The builder renders, probes its own output, and reports honestly. The director then probes independently — every changed render, at full size, **in the shipping format** (see Probe gates). Bounce defects back with concrete mechanisms, not vibes ("rebuild the arrow as ONE filled path — stroked V-heads leave seams"), and re-probe.
6. **Merge and count.** Batch outputs into per-destination run files (one PDF per paper stock, quantities baked in). Verify counts programmatically. The human's job at the printer is: print one copy of each file.
7. **Distribute on two lanes.** A human-facing hub (a single web page: download buttons, previews, quantities, handling notes) and a machine-facing CDN (a public git repo; raw file URLs). Redeploy in place — **stable URLs across every revision** so shared links never rot.
8. **Revision rounds** repeat 5–7. When a merged file changes after distribution, say so plainly: "re-download both files."
9. **Close.** Commit everything, note the final hub state, and give an honest note about anything already produced from stale files.

## Probe gates (non-negotiable)

- **Look at every changed render at full size.** Both builder and director, independently. "Requests applied" is not verification.
- **Probe the shipping format.** PDF output can differ from screen previews (rasterization, smoothing, embedded-image handling). A screen-crisp asset can ship blurry. If it ships as PDF, open the PDF.
- **QRs decode-verify** with OpenCV from the *final placed render*, and the decoded string must equal the intended URL exactly. See `references/qr-codes.md`.
- **Merged runs page-count** against the manifest. See `scripts/pdf_runs.py`.
- **Zoom-check pixel-precise elements** (fiducials, QRs, fine linework) at high magnification.
- Fix and re-probe before reporting. Report probe results honestly, including what's still off.

## Asset families

| Family | Source of truth | Output | Reference |
|---|---|---|---|
| Print signage / posters | one HTML file per sign | PDF (print) + PNG (preview) via headless Chrome | `references/print-signage.md` |
| B&W backup set | derived `-bw` HTML variants | letter PDFs for any office printer | `references/bw-conversion.md` |
| Social cards (OG / square) | HTML card templates + brand CSS | PNG at exact pixel dims via Chrome screenshot | `references/social-cards.md` |
| Slide decks | Slides API batchUpdate | live deck; thumbnails as probes | `references/slides-decks.md` |
| Hubs / dashboards | HTML with embedded previews | a single hosted web page | `references/distribution.md` |

Cross-cutting recipes: `references/qr-codes.md`, `references/fiducials.md`, `references/pdf-runs.md`.

## Brand resolution

This system contains **no brand**. Resolve, in order: (1) brand/style docs named in your project's README or style guide; (2) a `design/` or `brand-assets/` directory in the project (tokens, logo library, font specs); (3) an existing approved asset family (a shipped card system or site) — extract its tokens rather than inventing; (4) if none exist, propose tokens as part of the mockup and get them picked like any other option. Logos: use the project's asset library; never redraw a third-party mark by hand; derive variants (raster, invert, crop) by script — see `scripts/image_tools.py`. Never redistribute third-party logos beyond what the project already publishes.

*Example only:* one project that ran this system chose Instrument Serif for display type and Archivo Black for hero headlines, with a small locked hex palette. That's one project's pick, not a rule — treat any brand specifics you see referenced elsewhere as one team's answer to step 4, not this system's default.

## Human gates (never automate)

Taste verdicts. Facts (phone numbers, passwords, who's-on-which-tier). Irreversible spends (print runs, publishing, sends). Sharing a hosted page or making a repo public. When the client's instruction conflicts with a recorded obligation (e.g. a sponsor contract promising placement), flag it once, plainly, then follow their call.

## Review posture

Present **options, not questions** — n rendered variants beat one "what direction?" Ask only for facts you cannot derive and decisions that are genuinely the client's. Batch asks. When the client gives feedback mid-flow, fold it into the live builder round; when they say something looks wrong, find the mechanism before bouncing it.
