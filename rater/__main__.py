"""Command line: python -m rater <validate|agreement|pairwise> <file.csv>"""

import sys

from .agreement import needs_met_report, pairwise_report
from .checks import load, validate


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) != 2 or argv[0] not in {"validate", "agreement", "pairwise"}:
        print(__doc__)
        return 2
    cmd, path = argv
    rows = load(path)

    if cmd == "validate":
        issues = validate(rows)
        for tid, who, level, msg in issues:
            print(f"[{level}] {tid} ({who}): {msg}")
        errors = sum(1 for i in issues if i[2] == "error")
        print(f"{len(rows)} rows, {errors} errors, {len(issues) - errors} warnings")
        return 1 if errors else 0

    if cmd == "agreement":
        r = needs_met_report(rows)
        print(f"Raters: {r['raters'][0]} vs {r['raters'][1]} on {r['tasks']} tasks")
        print(f"Exact agreement: {r['exact_agreement']:.0%}")
        print(f"Cohen's kappa:   {r['kappa']:.2f}")
        if r["disagree_by_2_or_more"]:
            print("Review (2+ steps apart): " + ", ".join(r["disagree_by_2_or_more"]))
        return 0

    r = pairwise_report(rows)
    print(f"{r['judgements']} judgements | A {r['A_share']:.0%} | B {r['B_share']:.0%} | same {r['same_share']:.0%}")
    print("Position bias suspected" if r["position_bias_flag"] else "No position bias detected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
