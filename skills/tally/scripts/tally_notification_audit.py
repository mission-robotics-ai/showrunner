#!/usr/bin/env python3
"""
tally_notification_audit.py — confirm Tally form notifications actually reach a monitored inbox.

Born from a real failure: a hackathon project-submission form (Tally form 44DBWX) whose
submission notifications reached NO inbox. The form worked. The data was real. It just sat
invisible behind the dashboard login until someone thought to look, days later.

This script does not touch the Tally API (no key exists at the org running this script yet).
It reads the INBOXES that are supposed to be receiving Tally's notification emails, and asks
a blunt question: for every form we expect to be live, did a notification actually show up
somewhere a human reads?

Usage
-----
Quick, one-Gmail-one-AgentMail case:

    python3 tally_notification_audit.py --days 10 \\
        --gmail-token /path/to/gmail_token.json --gmail-label "you@yourdomain.com" \\
        --agentmail-key /path/to/agentmail_key --agentmail-inbox agent@yourdomain.com \\
        --expect "Project Submission" --expect "General Intake"

Arbitrary set of inboxes (any org, any mix of Gmail/AgentMail accounts) via a JSON config:

    python3 tally_notification_audit.py --days 10 --config inboxes.json --expect "..."

Config file shape:

    {
      "inboxes": [
        {"type": "gmail", "label": "you@yourdomain.com", "token_path": "/path/to/token.json"},
        {"type": "agentmail", "label": "agent@yourdomain.com", "key_path": "/path/to/key",
         "inbox": "agent@yourdomain.com", "limit": 200}
      ]
    }

No inbox address, key path, or token path is hardcoded anywhere in this file — every value
above comes from --config or the --gmail-*/--agentmail-* flags. Add a new adapter type by
subclassing InboxAdapter and registering it in ADAPTER_TYPES.

Exit codes
----------
0 — ran cleanly; every --expect'd form was seen in at least one inbox (or no --expect given)
1 — ran cleanly; at least one --expect'd form was seen in ZERO inboxes (the failure this
    script exists to catch)
2 — could not fetch from any configured inbox (config/auth/network problem)

Never prints key or token file contents — only paths.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

# Tally's notification subject pattern. Other tally.so mail exists (billing receipts, digest
# emails) — this is what distinguishes an actual submission notification from the rest.
SUBJECT_RE = re.compile(r"^(?:Re:\s*)?New Tally Form Submission for (.+)$", re.IGNORECASE)
TALLY_SENDER_HINTS = ("tally.so",)


@dataclass
class Notification:
    inbox_label: str
    form_title: str
    timestamp: datetime
    sender: str
    subject: str


@dataclass
class InboxAdapter:
    """Base class for a pluggable notification source. Subclass and implement fetch()."""

    label: str

    def fetch(self, since: datetime) -> list[Notification]:
        raise NotImplementedError


@dataclass
class GmailAdapter(InboxAdapter):
    token_path: str = ""

    def fetch(self, since: datetime) -> list[Notification]:
        try:
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
        except ImportError as e:
            raise RuntimeError(
                "gmail adapter needs google-api-python-client + google-auth. "
                "Run this script via: uv run --with google-api-python-client --with google-auth python3 ..."
            ) from e

        with open(self.token_path) as f:
            info = json.load(f)
        creds = Credentials.from_authorized_user_info(info, info.get("scopes"))
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
        service = build("gmail", "v1", credentials=creds)

        days = max(1, (datetime.now(timezone.utc) - since).days + 1)
        query = f"from:tally.so newer_than:{days}d"

        results: list[Notification] = []
        page_token = None
        while True:
            resp = (
                service.users()
                .messages()
                .list(userId="me", q=query, pageToken=page_token, maxResults=100)
                .execute()
            )
            for m in resp.get("messages", []):
                msg = (
                    service.users()
                    .messages()
                    .get(
                        userId="me",
                        id=m["id"],
                        format="metadata",
                        metadataHeaders=["Subject", "From", "Date"],
                    )
                    .execute()
                )
                headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
                subject = headers.get("Subject", "")
                sender = headers.get("From", "")
                match = SUBJECT_RE.match(subject.strip())
                if not match:
                    continue  # tally.so mail that isn't a submission notification (receipts, etc.)
                internal_ms = int(msg.get("internalDate", "0"))
                ts = datetime.fromtimestamp(internal_ms / 1000, tz=timezone.utc)
                if ts < since:
                    continue
                results.append(
                    Notification(
                        inbox_label=self.label,
                        form_title=match.group(1).strip(),
                        timestamp=ts,
                        sender=sender,
                        subject=subject,
                    )
                )
            page_token = resp.get("nextPageToken")
            if not page_token:
                break
        return results


@dataclass
class AgentMailAdapter(InboxAdapter):
    key_path: str = ""
    inbox: str = ""
    limit: int = 200
    base_url: str = "https://api.agentmail.to/v0"

    def fetch(self, since: datetime) -> list[Notification]:
        with open(self.key_path) as f:
            key = f.read().strip()

        url = f"{self.base_url}/inboxes/{self.inbox}/messages?limit={self.limit}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.load(resp)
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"agentmail fetch failed for inbox {self.inbox}: HTTP {e.code}") from e

        results: list[Notification] = []
        for msg in data.get("messages", []):
            sender = msg.get("from", "")
            if not any(hint in sender.lower() for hint in TALLY_SENDER_HINTS):
                continue
            subject = msg.get("subject", "")
            match = SUBJECT_RE.match(subject.strip())
            if not match:
                continue
            ts_raw = msg.get("timestamp", "")
            try:
                ts = datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
            except ValueError:
                continue
            if ts < since:
                continue
            results.append(
                Notification(
                    inbox_label=self.label,
                    form_title=match.group(1).strip(),
                    timestamp=ts,
                    sender=sender,
                    subject=subject,
                )
            )

        # Warn (don't fail) if the page may be truncating the lookback window.
        if len(data.get("messages", [])) >= self.limit and data.get("next_page_token"):
            oldest_fetched = None
            if data.get("messages"):
                try:
                    oldest_fetched = datetime.fromisoformat(
                        data["messages"][-1]["timestamp"].replace("Z", "+00:00")
                    )
                except (KeyError, ValueError):
                    pass
            if oldest_fetched and oldest_fetched > since:
                print(
                    f"  [warn] agentmail inbox '{self.inbox}': limit={self.limit} may not cover "
                    f"the full {since.date()}-to-now window (more pages exist). Raise --agentmail-limit.",
                    file=sys.stderr,
                )
        return results


ADAPTER_TYPES = {
    "gmail": GmailAdapter,
    "agentmail": AgentMailAdapter,
}


def build_adapters_from_config(config_path: str) -> list[InboxAdapter]:
    with open(config_path) as f:
        cfg = json.load(f)
    adapters = []
    for entry in cfg.get("inboxes", []):
        entry = dict(entry)
        kind = entry.pop("type", None)
        cls = ADAPTER_TYPES.get(kind)
        if cls is None:
            raise ValueError(f"unknown inbox type '{kind}' in config (known: {list(ADAPTER_TYPES)})")
        adapters.append(cls(**entry))
    return adapters


def build_adapters_from_flags(args: argparse.Namespace) -> list[InboxAdapter]:
    adapters: list[InboxAdapter] = []
    if args.gmail_token:
        adapters.append(
            GmailAdapter(label=args.gmail_label or args.gmail_token, token_path=args.gmail_token)
        )
    if args.agentmail_key:
        if not args.agentmail_inbox:
            raise ValueError("--agentmail-key requires --agentmail-inbox")
        adapters.append(
            AgentMailAdapter(
                label=args.agentmail_label or args.agentmail_inbox,
                key_path=args.agentmail_key,
                inbox=args.agentmail_inbox,
                limit=args.agentmail_limit,
            )
        )
    return adapters


def normalize(title: str) -> str:
    return re.sub(r"\s+", " ", title.strip()).lower()


def main() -> int:
    p = argparse.ArgumentParser(
        description="Audit whether Tally form submission notifications actually reach monitored inboxes."
    )
    p.add_argument("--days", type=int, default=10, help="lookback window in days (default: 10)")
    p.add_argument("--config", help="path to JSON config listing inboxes (see module docstring)")
    p.add_argument("--gmail-token", help="path to a Gmail OAuth token JSON (readonly scope is enough)")
    p.add_argument("--gmail-label", help="display label for the Gmail inbox (default: the token path)")
    p.add_argument("--agentmail-key", help="path to an AgentMail API key file")
    p.add_argument("--agentmail-inbox", help="AgentMail inbox address, e.g. agent@yourdomain.com")
    p.add_argument("--agentmail-label", help="display label for the AgentMail inbox (default: the inbox address)")
    p.add_argument("--agentmail-limit", type=int, default=200, help="max messages to page through per AgentMail inbox (default: 200)")
    p.add_argument(
        "--expect",
        action="append",
        default=[],
        metavar="FORM_TITLE",
        help="a form title that MUST show up in at least one inbox; repeatable. "
        "Matched case-insensitively as substring-or-equal against observed titles.",
    )
    p.add_argument("--json", action="store_true", help="emit machine-readable JSON instead of a table")
    args = p.parse_args()

    adapters: list[InboxAdapter] = []
    if args.config:
        adapters.extend(build_adapters_from_config(args.config))
    adapters.extend(build_adapters_from_flags(args))

    if not adapters:
        p.error("no inboxes configured — pass --config, or --gmail-token / --agentmail-key+--agentmail-inbox")

    since = datetime.now(timezone.utc) - timedelta(days=args.days)

    all_notifications: list[Notification] = []
    fetch_errors: list[str] = []
    for adapter in adapters:
        try:
            notes = adapter.fetch(since)
            all_notifications.extend(notes)
        except Exception as e:  # noqa: BLE001 — surface any adapter failure, keep going with the rest
            fetch_errors.append(f"{adapter.label}: {e}")
            print(f"[error] could not fetch from inbox '{adapter.label}': {e}", file=sys.stderr)

    if fetch_errors and len(fetch_errors) == len(adapters):
        print("All configured inboxes failed to fetch. Aborting.", file=sys.stderr)
        return 2

    # Per-inbox: distinct form titles seen, with latest arrival.
    per_inbox: dict[str, dict[str, datetime]] = {}
    for n in all_notifications:
        bucket = per_inbox.setdefault(n.inbox_label, {})
        if n.form_title not in bucket or n.timestamp > bucket[n.form_title]:
            bucket[n.form_title] = n.timestamp

    # Cross-inbox index for --expect matching.
    all_titles_normalized = {normalize(n.form_title): n.form_title for n in all_notifications}

    missing: list[str] = []
    for expected in args.expect:
        exp_norm = normalize(expected)
        hit = any(exp_norm in observed or observed in exp_norm for observed in all_titles_normalized)
        if not hit:
            missing.append(expected)

    if args.json:
        payload = {
            "window_days": args.days,
            "since": since.isoformat(),
            "inboxes": {
                label: [
                    {"form_title": title, "latest": ts.isoformat()}
                    for title, ts in sorted(titles.items(), key=lambda kv: kv[1], reverse=True)
                ]
                for label, titles in per_inbox.items()
            },
            "expected": args.expect,
            "missing": missing,
            "fetch_errors": fetch_errors,
        }
        print(json.dumps(payload, indent=2))
    else:
        print(f"Tally notification audit — last {args.days} day(s), since {since.date().isoformat()}\n")
        if not all_notifications:
            print("  (no Tally submission notifications found in any configured inbox)")
        for label, titles in per_inbox.items():
            print(f"[{label}]")
            if not titles:
                print("  (none)")
            for title, ts in sorted(titles.items(), key=lambda kv: kv[1], reverse=True):
                print(f"  {ts.isoformat(timespec='minutes')}  {title}")
            print()

        if args.expect:
            print("Expected-form check:")
            for expected in args.expect:
                status = "MISSING — zero notifications in any inbox" if expected in missing else "OK"
                print(f"  [{'FAIL' if expected in missing else ' ok '}] {expected}: {status}")
            print()

        if missing:
            print(f"FAILED: {len(missing)} expected form(s) had zero notifications anywhere in the last {args.days} day(s):")
            for m in missing:
                print(f"  - {m}")
            print("\nFix: in Tally, open the form's Settings > Notifications and add a monitored recipient. "
                  "Then re-submit a test entry and re-run this audit.")

    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
