"""
TASK AUTOMATION — Script 3
Goal: Fetch the <title> of a fixed webpage and save it to a file.
Concepts: requests, re (or html.parser), file handling
"""

import re
import os
import json
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


# ── Lightweight title extractor (no third-party deps) ────────────────────────
TITLE_PATTERN = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def fetch_page_title(url: str, timeout: int = 10) -> str:
    """
    Download the HTML at `url` and return the text inside <title>…</title>.
    Falls back to the URL itself if no title is found.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; TitleBot/1.0; "
            "+https://example.com/bot)"
        )
    }

    req = Request(url, headers=headers)

    try:
        with urlopen(req, timeout=timeout) as response:
            # Read only the first 32 KB — enough for the <head>
            raw = response.read(32_768).decode("utf-8", errors="replace")
    except HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code} — {exc.reason} for URL: {url}") from exc
    except URLError as exc:
        raise RuntimeError(f"URL error: {exc.reason}") from exc

    match = TITLE_PATTERN.search(raw)
    if not match:
        return "(no <title> found)"

    # Collapse whitespace and decode common HTML entities
    title = match.group(1).strip()
    title = re.sub(r"\s+", " ", title)
    for entity, char in [("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                          ("&quot;", '"'), ("&#39;", "'"), ("&nbsp;", " ")]:
        title = title.replace(entity, char)
    return title


def scrape_and_save(url: str, output_file: str) -> dict:
    """
    Fetch the page title from `url` and append a JSON record to `output_file`.

    Args:
        url:         The webpage URL to scrape.
        output_file: Path to the results file (JSON-Lines format).

    Returns:
        A dict with 'url', 'title', and 'timestamp'.
    """
    print(f"[→] Fetching: {url}")
    title = fetch_page_title(url)
    print(f"[✓] Title found: {title!r}")

    record = {
        "url":       url,
        "title":     title,
        "timestamp": datetime.now().isoformat(),
    }

    # Append to file (JSON-Lines — one JSON object per line)
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    with open(output_file, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"[✓] Record saved to: {output_file!r}")
    return record


def batch_scrape(urls: list[str], output_file: str) -> list[dict]:
    """
    Scrape titles for multiple URLs and save all results.
    """
    results = []
    for url in urls:
        try:
            record = scrape_and_save(url, output_file)
            results.append(record)
        except Exception as exc:
            error_record = {
                "url":       url,
                "title":     None,
                "error":     str(exc),
                "timestamp": datetime.now().isoformat(),
            }
            results.append(error_record)
            print(f"[✗] Failed: {exc}")
    return results


# ── Demo / quick test ────────────────────────────────────────────────────────
if __name__ == "__main__":
    import tempfile

    URLS_TO_SCRAPE = [
        "https://www.wikipedia.org",
        "https://example.com",
        "https://python.org",
    ]

    with tempfile.TemporaryDirectory() as tmp:
        out_path = os.path.join(tmp, "scraped_titles.jsonl")

        print("=== Script 3 — Scrape Page Titles ===\n")
        records = batch_scrape(URLS_TO_SCRAPE, out_path)

        print("\n─── Results ───")
        for rec in records:
            status = "✓" if rec.get("title") else "✗"
            print(f"  [{status}] {rec['url']}")
            print(f"       → {rec.get('title') or rec.get('error')}")

        print("\n─── Output file (.jsonl) ───")
        with open(out_path) as f:
            for line in f:
                print(" ", line.rstrip())