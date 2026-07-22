# Skills — agent tooling for the event stack

Packaged agent skills for the tools in [`tools.md`](../tools.md), so an AI agent working alongside an event host can operate the stack directly. Roadmap-first: each skill gets built by extracting what we actually did with the tool at a real event, not by wrapping API docs.

## Planned

### luma
Registration operations as an agent skill: approval-pass triage (approve/waitlist/decline against event criteria), funnel snapshots (approved/pending/waitlist counts logged on a cadence — these are unrecoverable after the event), guest-list pulls for door lists and post-event sweeps, blast timing. Built from: running an approval-gated 340+-registration event where the pre-event snapshot and the door list both turned out to matter after the fact.

### tally
Forms as part of an agentic stack, not just a form builder: create/configure event forms (project submission, intake, prize fulfillment) via the API, **verify notification routing end-to-end before doors** (the failure we hit: a submission form whose notifications reached no monitored inbox — the data existed only behind the dashboard login until someone thought to look), pull submissions programmatically for tag maps, judging support, and results reconciliation.

## The bar for adding a skill here

1. We used the tool at a real event and hit its sharp edges
2. The skill encodes the *operational* knowledge (when to run which pass, what to verify, what goes wrong), not just endpoint wrappers
3. Scrubbed: no credentials, no org-specific assumptions — configuration lives in the consuming project
