# Distribution — two lanes, stable URLs

## Lane 1: the hub (humans)

A single HTML page published somewhere the client can open with one click — a live-preview artifact page, a static site, a shared doc, whatever your stack supports for "privately previewable, then shareable with one action": big download buttons for run files at the top, "what's inside" tables with per-file links, preview grid of every asset, handling notes at the bottom. Written for the person standing at the print counter — quantities, stocks, and instructions live here, not in chat scrollback.

- Embed previews as compressed base64 JPEGs (~440px wide, quality ~68) — many hosted-page environments block external fetches for page assets (CSP), and self-contained means it loads anywhere regardless.
- Keep a **template file with `%%name%%` tokens** and inject previews by script; edit the template, regenerate, republish to the **same file path** so the URL is stable across revisions.
- If your hosting mechanism defaults to private, tell the client explicitly when they're about to send the link — don't assume they know to flip it to shared/public first.
- A login/account switch mid-session can orphan a hosted page (new publishes can't target the old URL). If it happens: publish under a fresh file path, hand over the new URL explicitly, and note that stale copies of the hub still download current files if the file links point at the CDN lane.

## Lane 2: the CDN (files and machines)

A public git repo directory holds every shipping file: per-asset PDFs, merged runs, and image assets. Raw file URLs (e.g. `raw.githubusercontent.com` if hosted on GitHub) serve them as direct downloads and as image sources for slide-deck embeds (content-type follows extension; SVGs won't embed in most slide tools — push rasterized PNGs).

- Revisions overwrite in place: **same filenames, same URLs, forever.** Anyone holding a link always downloads the current file.
- Only push what's meant to be public. Brand-internal source files, contact sheets, and unredacted data stay in a private repo; the public dir gets shipping artifacts only. Don't redistribute third-party assets beyond what the project already publishes.
- Commit messages carry the revision story; a private project repo (if you keep one) mirrors the sources.
