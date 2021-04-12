from stockx_wrapper.products.prices import Prices


class Product:

    def __init__(self, product_data):
        self.parent_id = product_data.get('parentId', None)
        self.id = product_data.get('id', None)
        self.style_id = product_data.get('styleId', None)
        self.name = product_data.get('name', None)
        self.full_name = product_data.get('title', None)
        self.description = product_data.get('description', None)
        self.brand = product_data.get('brand', None)
        self.retail_price = product_data.get('retailPrice', None)
        self.category = product_data.get('productCategory', None)
        self.shoe_size = product_data.get('shoeSize', None)
        self.media = product_data.get('media', None)
        self.market = product_data.get('market', None)
        self.children = product_data.get('children', None)

        self.prices = Prices(product_id=self.id)

    def get_specific_size(self, size):
        """
        Iterate through product children searching for specific size.

        :param size: str
            Size in US format (Ex: 9)

        :return: Product
            Product data.
        """

        if self.children:
            child_data = next((child for child in self.children.values() if child['shoeSize'] == size), None)

            if child_data:
                return Product(product_data=child_data)

        return None
