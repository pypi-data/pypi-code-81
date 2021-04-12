from stockx_wrapper import settings as st
from stockx_wrapper.products.product import Product
from stockx_wrapper.requester import requester
from stockx_wrapper.utils import split_number_into_chunks


class Products:

    @staticmethod
    def get_product_data(product_id, country='US', currency='USD'):
        """
        Get product data by product id.

        :param product_id: str
        :param country: str, optional
            Country for focusing market information.
        :param currency: str, optional
            Currency to get. Tested with 'USD' and 'EUR'.

        :return: Product
            Product info.
        """

        # Format url and get data
        url = f'{st.API_URL}/{st.GET_PRODUCT}/{product_id}'
        params = {
            'includes': 'market',
            'currency': currency,
            'country': country
        }
        data = requester.get(url=url, params=params)
        _product = data.get('Product')

        if _product:
            return Product(product_data=_product)

        return None

    def search_products(self, product_name, product_category=None, gender=None, year=None, retail_price=None,
                        shoe_size=None, country='US', currency='USD', market_lowest_ask=None, tags=None,
                        number_of_products=1, more_data=False):
        """
        Search by product name.

        :param product_name: str
        :param product_category: str, optional
            Category of product. For example, 'sneakers'.
        :param gender: str, optional
            Gender of the product. For example, 'women'.
        :param year: int, optional
            Year of release.
        :param retail_price: int, optional
            Filter by retail price. For example,    'lte-100' (less equal than 100),
                                                    'gte-200' (greater equal than 200),
                                                    'range(200|300) (between 200 and 300)
        :param shoe_size: int, optional
            Size of the shoe if a sneaker is asked.
        :param country: str, optional
            Country for focusing market information.
        :param currency: str, optional
            Currency to get. Tested with 'USD' and 'EUR'.
        :param market_lowest_ask: list of str, optional
            Filter by market lowest ask. Follows same schema as retail_price.
        :param tags: list of str, optional
            Tags to focus the search. For example, 'air jordan'.
        :param number_of_products: int, optional
            Number of hits to return.
        :param more_data: bool, optional
            If given, return data will be more exhaustive.

        :return: list of Products
            Product info.
        """

        # Number of hits is limited by default
        products_to_fetch = min(number_of_products, st.SEARCH_PRODUCTS_OLD_API_HITS_LIMIT)

        chunks = split_number_into_chunks(products_to_fetch, st.SEARCH_PRODUCTS_OLD_API_PRODUCTS_LIMIT)

        products = []

        for page, number_to_get in enumerate(chunks):
            # Format url and get data
            url = f'{st.API_URL}/{st.SEARCH_PRODUCTS}'
            params = {
                'page': page+1,
                '_search': product_name,
                '_tags': ','.join(tags) if tags else None,
                'productCategory': product_category,
                'gender': gender,
                'retailPrice': ','.join(retail_price) if retail_price else None,
                'year': year,
                'shoeSize': shoe_size,
                'currency': currency,
                'country': country,
                'market.lowestAsk': ','.join(market_lowest_ask) if market_lowest_ask else None,
                'dataType': 'product' if not product_category else None
            }
            data = requester.get(url=url, params=params)
            _products = data.get('Products')

            if not _products:
                break

            # Return first hit
            products.extend([self.get_product_data(product_id=product_data['id'], country=country, currency=currency)
                             if more_data else
                             Product(product_data=product_data)
                             for product_data in _products[:number_to_get]])

        return products

    def search_products_new_api(self, product_name, number_of_products=1, country='US', currency='USD', more_data=False):
        """
        Uses new API from Algolia.

        :param product_name: str
        :param number_of_products: int, optional
            Number of hits to return.
        :param country: str, optional
            Country for focusing market information.
        :param currency: str, optional
            Currency to get. Tested with 'USD' and 'EUR'.
        :param more_data: bool, optional
            If given, return data will be more exhaustive.

        :return: list of Products
            Product info.
        """

        # Number of hits is limited by default
        products_to_fetch = min(number_of_products, st.SEARCH_PRODUCTS_NEW_API_HITS_LIMIT)

        body = {
            'query': product_name,
            'facets': '*',
            'filters': '',
            "hitsPerPage": products_to_fetch,
        }

        data = requester.post(url=st.ALGOLIA_URL, body=body)
        products = data.get('hits')

        if not products:
            return []

        return [self.get_product_data(product_id=product_data['id'], country=country, currency=currency)
                if more_data else
                Product(product_data=product_data)
                for product_data in products]
