"""Agreement between raters and bias checks for pairwise tasks."""

from collections import Counter, defaultdict

from .scales import NEEDS_MET, PAIRWISE, ordinal


def cohen_kappa(a, b):
    """Cohen's kappa for two equal-length label lists."""
    if len(a) != len(b) or not a:
        raise ValueError("need two non-empty lists of the same length")
    n = len(a)
    observed = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    expected = sum(ca[k] * cb[k] for k in set(a) | set(b)) / (n * n)
    if expected == 1:
        return 1.0
    return (observed - expected) / (1 - expected)


def pair_up(rows, field="needs_met"):
    """Group labels by task for the two raters who rated the most tasks together."""
    by_task = defaultdict(dict)
    for r in rows:
        by_task[r["task_id"]][r["rater"]] = r[field]
    raters = Counter(k for labels in by_task.values() for k in labels)
    if len(raters) < 2:
        raise ValueError("need at least two raters")
    r1, r2 = [k for k, _ in raters.most_common(2)]
    shared = [t for t, labels in by_task.items() if r1 in labels and r2 in labels]
    return r1, r2, shared, by_task


def needs_met_report(rows):
    r1, r2, shared, by_task = pair_up(rows)
    a = [by_task[t][r1] for t in shared]
    b = [by_task[t][r2] for t in shared]
    far = [t for t in shared
           if abs(ordinal(NEEDS_MET, by_task[t][r1]) - ordinal(NEEDS_MET, by_task[t][r2])) >= 2]
    return {
        "raters": (r1, r2),
        "tasks": len(shared),
        "exact_agreement": sum(x == y for x, y in zip(a, b)) / len(shared),
        "kappa": cohen_kappa(a, b),
        "disagree_by_2_or_more": far,
    }


def pairwise_report(rows):
    """Position bias: a fair rater should not pick A far more often than B."""
    counts = Counter(r["preference"] for r in rows if r.get("preference") in PAIRWISE)
    total = sum(counts.values())
    a_side = counts["A_much_better"] + counts["A_better"]
    b_side = counts["B_much_better"] + counts["B_better"]
    return {
        "judgements": total,
        "A_share": a_side / total if total else 0.0,
        "B_share": b_side / total if total else 0.0,
        "same_share": counts["same"] / total if total else 0.0,
        "position_bias_flag": total >= 10 and abs(a_side - b_side) / total > 0.3,
    }
