# vi-search-quality-rater

A small toolkit and Claude Code skill for **rating Vietnamese search results and AI responses**, and for **quality-checking rating data** the way a QA reviewer would.

Built by Nguyen Thi Linh Trang, SEO specialist (3+ years) and English Language graduate, to practise the evaluation work behind search engines and AI models.

## What it does

| Part | Purpose |
|---|---|
| `skill/vi-search-quality-rater/SKILL.md` | A Claude Code skill: how to rate a Vietnamese query's results (Needs Met, Page Quality, YMYL) and compare two AI answers |
| `python -m rater validate` | Finds missing fields, illegal labels and rule breaks (e.g. FullyM on a broad query, high rating on a low-quality health page) |
| `python -m rater agreement` | Exact agreement and Cohen's kappa between two raters, plus tasks they rated 2+ steps apart |
| `python -m rater pairwise` | A/B preference share and a position-bias flag for pairwise comparison tasks |

Scales follow the concepts in Google's public [Search Quality Rater Guidelines](https://guidelines.raterhub.com/searchqualityevaluatorguidelines.pdf). No private guidelines or client data are used.

## Quick start

Python 3.8+, standard library only.

```bash
git clone https://github.com/nguyenthilinhtrang/vi-search-quality-rater.git
cd vi-search-quality-rater
python -m rater validate data/sample_ratings.csv
python -m rater agreement data/sample_ratings.csv
python -m rater pairwise data/sample_pairwise.csv
python -m unittest -v
```

Sample output:

```
Raters: rater_a vs rater_b on 8 tasks
Exact agreement: 62%
Cohen's kappa:   0.50
```

## Use the skill in Claude Code

```bash
cp -r skill/vi-search-quality-rater ~/.claude/skills/
```

Then ask Claude, for example: *"Rate these 3 results for the query 'triệu chứng sốt xuất huyết'"* or *"Which answer is better, A or B?"*.

## Data format

`ratings.csv`: `task_id, rater, query, query_type, topic, result, needs_met, page_quality, rationale`
`pairwise.csv`: `task_id, rater, prompt, preference, rationale`

All sample queries and results in `data/` are written by the author for demonstration.

## License

MIT
