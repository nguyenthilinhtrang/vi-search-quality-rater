"""Rating scales used in search quality and AI response evaluation.

The names follow the public Google Search Quality Rater Guidelines
(Needs Met and Page Quality), plus a simple pairwise preference scale
used in AI response comparison tasks.
"""

NEEDS_MET = ["FailsM", "SM", "MM", "HM", "FullyM"]
PAGE_QUALITY = ["Lowest", "Low", "Medium", "High", "Highest"]
PAIRWISE = ["A_much_better", "A_better", "same", "B_better", "B_much_better"]

# Query types (user intent) used for Vietnamese queries.
QUERY_TYPES = [
    "know",          # wants information, may need several sources
    "know_simple",   # one short, correct answer exists
    "do",            # wants to complete a task (download, buy, book)
    "website",       # wants one specific website or page
    "visit_in_person",  # wants a nearby place
]

# FullyM is reserved for queries where one result can satisfy almost
# every user: a specific website, a single fact, or one nearby place.
FULLYM_ALLOWED = {"know_simple", "website", "visit_in_person"}

# Topics where a wrong answer can hurt health, money or safety.
YMYL_TOPICS = {"health", "finance", "legal", "safety", "news"}


def ordinal(scale, label):
    """Return the position of a label in its scale (0 = worst)."""
    return scale.index(label)
