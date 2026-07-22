# Play: funnel-snapshot

Log an event's registration funnel — approved / pending / waitlist / declined / invited counts — to a dated, citable row, on a cadence, before the numbers stop existing.

## Why

Luma's dashboard shows current totals only. There is no historical view of approval-status counts — no "what did pending look like three days ago," no built-in day-over-day chart. Once a guest's status changes (pending → approved, or a late decline), whatever it was before is gone. The only way "we had 340 pending the night before doors" is ever a true, sourceable sentence is if something took that snapshot at that moment.

This org got burned by exactly that gap: a recap needed a "day-before" registration snapshot for a hackathon, and none had been taken — the number had to be reconstructed from memory instead of cited from a log. Recap write-ups, sponsor reports, and formal follow-up letters all eventually want a dated funnel number. Don't reconstruct it. Log it as it happens.

## When

Run it:

- **Daily during the promo window** — cadence, not urgency. Cheap to run, cheap to skip a day, but the trend line only exists if most days are there.
- **Mandatory the day before the event** — this is the number recaps and reports actually reach for. Never skip this one.
- **Morning of** — captures overnight approvals/declines before doors change anything.
- **Pre-doors, final** — the last true "registered" snapshot before check-in data (a different signal — who showed up, not who registered) takes over.

Any of these that gets missed is a small, permanent gap in a citable record. There's no backfill.

## How

```bash
# source your project's Luma API key first
set -a; source /path/to/project/.env; set +a

python3 scripts/luma_snapshot.py --event-id evt-XXXXXXXXXXXX --append snapshots.csv
# or, if you only have the public URL:
python3 scripts/luma_snapshot.py --event-url https://luma.com/some-slug --append snapshots.csv
```

`--append FILE` appends one row to a running CSV log, writing the header first if the file is new or empty. Safe to run repeatedly against the same file — every run adds a row, nothing is overwritten. Add `--json` to get the same row as JSON on stdout instead (useful for piping into something else); it does not replace the CSV append, which still happens if `--append` is also given.

Auth is the public API key lane (`x-luma-api-key` header, env var `LUMA_API_KEY`) — the same key used for guest-list pulls and approve/decline calls elsewhere in this skill family. Not the browser-session-cookie lane used for event-admin writes (cover images, blasts) — that's a different credential entirely.

## Output contract

One CSV row per run:

| column | meaning |
|---|---|
| `iso_timestamp` | UTC, `YYYY-MM-DDTHH:MM:SSZ` — when the snapshot was taken, not when the event happens |
| `event_id` | the `evt-...` id, always logged even if you passed a URL, so rows are joinable without re-resolving |
| `event_name` | as Luma has it at snapshot time |
| `approved` / `pending` / `waitlist` / `declined` / `invited` | guest counts by `approval_status`, tallied from the full paginated guest list |
| `total` | sum of all guests pulled, regardless of status — should equal the sum of the five status columns plus anything unrecognized (see below) |
| `approval_rate` | `approved / total`, rounded to 4 decimals; blank if `total` is 0 |

If the live API ever returns an `approval_status` value this script doesn't recognize, it still counts toward `total` but prints a warning to stderr rather than silently dropping it or guessing which column it belongs in — check the warning before citing the row.

## Verification

- Row lands with plausible non-zero integers for an event that's had registrations.
- The five status columns sum to `total` (any gap means an unrecognized status came through — check stderr).
- `event_id` is stable across runs against the same event — if it drifts, something upstream (URL resolution) is wrong, not the count.
