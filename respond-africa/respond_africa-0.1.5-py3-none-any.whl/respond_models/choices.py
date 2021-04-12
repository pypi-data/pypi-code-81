from edc_constants.constants import FASTING, NEVER, NON_FASTING

from .constants import MORE_THAN_HALF, NEARLY_EVERYDAY, NOT_AT_ALL, SEVERAL_DAYS

MISSED_PILLS = (
    ("today", "today"),
    ("yesterday", "yesterday"),
    ("earlier_this_week", "earlier this week"),
    ("last_week", "last week"),
    ("lt_month_ago", "less than a month ago"),
    ("gt_month_ago", "more than a month ago"),
    (NEVER, "have never missed taking my study pills"),
)

PHQ_CHOICES = (
    (NOT_AT_ALL, "Not at all"),
    (SEVERAL_DAYS, "Several days"),
    (MORE_THAN_HALF, "More than half the days"),
    (NEARLY_EVERYDAY, "Nearly everyday"),
)

FASTING_CHOICES = ((FASTING, "Fasting"), (NON_FASTING, "Non-fasting"))
