"""Quality checks for rating files, the way a QA reviewer would read them."""

import csv

from .scales import FULLYM_ALLOWED, NEEDS_MET, PAGE_QUALITY, QUERY_TYPES, YMYL_TOPICS

REQUIRED = ["task_id", "rater", "query", "query_type", "topic", "result",
            "needs_met", "page_quality", "rationale"]


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate(rows):
    """Return a list of (task_id, rater, level, message)."""
    issues = []
    for i, r in enumerate(rows, start=2):
        tid = r.get("task_id") or f"row{i}"
        who = r.get("rater", "?")

        def add(level, msg):
            issues.append((tid, who, level, msg))

        missing = [c for c in REQUIRED if not (r.get(c) or "").strip()]
        if missing:
            add("error", "missing: " + ", ".join(missing))
            continue
        if r["query_type"] not in QUERY_TYPES:
            add("error", f"unknown query_type '{r['query_type']}'")
        if r["needs_met"] not in NEEDS_MET:
            add("error", f"unknown needs_met '{r['needs_met']}'")
            continue
        if r["page_quality"] not in PAGE_QUALITY:
            add("error", f"unknown page_quality '{r['page_quality']}'")
            continue

        if r["needs_met"] == "FullyM" and r["query_type"] not in FULLYM_ALLOWED:
            add("warning", f"FullyM on a '{r['query_type']}' query: one result rarely satisfies everyone")
        if r["topic"] in YMYL_TOPICS and r["page_quality"] in ("High", "Highest") \
                and r["needs_met"] in ("FailsM", "SM"):
            add("warning", "high page quality but fails the need: check that the page answers this query")
        if r["topic"] in YMYL_TOPICS and r["needs_met"] in ("HM", "FullyM") \
                and r["page_quality"] in ("Lowest", "Low"):
            add("warning", "YMYL topic: a low-quality page should not get HM/FullyM")
        if len(r["rationale"].split()) < 5:
            add("warning", "rationale too short to justify the rating")
    return issues
