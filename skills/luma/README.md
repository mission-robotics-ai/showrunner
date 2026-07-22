# Luma — registration operations as agent plays

Plays, not endpoints. Luma's API surface is small enough to hit directly, but hitting it directly is how you end up re-deriving pagination, auth lanes, and status enums from scratch every time someone needs a number. Each play here bundles the doctrine (why this, why now), a script that does the actual pull/aggregate/write, a verification step that catches the failure mode particular to that play, and a note on which decisions stay human (approve/decline calls, blast sends, anything irreversible).

Built from running an approval-gated 340+-registration event where the pre-event snapshot and the door list both turned out to matter after the fact — not written from the API docs outward.

## Plays

| Play | Status | What it does |
|---|---|---|
| [`funnel-snapshot`](funnel-snapshot.md) | **Built** | Logs approved/pending/waitlist/declined/invited counts to a dated CSV row, on a cadence — the numbers are unrecoverable once statuses change, so this is the only way a "day-before" or "pre-doors" count is ever citable later. |
| `curation-pass` | Planned | Approval-pass triage: approve/waitlist/decline registrants against event criteria in a batch, instead of one-by-one. |
| `attendee-dossier` | Planned | Expand the guest list with social handles / bio / registration answers into a per-attendee reference sheet, for door-list lookups and post-event follow-up. |
| `blast-staging` | Planned | Draft and preview event-blast copy safely (preview-only endpoint sends to the authenticated user, never to guests) before an explicit human go fires the real send. |
| `event-staging` | Planned | Event-detail writes (cover image, name, dates, visibility) via the admin session-cookie lane, with the partial-diff footgun (never send the full event object back) documented up front. |

## Auth lanes

Two separate credentials cover different endpoint families — don't reach for the wrong one:

- **Public API key** (`LUMA_API_KEY`, header `x-luma-api-key`) — guest-list reads, guest status updates (approve/decline/waitlist), single-event and calendar-list reads. What `funnel-snapshot` uses.
- **Admin session cookie** (a browser `.luma-session` cookie, gitignored) — event-object writes (cover image, name, blast sends) that the public API key cannot reach. Needed by the planned `event-staging` and `blast-staging` plays.

Both lanes 403 a default `urllib`/`requests` User-Agent regardless of header spoofing (Luma's WAF fingerprints the TLS handshake, not just the UA string) — shell out to `curl` for both.

## Bar for adding a play here

Same bar as the rest of this skill family: run it at a real event, hit its sharp edges, encode the operational knowledge (when to run it, what to verify, what goes wrong) rather than just wrapping an endpoint. Scrubbed — no credentials, no org-specific event IDs or paths; those live in whatever project runs the script.
