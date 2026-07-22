# Tally — agent skills

Tally as part of an agentic event stack, packaged as **plays**, not endpoint wrappers. A play is an operational sequence with a reason behind every step — built by hitting a real failure at a real event, not by reading the API docs and guessing what might go wrong.

## Plays

| Play | Status | What it does |
|---|---|---|
| [`notification-verify`](notification-verify.md) | **Built** | Confirms every event form's submission notifications actually reach a monitored inbox, before doors open — catches the failure mode where a form works perfectly and its notifications go nowhere anyone reads. |
| `form-staging` | Planned | Create/configure event forms (project submission, intake, prize fulfillment) via the Tally API once a key exists — fields, logic, and notification recipients set programmatically instead of by hand in the dashboard. |
| `submissions-pull` | Planned | Pull submissions programmatically for tag maps, judging support, and results reconciliation — the same-day export tools.md already calls for, done without a manual CSV download. |

## The bar for adding a play here

1. We used Tally at a real event and hit its sharp edges
2. The play encodes the *operational* knowledge (when to run which pass, what to verify, what goes wrong) — not just an endpoint wrapper
3. Scrubbed: no credentials, no org-specific assumptions — inbox addresses, key paths, and config all come from the consuming project
