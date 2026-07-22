# notification-verify

Confirm that every event form's submission notifications actually reach a monitored inbox — before doors open, not after someone notices the silence.

## Why this play exists

A hackathon ran a project-submission form on Tally. The form worked perfectly: teams filled it out, submissions landed in Tally's dashboard, the data was all there. Nobody was told. The form's notification settings pointed at no inbox anyone actually reads — so every submission sat invisible behind the dashboard login, for days, until someone thought to log in and check.

Nothing about the form was broken. The failure was entirely downstream of "submit succeeded" — in the one setting nobody looks at because the happy path (fill it out, hit submit, see a thank-you page) never touches it. A form can pass every manual test a builder runs and still fail this way, because the builder is testing "does submission work," not "does anyone find out it happened."

The fix isn't "check more carefully." It's "verify the notification path end-to-end, mechanically, for every form, before the event needs it" — the same discipline as testing a webhook by firing it, not by reading the config screen and assuming it's wired right.

## The protocol

Run this for every form in play before an event, and again for any form added mid-event:

1. **Enumerate the event's forms.** Every Tally form that's live for this event — submission forms, intake forms, prize-fulfillment forms, feedback forms. If a form exists and someone is supposed to see what comes in, it's in scope.
2. **Confirm notification recipients in Tally settings.** Open each form's Settings > Notifications tab. Note who's listed. If nobody is listed, or the list is a person who left, or an inbox nobody actively reads — that's already a finding, before any test submission.
3. **End-to-end test.** Submit a real test entry through the live form (not a preview). Confirm arrival in **every** monitored inbox within a few minutes. Don't stop at the first inbox that gets it — the failure this play catches is exactly "some inboxes get it, the one that matters doesn't."
4. **Confirm the data destination is accessible to the team.** Whoever needs the export (judging, follow-up, results) can actually reach it — right permissions on the sheet/dashboard, not just "it exists somewhere."
5. **Record verification in the event checklist.** A run without a written record is indistinguishable, a week later, from a run that never happened. Note the date, who tested, which inboxes confirmed receipt.

Step 3 is where `tally_notification_audit.py` earns its keep — it turns "did the test submission arrive" from a manual inbox-check into a scripted, repeatable pass across every inbox you monitor, and it's the same tool you re-run after the event to catch drift (someone changes notification settings mid-event, a new form gets added without anyone testing it).

## Script usage

`scripts/tally_notification_audit.py` reads your monitored inboxes over a lookback window, lists every distinct Tally form title it found notifications for (per inbox, with the latest arrival time), and — if you pass `--expect "Form Title"` for each form that should be live — exits nonzero and prints exactly which expected form had **zero** notifications in **any** inbox.

Minimal case — one Gmail account, one AgentMail-style inbox:

```bash
uv run --with google-api-python-client --with google-auth python3 scripts/tally_notification_audit.py \
  --days 10 \
  --gmail-token /path/to/gmail_token.json --gmail-label "you@yourdomain.com" \
  --agentmail-key /path/to/agentmail_key --agentmail-inbox agent@yourdomain.com \
  --expect "Project Submission" \
  --expect "General Intake"
```

Arbitrary inbox set via JSON config (any org, any mix of accounts):

```bash
python3 scripts/tally_notification_audit.py --days 10 --config inboxes.json --expect "Project Submission"
```

```json
{
  "inboxes": [
    {"type": "gmail", "label": "you@yourdomain.com", "token_path": "/path/to/token.json"},
    {"type": "agentmail", "label": "agent@yourdomain.com", "key_path": "/path/to/key",
     "inbox": "agent@yourdomain.com", "limit": 200}
  ]
}
```

No inbox address, key path, or token path is hardcoded in the script — everything comes from `--config` or the `--gmail-*` / `--agentmail-*` flags. Adding another inbox type (Slack webhook capture, a different email provider) is a new `InboxAdapter` subclass registered in `ADAPTER_TYPES`; the audit and matching logic don't change.

Exit codes: `0` clean (every `--expect`'d form seen somewhere, or no `--expect` given), `1` at least one expected form was missing everywhere — this is the failure mode to treat as a blocker, not a warning — `2` every configured inbox failed to fetch (a config/auth/network problem, not a form problem).

Match logic on `--expect` is case-insensitive substring-or-equal against observed titles, so small title variations (trailing punctuation, casing) don't produce false misses — but a genuinely wrong title will still slip past, so eyeball the printed table too, not just the exit code.

## The API-key lane (upgrade path)

No Tally API key exists yet for this org. When one does, this play upgrades from "read the inboxes and infer" to "ask Tally directly":

- **Form enumeration** — list every form via the API instead of manually walking the dashboard, closing the gap where a form gets created and nobody adds it to the checklist.
- **Webhook checks** — Tally supports webhooks in addition to email notifications; with a key, confirm webhook delivery status directly rather than only inferring from inbox arrival.
- **Submissions pull** — pull submission data programmatically (feeds `submissions-pull`, the planned play in the parent [README](README.md)), which also gives this play a second, independent confirmation path: "did Tally register a submission" cross-checked against "did a notification email arrive."

Until the key lane exists, this play's ground truth is the inbox — which is also, not coincidentally, the actual failure surface. A working API integration doesn't replace this check; it adds a second one.
