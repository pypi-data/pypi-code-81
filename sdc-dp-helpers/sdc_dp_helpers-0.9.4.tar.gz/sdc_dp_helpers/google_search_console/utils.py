from datetime import timedelta, datetime


def phrase_to_date(phrase):
    """
    Takes a typical phrase such as "3_days_ago" and returns a
    date based on that phrase.
    :phrase: str. Something like 3_days_ago or 25_days_ago etc.
    :return: '%Y-%m-%d'
    """
    try:
        date_delta = int(phrase.split('_')[0])
        return (datetime.now() - timedelta(days=date_delta)).strftime('%Y-%m-%d')
    except ValueError as err:
        raise ValueError(f'Phrasing for date: {phrase} is not valid, '
                         f'try something like: 3_days_ago') from err


def date_range(start_date, end_date, delta=timedelta(days=1)):
    """
    The range is inclusive, so both start_date and end_date will be returned.
    :start_date: The datetime object representing the first day in the range.
    :end_date: The datetime object representing the second day in the range.
    :delta: A datetime.timedelta instance, specifying the step interval. Defaults to one day.
    Yields:
        Each datetime object in the range.
    """

    if start_date == 'today':
        start_date = datetime.now().strftime('%Y-%m-%d')
    elif start_date == 'yesterday':
        start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    elif '_days_ago' in start_date:
        start_date = phrase_to_date(start_date)
    else:
        raise ValueError('StartDate requires a valid input '
                         'such as "today", "yesterday" or "<int>_days_ago".')

    if end_date == 'today':
        end_date = datetime.now().strftime('%Y-%m-%d')
    elif end_date == 'yesterday':
        end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    elif '_days_ago' in end_date:
        end_date = phrase_to_date(end_date)
    else:
        raise ValueError('EndDate requires a valid input '
                         'such as "today", "yesterday" or "<int>_days_ago".')

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    current_date = start_date
    while current_date <= end_date:
        yield current_date.strftime('%Y-%m-%d')
        current_date += delta


def un_nest_keys(data, col, key_list, value_list):
    """
    A simple method that takes a set of keys and values
    from a dataset with dimensions and replaces them
    with key value pairs.

    :data: The dataset that needs to be un_nested.
    :col: The key name of the dimensions.
    :key_list: List of keys.
    :value_list: List of Values.

    returns:
        So dataset A:
            {'keys': [1, 2, 3]}
        Can become:
            {'key1': 1, 'key2': 2, 'key3': 3}
    """
    data.update(
        dict(zip(key_list, value_list))
    )
    del data[col]
    return data
