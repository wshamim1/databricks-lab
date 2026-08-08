#!/usr/bin/env python3

import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


API_BASE_URL = os.environ.get("RETURNS_API_BASE_URL", "https://api.example.com/v1/returns")
API_TOKEN = os.environ.get("RETURNS_API_TOKEN", "")
START_TS = os.environ.get("START_TS", "2026-01-01T00:00:00Z")
END_TS = os.environ.get("END_TS", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
PAGE_SIZE = int(os.environ.get("PAGE_SIZE", "500"))
OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", "./landing/returns"))
SLEEP_MS = int(os.environ.get("SLEEP_MS", "200"))


def api_get(url: str) -> dict:
    headers = {"Accept": "application/json"}
    if API_TOKEN:
        headers["Authorization"] = f"Bearer {API_TOKEN}"

    req = urllib.request.Request(url=url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=60) as resp:
        payload = resp.read().decode("utf-8")
    return json.loads(payload)


def write_page(data: dict, page_number: int) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    page_file = OUTPUT_DIR / f"returns_page_{page_number:04d}.json"
    with page_file.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=True)


def build_first_url() -> str:
    query = urllib.parse.urlencode(
        {
            "updated_from": START_TS,
            "updated_to": END_TS,
            "page_size": PAGE_SIZE,
        }
    )
    return f"{API_BASE_URL}?{query}"


def main() -> int:
    next_url = build_first_url()
    page_number = 1
    total_records = 0

    while next_url:
        payload = api_get(next_url)
        write_page(payload, page_number)

        records = payload.get("data", [])
        total_records += len(records)

        next_token = payload.get("next_page_token")
        if next_token:
            query = urllib.parse.urlencode({"page_token": next_token, "page_size": PAGE_SIZE})
            next_url = f"{API_BASE_URL}?{query}"
            time.sleep(SLEEP_MS / 1000)
        else:
            next_url = ""

        print(f"Wrote page {page_number} with {len(records)} records")
        page_number += 1

    print(f"Completed API extraction. Total records: {total_records}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"API extraction failed: {exc}", file=sys.stderr)
        raise
