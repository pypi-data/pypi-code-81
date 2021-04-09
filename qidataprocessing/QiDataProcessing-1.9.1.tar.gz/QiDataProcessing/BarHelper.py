from QiDataProcessing.BarProvider import BarProvider


def gen_bar_series(org_bar_series, instrument_manager, instrument_id, begin_date, end_date, interval, bar_type):
    """
    根据源生K线按照指定的Interval进行切分
    """
    bar_provider = BarProvider()
    bar_provider.create_bar_provider_by_date(instrument_manager, instrument_id, begin_date, end_date, interval, bar_type)
    for bar in org_bar_series:
        bar_provider.add_bar(bar)

    bar_series = bar_provider.bar_series
    return bar_series
