#!/usr/bin/env python3
"""Snapshot a Luma event's registration funnel to one CSV row.

Counts are unrecoverable after the fact: Luma's dashboard shows current
totals only, with no historical breakdown by approval status. A "day
before doors" or "morning of" number only exists if something took the
snapshot at that moment. This script pulls the full guest list (handling
pagination), tallies guests by approval_status, and emits ONE row:

  iso_timestamp, event_id, event_name, approved, pending, waitlist,
  declined, invited, total, approval_rate

Usage:
  luma_snapshot.py --event-id evt-XXXXXXXXXXXX
  luma_snapshot.py --event-url https://luma.com/some-slug
  luma_snapshot.py --event-id evt-XXXX --append snapshots.csv
  luma_snapshot.py --event-id evt-XXXX --json

Auth: reads LUMA_API_KEY from the environment (the `x-luma-api-key`
header lane — the public API key, not a browser session cookie). Source
it yourself before running, e.g.:

  set -a; source /path/to/project/.env; set +a
  python3 luma_snapshot.py --event-id evt-XXXX --append log.csv

This script never reads a project's .env directly and has no fixed home
for its config — that's the consuming project's job. No event ids,
calendar ids, or output paths are hardcoded here.
"""
import argparse
import csv
import io
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime, timezone

API = "https://api.lu.ma/public/v1"
# Luma's WAF 403s a default urllib/requests TLS fingerprint regardless of
# UA header; shelling out to curl for both API and page fetches sidesteps it.
CURL_UA = "curl/8.4.0"
BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

# approval_status values observed from the live API -> CSV column.
# Anything not in this map still counts toward `total` but is bucketed as
# "other" and flagged on stderr rather than silently dropped or guessed at.
STATUS_MAP = {
    "approved": "approved",
    "pending_approval": "pending",
    "waitlist": "waitlist",
    "declined": "declined",
    "invited": "invited",
}

FIELDS = [
    "iso_timestamp", "event_id", "event_name",
    "approved", "pending", "waitlist", "declined", "invited",
    "total", "approval_rate",
]


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def api_key():
    key = os.environ.get("LUMA_API_KEY", "")
    if not key:
        die("LUMA_API_KEY not set in the environment. Source your "
            "project's .env first, e.g.: set -a; source .env; set +a")
    return key


def curl_json(url, key):
    out = subprocess.run(
        ["curl", "-s", "-w", "\n%{http_code}",
         "-H", f"x-luma-api-key: {key}", "-H", f"User-Agent: {CURL_UA}", url],
        capture_output=True, text=True, timeout=30,
    )
    if out.returncode != 0:
        die(f"curl failed ({out.returncode}): {out.stderr[:200]}")
    body, _, code = out.stdout.rpartition("\n")
    if code.strip() != "200":
        die(f"HTTP {code.strip()} from {url}\n{body[:300]}")
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        die(f"non-JSON response from {url}: {body[:300]}")


def resolve_event_id(event_url):
    """Resolve a public luma.com/<slug> URL to an evt-... id.

    There is no documented lookup-by-slug endpoint on the public API
    (calendar/lookup-event exists but expects an id already, not a slug —
    not usable for this). Instead, fetch the rendered public page and grep
    for the evt- id Luma embeds in its own markup — the same technique
    used to verify cover-image swaps propagated (see luma-event-write.md).
    """
    out = subprocess.run(
        ["curl", "-sL", "--compressed", "-A", BROWSER_UA, event_url],
        capture_output=True, text=True, timeout=30,
    )
    if out.returncode != 0:
        die(f"could not fetch {event_url}: {out.stderr[:200]}")
    m = re.search(r"evt-[A-Za-z0-9]+", out.stdout)
    if not m:
        die(f"could not find an evt- id on {event_url} — pass --event-id directly.")
    return m.group(0)


def get_event_name(event_id, key):
    d = curl_json(f"{API}/event/get?" + urllib.parse.urlencode({"id": event_id}), key)
    return d.get("event", {}).get("name", "")


def get_guest_statuses(event_id, key):
    statuses, cursor = [], None
    while True:
        q = {"event_api_id": event_id, "pagination_limit": 100}
        if cursor:
            q["pagination_cursor"] = cursor
        d = curl_json(f"{API}/event/get-guests?" + urllib.parse.urlencode(q), key)
        for e in d.get("entries", []):
            statuses.append(e.get("approval_status") or "")
        if d.get("has_more") and d.get("next_cursor"):
            cursor = d["next_cursor"]
            time.sleep(0.3)
        else:
            break
    return statuses


def build_row(event_id, key):
    name = get_event_name(event_id, key)
    statuses = get_guest_statuses(event_id, key)
    counts = {col: 0 for col in set(STATUS_MAP.values())}
    other = {}
    for s in statuses:
        col = STATUS_MAP.get(s)
        if col:
            counts[col] += 1
        else:
            key_ = s or "(blank)"
            other[key_] = other.get(key_, 0) + 1
    total = len(statuses)
    if other:
        print(f"warning: unmapped approval_status values seen: {other} "
              f"— counted in total, not in any named column. Verify against "
              f"the live API; Luma's status enum isn't publicly documented.",
              file=sys.stderr)
    row = {
        "iso_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "event_id": event_id,
        "event_name": name,
        "total": total,
        "approval_rate": round(counts["approved"] / total, 4) if total else "",
    }
    row.update(counts)
    return row


def csv_line(row):
    buf = io.StringIO()
    csv.writer(buf).writerow([row[f] for f in FIELDS])
    return buf.getvalue().rstrip("\r\n")


def append_row(row, path):
    is_new = not os.path.exists(path) or os.path.getsize(path) == 0
    with open(path, "a", newline="") as f:
        w = csv.writer(f)
        if is_new:
            w.writerow(FIELDS)
        w.writerow([row[f] for f in FIELDS])
    print(f"appended to {path}", file=sys.stderr)


def main():
    p = argparse.ArgumentParser(
        description="Snapshot a Luma event's registration funnel to one CSV row.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--event-id", help="evt-... id")
    src.add_argument("--event-url", help="public luma.com/<slug> URL; resolved to an event id")
    p.add_argument("--append", metavar="FILE",
                    help="append the row to FILE (CSV header written if the file is new/empty)")
    p.add_argument("--json", action="store_true",
                    help="print the row as JSON on stdout instead of a CSV line")
    args = p.parse_args()

    key = api_key()
    event_id = args.event_id or resolve_event_id(args.event_url)
    row = build_row(event_id, key)

    if args.append:
        append_row(row, args.append)

    if args.json:
        print(json.dumps(row, indent=2))
    else:
        print(csv_line(row))


if __name__ == "__main__":
    main()
