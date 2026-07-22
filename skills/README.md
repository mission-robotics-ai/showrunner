# Skills — agent tooling for the event stack

Packaged agent skills for the tools in [`tools.md`](../tools.md), so an AI agent working alongside an event host can operate the stack directly. Roadmap-first: each skill gets built by extracting what we actually did with the tool at a real event, not by wrapping API docs.

## Built

### [tally/](tally/)
Forms as part of an agentic stack, not just a form builder. First play shipped: `notification-verify` — a scripted audit that confirms every event form's submission notifications actually reach a monitored inbox, before doors open. Built from the failure we hit: a submission form whose notifications reached no monitored inbox — the data existed only behind the dashboard login until someone thought to look, days later. `form-staging` (create/configure forms via the API) and `submissions-pull` (programmatic export) are planned there next, once a Tally API key exists.

### [luma/](luma/README.md)
Registration operations as an agent skill, play by play. First play shipped: `funnel-snapshot` — approved/pending/waitlist/declined/invited counts logged to a dated, citable CSV row on a cadence (daily during promo, mandatory day-before, morning-of, pre-doors final), because the numbers are unrecoverable once statuses change. Built from running an approval-gated 340+-registration event where the pre-event snapshot and the door list both turned out to matter after the fact. `curation-pass` (approval triage), `attendee-dossier`, `blast-staging`, and `event-staging` are planned there next.

## The bar for adding a skill here

1. We used the tool at a real event and hit its sharp edges
2. The skill encodes the *operational* knowledge (when to run which pass, what to verify, what goes wrong), not just endpoint wrappers
3. Scrubbed: no credentials, no org-specific assumptions — configuration lives in the consuming project
