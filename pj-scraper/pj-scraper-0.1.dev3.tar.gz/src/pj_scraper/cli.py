from .scraper import Scraper


def main():
    s = Scraper()
    products = s.get_all_products_from_category("smartklokker", no_pages=1)
    sellers_and_prices = s.get_sellers_and_prices_of_product_list(
        products["Product number"]
    )
    print(sellers_and_prices.head())
