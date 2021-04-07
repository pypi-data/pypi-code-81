from moz_sql_parser.keywords import *

UNION_DISTINCT = Group(UNION + DISTINCT).set_parser_name("union_distinct")

reserved = [
    ALL,
    AND,
    AS,
    ASC,
    BETWEEN,
    BY,
    CASE,
    CAST,
    COLLATE,
    CROSS_JOIN,
    CROSS,
    # DATETIME_SUB, DATETIME_ADD, DATE_SUB, DATE_ADD, TIMESTAMP_SUB, TIMESTAMP_ADD,
    DESC,
    DISTINCT,
    ELSE,
    END,
    FALSE,
    FROM,
    FULL_JOIN,
    FULL_OUTER_JOIN,
    FULL,
    GROUP_BY,
    GROUP,
    HAVING,
    IN,
    INNER_JOIN,
    INNER,
    INTERVAL,
    IS_NOT,
    IS,
    JOIN,
    LEFT_JOIN,
    LEFT_OUTER_JOIN,
    LEFT,
    LIKE,
    LIMIT,
    NOCASE,
    NOT_BETWEEN,
    NOT_IN,
    NOT_LIKE,
    NOT_RLIKE,
    NOT,
    NULL,
    OFFSET,
    ON,
    OR,
    ORDER_BY,
    ORDER,
    OUTER,
    OVER,
    PARTITION_BY,
    PARTITION,
    RIGHT_JOIN,
    RIGHT_OUTER_JOIN,
    RIGHT,
    RLIKE,
    SELECT_DISTINCT,
    SELECT,
    THEN,
    TRUE,
    UNION_DISTINCT,
    UNION_ALL,
    UNION,
    USING,
    WHEN,
    WHERE,
    WITH,
    WITHIN_GROUP,
    WITHIN,
]

unions = [UNION_DISTINCT, UNION_ALL, UNION]

min_keys = {
    "cast": 2,
    "mul": 2,
    "div": 2,
    "mod": 2,
    "neg": 2,
    "add": 2,
    "sub": 2,
    "case": 2,
    "binary_not": 2,
    "binary_and": 2,
    "binary_or": 2,
    "timestamp_sub": 2,
    "timestamp_add": 2,
    "date_add": 2,
    "date_sub": 2,
    "datetime_sub": 2,
    "datetime_add": 2,
    "gte": 2,
    "lte": 2,
    "lt": 2,
    "gt": 2,
    "eq": 2,
    "neq": 2,
    "between": 2,
    "not_between": 2,
    "in": 2,
    "nin": 2,
    "is": 2,
    "like": 2,
    "not_like": 2,
    "rlike": 2,
    "not_rlike": 2,
    "similar_to": 2,
    "not_similar_to": 2,
}

durations = {
    "microseconds": "microsecond",
    "microsecond": "microsecond",
    "microsecs": "microsecond",
    "microsec": "microsecond",
    "useconds": "microsecond",
    "usecond": "microsecond",
    "usecs": "microsecond",
    "usec": "microsecond",
    "us": "microsecond",
    "milliseconds": "millisecond",
    "millisecond": "millisecond",
    "millisecon": "millisecond",
    "mseconds": "millisecond",
    "msecond": "millisecond",
    "millisecs": "millisecond",
    "millisec": "millisecond",
    "msecs": "millisecond",
    "msec": "millisecond",
    "ms": "millisecond",
    "seconds": "second",
    "second": "second",
    "secs": "second",
    "sec": "second",
    "s": "second",
    "minutes": "minute",
    "minute": "minute",
    "mins": "minute",
    "min": "minute",
    "m": "minute",
    "hours": "hour",
    "hour": "hour",
    "hrs": "hour",
    "hr": "hour",
    "h": "hour",
    "days": "day",
    "day": "day",
    "d": "day",
    "dayofweek": "dow",
    "dow": "dow",
    "weekday": "dow",
    "weeks": "week",
    "week": "week",
    "w": "week",
    "months": "month",
    "month": "month",
    "mons": "month",
    "mon": "month",
    "quarters": "quarter",
    "quarter": "quarter",
    "years": "year",
    "year": "year",
    "decades": "decade",
    "decade": "decade",
    "decs": "decade",
    "dec": "decade",
    "centuries": "century",
    "century": "century",
    "cents": "century",
    "cent": "century",
    "c": "century",
    "millennia": "millennium",
    "millennium": "millennium",
    "mils": "millennium",
    "mil": "millennium",
    "epoch": "epoch",
}
