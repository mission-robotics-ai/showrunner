# Tools

The stack we actually run events on, with the sharp edges labeled. Nothing here is sponsored; it's just what survived contact with real events.

## Registration & attendance

**Luma** — event page, registration, approvals, comms.
- Use **approval-gated registration** for capacity-limited events: it turns your attendee list into a curation surface and gives you a waitlist for free.
- Pending guests can't see venue details until approved — run approval passes on a cadence (daily as the event nears), or people show up confused about where to go.
- The host dashboard's counts are the truth; public API counts undercount pending. Snapshot your funnel numbers (approved / pending / waitlist / declined) the day before doors — you'll want them for the recap, and they're unrecoverable later.
- Blast emails to approved guests lift approval-to-attendance meaningfully; the day-before and morning-of sends matter most.

## Forms & submissions

**Tally** — project submissions, intake forms, prize fulfillment.
- **Verify notification routing before the event.** A form works perfectly while its submission notifications go... nowhere you read. Test-submit and confirm the notification lands in a monitored inbox.
- Make teams **confirm their repo is public** with a literal checkbox ("I opened it in an incognito window") — judges hitting 404s during deliberation is a self-inflicted wound.
- Ask for "where to find you" (table number) and a during-judging phone contact — demo-day logistics run on these two fields.
- Export submissions to a spreadsheet same-day; the export is your tag map for winner announcements (names, repos, links).

## Comms

**Slack** — one partner channel per event ([template](templates/partner-slack-channel.md)). Create it the week before load-in; the pinned message carries the run of show. Faster than email threads for "a robot is wobbling" day-of traffic.

**A fulfillment sheet** (Google Sheets) — winners, amounts, payout details ([pattern](templates/prize-fulfillment-sheet.md)). Private. Created before demos, filled during deliberation.

## Collateral

**The art-dept system** ([full docs](art-dept/)) — HTML + a shared brand CSS file as the single source of truth, rendered to exact-dimension PNGs via headless Chrome for social cards, and to PDFs for print signage. QR codes decode-verified from final renders with OpenCV. The whole methodology, including the verification gates that catch what "looks done" hides, lives in the folder.

## Food logistics

Same-day grocery delivery (Instacart → Costco, Safeway delivery) + one local pizza shop + a bagel catering delivery ([full order book](event-types/in-person-hackathon/food-and-vendors.md)). No catering contracts, no minimums, one card, one owner.

## Print

Any office **B&W laser printer** covers signage needs if your design system is built for it (the art-dept references include a B&W conversion recipe). Color print shops are for banners only; everything else is letter paper, high contrast, big type.

## Roadmap

Agent skills for this stack — Luma and Tally first — are being packaged in [`skills/`](skills/) as we extract them from our own operations.
