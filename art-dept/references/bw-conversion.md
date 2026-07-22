# B&W backup sets

A parallel `-bw` set of every color asset, designed for any office black-and-white printer on plain letter paper. Purpose: if the color print run fails or a sign needs an instant reprint, anyone with a laser printer recovers in minutes.

## Rules

- **Invert to black-ink-on-paper.** Never print dark fields in grayscale — solid toner floods, bands, and wastes cartridges. Dark-ground designs flip to the light treatment: black band, black type, black arrows on paper.
- Color accents map to black; hazard/stripe motifs become black/white with the same geometry.
- **Logos:** use each brand's dark-ink variant where one exists; otherwise invert the white asset programmatically (`scripts/image_tools.py invert`) — white pixels → black, alpha preserved. Probe for gray halos after inversion. Never redraw a mark.
- Keep the -bw set as **separate files** alongside color (suffix `-bw`), merged into their own `bw-run.pdf`. Replace nothing.
- Letter size regardless of the color original — the point is universal printability.
