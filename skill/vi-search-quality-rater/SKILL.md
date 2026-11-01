---
name: vi-search-quality-rater
description: Rate Vietnamese search results and compare AI responses using the public Search Quality Rater Guidelines concepts (Needs Met, Page Quality, YMYL) and a pairwise preference scale. Use when the user gives a Vietnamese query with results or two AI answers and asks which is better, or asks to QA a rating file.
---

# Vietnamese search & AI response rater

## 1. Read the query like a Vietnamese user
- Decide the query type: `know`, `know_simple`, `do`, `website`, `visit_in_person`.
- Note locale signals: city names, slang, missing diacritics ("thoi tiet ha noi" = "thời tiết Hà Nội"), current year.
- If the query has several meanings, list them and rate against the most likely one first.

## 2. Rate each search result
- **Needs Met** (FailsM < SM < MM < HM < FullyM): how well this result satisfies the user.
  - FullyM only for `know_simple`, `website` or `visit_in_person` queries.
  - Outdated facts (wrong year, old prices, old schedules) lower the rating.
- **Page Quality** (Lowest < Low < Medium < High < Highest): purpose, expertise, trust, reputation.
  - Health, finance, legal, safety and news topics (YMYL) need clear authorship and sources.
  - A YMYL page with no owner, license or source is Lowest, however well written.
- Write one rationale sentence of at least 5 words that names the evidence.

## 3. Compare two AI responses (pairwise)
Scale: `A_much_better`, `A_better`, `same`, `B_better`, `B_much_better`.
Check in this order and stop at the first clear difference:
1. Safety: does one give risky medical, financial or legal advice?
2. Accuracy: wrong or outdated facts.
3. Completeness: does it answer every part of the prompt?
4. Vietnamese quality: natural wording, correct diacritics, right tone (formal vs casual).
5. Length and format: shorter wins when both are correct.
Ignore which answer comes first; position must not affect the choice.

## 4. QA a rating file
Run the toolkit in this repo:
```
python -m rater validate ratings.csv   # missing fields, illegal labels, rule warnings
python -m rater agreement ratings.csv  # exact agreement, Cohen's kappa, tasks 2+ steps apart
python -m rater pairwise pairwise.csv  # A/B share and position-bias flag
```
Report errors first, then warnings, then the tasks raters should discuss.
