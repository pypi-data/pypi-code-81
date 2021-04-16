import requests, json, datetime, logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(threadName)-11s %(levelname)-10s %(message)s")

class YamiController:
    """Controller da API Yami"""
    url = 'https://api.ymi.io'

    @classmethod
    def create_brand(self, token, account, brand):
        """Cria uma marca
        - Parametros:
        ---
            - token: str
            - account: str
            - brand: YamiBrand"""
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = f'Bearer {token}'

        r = requests.post(f'{self.url}/catalog/brand?an={account}', headers=headers, data=json.dumps(brand.__dict__))

        if r.status_code == 200 or r.status_code == 201:
            logging.info(f'Created Brand... [{r.status_code}] - {r.content.decode("utf-8")}')
            return json.loads(r.content.decode('utf8'))['brandId']
        else:
            logging.error(f'Failed to create Brand [{r.status_code}] - {r.content.decode("utf-8")}')

    @classmethod
    def create_category(self, token, account, category):
        """Cria uma categoria
        - Parametros:
        ---
            - token: str
            - account: str
            - category: YamiCategory"""
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = f'Bearer {token}'

        r = requests.post(f'{self.url}/catalog/category?an={account}', headers=headers, data=json.dumps(category.__dict__))

        if r.status_code == 200 or r.status_code == 201:
            logging.info(f'Created Category... [{r.status_code}] - {r.content.decode("utf-8")}')
            return json.loads(r.content.decode('utf8'))['idCategory']
        else:
            logging.error(f'Failed to create Category [{r.status_code}] - {r.content.decode("utf-8")}')

    @classmethod
    def update_product(self, token, account, productId, product):
        """Atualiza um produto
        - Parametros:
        ---
            - token: str
            - account: str
            - productId: str
            - product: YamiProduct"""
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = f'Bearer {token}'

        r = requests.put(f'{self.url}/catalog/product/{productId}?an={account}', headers=headers, data=json.dumps(product.__dict__))

        if r.status_code == 200 or r.status_code == 201:
            logging.info(f'Updated Product... [{r.status_code}] - {r.content.decode("utf-8")}')
            return json.loads(r.content.decode('utf8'))['productId']
        else:
            logging.error(f'Failed to update Product [{r.status_code}] - {r.content.decode("utf-8")}')

    @classmethod
    def create_product(self, token, account, product):
        """Cria um produto
        - Parametros:
        ---
            - token: str
            - account: str
            - product: YamiProduct"""
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = f'Bearer {token}'

        r = requests.post(f'{self.url}/catalog/product/?an={account}', headers=headers, data=json.dumps(product.__dict__))

        if r.status_code == 200 or r.status_code == 201:
            logging.info(f'Created Product... [{r.status_code}] - {r.content.decode("utf-8")}')
            return json.loads(r.content.decode('utf8'))['id']
        else:
            logging.error(f'Failed to create Product [{r.status_code}] - {r.content.decode("utf-8")}')

    @classmethod
    def update_variation(self, token, account, skuId, variation):
        """Atualiza uma variação do produto pai
        - Parametros:
        ---
            - token: str
            - account: str
            - skuId:
            - variation: YamiSKUProduct"""
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = f'Bearer {token}'

        r = requests.put(f'{self.url}/catalog/sku/{skuId}?an={account}', headers=headers, data=json.dumps(variation.__dict__))

        if r.status_code == 200 or r.status_code == 201:
            logging.info(f'Updated Product SKU Variation... [{r.status_code}] - {r.content.decode("utf-8")}')
            return json.loads(r.content.decode('utf8'))['skuId']
        else:
            logging.error(f'Failed to update Product SKU Variation [{r.status_code}] - {r.content.decode("utf-8")}')

    @classmethod
    def create_variation(self, token, account, variation):
        """Cria uma variação do produto pai
        - Parametros:
        ---
            - token: str
            - account: str
            - variation: YamiSKUProduct"""
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = f'Bearer {token}'

        r = requests.post(f'{self.url}/catalog/sku?an={account}', headers=headers, data=json.dumps(variation.__dict__))

        if r.status_code == 200 or r.status_code == 201:
            logging.info(f'Created Product SKU... [{r.status_code}] - {r.content.decode("utf-8")}')
            return json.loads(r.content.decode('utf8'))['skuId']
        else:
            logging.error(f'Failed to create Product SKU [{r.status_code}] - {r.content.decode("utf-8")}')

    @classmethod
    def create_specification_group(self, token, account, group):
        """Cria uma especificação para a variação
        - Parametros:
        ---
            - token: str
            - account: str
            - group: YamiSpecificationGroup"""
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = f'Bearer {token}'

        r = requests.post(f'{self.url}/catalog/specification_group?an={account}', headers=headers, data=json.dumps(group.__dict__))

        if r.status_code == 200 or r.status_code == 201:
            logging.info(f'Created Specification Group... [{r.status_code}] - {r.content.decode("utf-8")}')
            return json.loads(r.content.decode('utf8'))['specificationGroupId']
        else:
            logging.error(f'Failed to create Specification Group [{r.status_code}] - {r.content.decode("utf-8")}')

    @classmethod
    def create_specification_field(self, token, account, field):
        """Cria uma especificação para a variação
        - Parametros:
        ---
            - token: str
            - account: str
            - field: YamiSpecificationField"""
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = f'Bearer {token}'

        r = requests.post(f'{self.url}/catalog/specification_field?an={account}', headers=headers, data=json.dumps(field.__dict__))

        if r.status_code == 200 or r.status_code == 201:
            logging.info(f'Created Specification Field... [{r.status_code}] - {r.content.decode("utf-8")}')
            return json.loads(r.content.decode('utf8'))['fieldId']
        else:
            logging.error(f'Failed to create Specification Field [{r.status_code}] - {r.content.decode("utf-8")}')

    @classmethod
    def create_variation_specification(self, token, account, variationId, specification):
        """Cria uma especificação para a variação
        - Parametros:
        ---
            - token: str
            - account: str
            - variantionId: int
            - specification: YamiProductSpecification"""
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = f'Bearer {token}'

        specs = []
        for i in specification:
            specs.append(i.__dict__)

        r = requests.put(f'{self.url}/catalog/sku_specification/{variationId}?an={account}', headers=headers, data=json.dumps(specs))

        if r.status_code == 200 or r.status_code == 201:
            logging.info(f'Created Product SKU Specification... [{r.status_code}] - {r.content.decode("utf-8")}')
        else:
            logging.error(f'Failed to create Product SKU Specification [{r.status_code}] - {r.content.decode("utf-8")}')

    @classmethod
    def create_variation_image(self, token, account, variationId, images):
        """Cria uma imagem para a variação
        - Parametros:
        ---
            - token: str
            - account: str
            - variantionId: int
            - specification: YamiProductSpecification"""
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = f'Bearer {token}'

        dictImages = []
        for i in images:
            dictImages.append(i.__dict__)

        r = requests.put(f'{self.url}/catalog/sku_images/{variationId}?an={account}', headers=headers, data=json.dumps(dictImages))

        if r.status_code == 200 or r.status_code == 201:
            logging.info(f'Created Product SKU Image... [{r.status_code}] - {r.content.decode("utf-8")}')
        else:
            logging.error(f'Failed to create Product SKU Image [{r.status_code}] - {r.content.decode("utf-8")}')

    @classmethod
    def create_variation_inventory(self, token, account, warehouseId, variationId, inventory):
        """Atualiza o estoque da variação do produto
        - Parametros:
        ---
            - token: str
            - account: str
            - warehouseId: int
            - variationId: int
            - inventory: YamiInvetory"""
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = f'Bearer {token}'

        r = requests.put(f'{self.url}/catalog/inventory/{variationId}/{warehouseId}?an={account}', headers=headers, data=json.dumps(inventory.__dict__))

        if r.status_code == 200 or r.status_code == 201:
            logging.info(f'Created Product SKU Inventory... [{r.status_code}] - {r.content.decode("utf-8")}')
            return json.loads(r.content.decode('utf8'))['skuId']
        else:
            logging.error(f'Failed to create Product SKU Inventory [{r.status_code}] - {r.content.decode("utf-8")}')

    @classmethod
    def create_variation_price(self, token, account, variationId, price):
        """Atualiza o preço da variação do Produto
        - Parametros:
        ---
            - token: str
            - account: str
            - variationId: int
            - price: YamiPrice"""
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = f'Bearer {token}'

        r = requests.put(f'{self.url}/catalog/price/{variationId}?an={account}', headers=headers, data=json.dumps(price.__dict__))

        if r.status_code == 200 or r.status_code == 201:
            logging.info(f'Created Product SKU Price... [{r.status_code}] - {r.content.decode("utf-8")}')
            return json.loads(r.content.decode('utf8'))['skuId']
        else:
            logging.error(f'Failed to create Product SKU Price [{r.status_code}] - {r.content.decode("utf-8")}')

    @classmethod
    def get_skus(self, token, account):
        """Retorna todos os SKUs em um dicionário

        Ex.: print(YamiController.get_skus(yamiToken, account))
        - Parametros:
        ---
            - token: str
            - account: str"""
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = f'Bearer {token}'

        r = requests.get(f'{self.url}/catalog/skus?an={account}', headers=headers)

        if r.status_code == 200 or r.status_code == 201:
            return r.json()['skus']
        else:
            logging.error(f'Failed to get all SKU [{r.status_code}] - {r.content.decode("utf-8")}')