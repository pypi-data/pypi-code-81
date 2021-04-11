import json

import pandas as pd
import requests
from bs4 import BeautifulSoup


class Scraper:
    """ Main class for scraping prisjakt """

    base_url = "https://www.prisjakt.no/"

    def get_sellers_and_prices_of_product_list(self, products: pd.Series):
        """Get a full table of all sellers and prices for a list of products

        Args:
            products: A list of the products

        Returns:
            A dataframe with all products, sellers and prices
        """

        out = pd.DataFrame()
        for product in products:
            try:
                out = out.append(self.get_sellers_and_prices_of_product(product))
            except:
                pass
        return out

    def get_all_products_from_category(
        self, category: str, no_pages: int = 10, prods_per_site: int = 36
    ) -> pd.Series:
        """Get all products from a category

        Args:
            category: Category name from url. Example: 'mobiltelefoner' which points to 'prisjakt.no/c/mobiltelefoner'
            no_pages: Amount of pages in the category to scrape
            prods_per_site: Products per site

        Returns:
            A dataframe with columns "Product name" and "Product number"
        """

        category_url = self.base_url + "c/" + category

        out = pd.DataFrame()
        for page_no in range(0, no_pages):
            soup = self._get_soup(category_url + f"?offset={prods_per_site*page_no}")
            out = out.append(self.get_products_from_page(soup))
        return out

    def get_products_from_page(self, soup: BeautifulSoup) -> pd.DataFrame:
        """Get products from a single page

        Args:
            soup: A bs4 soup of given page

        Return:
            A dataframe with columns "Product name" and "Product number"
        """
        prods = soup.select("a[class*='ProductLink']")
        return pd.DataFrame(
            {
                "Product name": [prod.attrs["aria-label"] for prod in prods],
                "Product number": [
                    prod.attrs["href"][prod.attrs["href"].index("=") + 1 :]
                    for prod in prods
                ],
            }
        )

    def get_sellers_and_prices_of_product(self, product_number: str) -> pd.DataFrame:
        """Get sellers and prices of product

        Args:
            product_number: Product number from url. Example: '5172022' which points to 'prisjakt.no/product.php?p=5172022'

        Returns:
            A dataframe with columns "Seller name" and "Price"
        """

        soup = self._get_soup(self.base_url + "product.php?p=" + product_number)

        info_raw = None
        for script in soup.find_all("script"):
            try:
                if script["data-script"] == "globals":
                    info_raw = script
                    break
            except:
                pass

        if info_raw:
            info_split = info_raw.string.split(',{"__typename":"Price",')[1:]
            info_split = [seller for seller in info_split if "variants" in seller[-30:]]
            out = pd.DataFrame()
            for info in info_split:
                temp_df = pd.DataFrame()
                current = json.loads("{" + info)
                try:
                    temp_df["price_id"] = [current["id"]]
                    temp_df["seller_product_name"] = [current["name"]]
                    temp_df["stock_status"] = [current["stock"]["status"]]
                    temp_df["price_incl_shipping"] = [current["price"]["inclShipping"]]
                    temp_df["price_excl_shipping"] = [current["price"]["exclShipping"]]
                    temp_df["seller_id"] = [current["store"]["id"]]
                    temp_df["seller_name"] = [current["store"]["name"]]
                    temp_df["seller_rating"] = [
                        current["store"]["userReviewSummary"]["rating"]
                    ]
                    out = out.append(temp_df)
                except:
                    pass
            out["product_number"] = product_number
            return out
        else:
            return None

    def _get_soup(self, url, parser="html.parser"):
        """ Make request and parse to bs4 soup """
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content.decode("unicode-escape"), parser)
            return soup
        except:
            raise
