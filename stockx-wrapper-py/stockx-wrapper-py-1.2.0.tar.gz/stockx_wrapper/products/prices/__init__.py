import datetime

from stockx_wrapper import settings as st
from stockx_wrapper.requester import requester


class Prices:

    def __init__(self, product_id):
        self.id = product_id

    def get_price_chart_data(self, start_date='all', end_date=datetime.date.today().strftime('%Y-%m-%d'),
                             intervals=100, country='US', currency='USD'):
        """
        Get product price chart. Average price over time.

        :param start_date: str, optional
            Has to be 'all' or 'YYYY-mm-dd' format.
        :param end_date: str, optional
            Has to be 'YYYY-mm-dd' format.
        :param intervals: str, optional
            Number of rows to get. Time between data returned decreases as this param increases.
        :param country: str, optional
            Country for focusing market information.
        :param currency: str, optional
            Currency to get. Tested with 'USD' and 'EUR'.

        :return: list of dicts

        """

        url = f'{st.API_URL}/{st.GET_PRODUCT}/{self.id}/{st.CHART_DATA}'
        params = {
            'start_date': start_date,
            'end_date': end_date,
            'intervals': intervals,
            'country': country,
            'currency': currency
        }
        data = requester.get(url=url, params=params)

        if not data:
            return None

        return_data = []

        for price, date_interval in zip(data['series'][0]['data'], data['xAxis']['categories']):
            return_data.append({
                'avgPrice': price,
                'dateInterval': date_interval
            })

        return return_data

    def get_price_sold_data(self, number_of_items=10, country='US', currency='USD'):
        """
        Get the last {number_of_items} sold prices.

        :param number_of_items: int
            It has to be less than 250 (Stockx API limit). If it's not, ignore it.
        :param country: str, optional
            Country for focusing market information.
        :param currency: str, optional
            Currency to get. Tested with 'USD' and 'EUR'.
        :return:
        """

        _number_of_items = min(number_of_items, st.SOLD_DATA_LIMIT)

        url = f'{st.API_URL}/{st.GET_PRODUCT}/{self.id}/{st.SOLD_DATA}'
        params = {
            'state': st.SOLD_STATE,
            'country': country,
            'currency': currency,
            'limit': _number_of_items,
            'page': 1,
            'sort': 'createdAt',
            'order': 'DESC'
        }

        data = requester.get(url=url, params=params)
        _prices = data.get('ProductActivity')

        return _prices
