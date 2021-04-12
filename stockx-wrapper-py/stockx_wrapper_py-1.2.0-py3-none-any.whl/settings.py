# Urls
API_URL = 'https://stockx.com/api'
ALGOLIA_URL = (
    "https://xw7sbct9v6-dsn.algolia.net/1/indexes/products/query?x-algolia-agent=Algolia for JavaScript (4.8.6); "
    "Browser "
)

# End points
GET_PRODUCT = 'products'
SEARCH_PRODUCTS = 'browse'
CHART_DATA = 'chart'
SOLD_DATA = 'activity'

# Algolia headers
ALGOLIA_HEADERS = {
    'x-algolia-api-key': 'ZTEwZjZhMzE3NWRiNDRkMTBkYWQ1NjRkMDA2MmI3NGNlYjZkNTNhM2RjZDRmZTI0YmEyZjEzM2Y2MGE4NzAxYnZhbGlkVW50aWw9MTYxNzY1NDEwOA==',
    'x-algolia-application-id': 'XW7SBCT9V6'
}

# Limits
SOLD_DATA_LIMIT = 250

SEARCH_PRODUCTS_OLD_API_PRODUCTS_LIMIT = 40
SEARCH_PRODUCTS_OLD_API_PAGES_LIMIT = 25
SEARCH_PRODUCTS_OLD_API_HITS_LIMIT = SEARCH_PRODUCTS_OLD_API_PRODUCTS_LIMIT*SEARCH_PRODUCTS_OLD_API_PAGES_LIMIT

SEARCH_PRODUCTS_NEW_API_HITS_LIMIT = 1000

# States
SOLD_STATE = 480
