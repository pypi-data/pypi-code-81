from functools import reduce


def _extract_grouped_data(data: str, key: str):
    # example data: Average_price_per_tonne:106950.5556;1991:-;1992:-
    return reduce(lambda prev, curr: {
        **prev,
        **{curr.split(':')[0]: curr.split(':')[1]}
    }, data.split(';'), {})[key] if data is not None and len(data) > 1 else None
