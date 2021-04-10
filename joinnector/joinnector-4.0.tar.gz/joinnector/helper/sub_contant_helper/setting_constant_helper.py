SERVICE_NAME = "nectorsdk"

API_PROD_BASE_URL = "https://platform.nector.io"
API_DEV_BASE_URL = "https://devplatform.nector.io"

API_BASE_HEADER = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-source": "web"
}

API_MAP = {
    "coupon": {
        "create": {"endpoint": "/coupons", "prefix": "/api/v2/merchant",  "has_signature": True},
        "get": {"endpoint": "/coupons/{id}", "prefix": "/api/v2/merchant", },
        "fetch": {"endpoint": "/coupons", "prefix": "/api/v2/merchant", }
    },
    "currency": {
        "get": {"endpoint": "/currencies/{id}", "prefix": "/api/v2/merchant", },
        "fetch": {"endpoint": "/currencies", "prefix": "/api/v2/merchant", }
    },
    "deal": {
        "reward": {"endpoint": "/dealrewards", "prefix": "/api/v2/merchant",  "has_signature": True},
        "get": {"endpoint": "/deals/{id}", "prefix": "/api/v2/merchant", },
        "fetch": {"endpoint": "/deals", "prefix": "/api/v2/merchant", }
    },
    "lead": {
        "create": {"endpoint": "/leads", "prefix": "/api/v2/merchant",  "has_signature": True},
        "get": {"endpoint": "/leads/{id}", "prefix": "/api/v2/merchant", },
        "save": {"endpoint": "/leads/{id}", "prefix": "/api/v2/merchant",  "has_signature": True},
    },
    "notification": {
        "get": {"endpoint": "/notifications/{id}", "prefix": "/api/v2/merchant", },
        "fetch": {"endpoint": "/notifications", "prefix": "/api/v2/merchant", }
    },
    "review": {
        "create": {"endpoint": "/reviews", "prefix": "/api/v2/merchant",  "has_signature": True},
        "get": {"endpoint": "/reviews/{id}", "prefix": "/api/v2/merchant", },
        "save": {"endpoint": "/reviews/{id}", "prefix": "/api/v2/merchant",  "has_signature": True},
        "delete": {"endpoint": "/reviews/{id}", "prefix": "/api/v2/merchant", },
        "fetch": {"endpoint": "/reviews", "prefix": "/api/v2/merchant", }
    },
    "setting": {
        "get": {"endpoint": "/settings/{id}", "prefix": "/api/v2/merchant", }
    },
    "swap": {
        "create": {"endpoint": "/swaps", "prefix": "/api/v2/merchant",  "has_signature": True},
        "get": {"endpoint": "/swaps/{id}", "prefix": "/api/v2/merchant", },
        "fetch": {"endpoint": "/swaps", "prefix": "/api/v2/merchant", }
    },
    "task": {
        "get": {"endpoint": "/tasks/{id}", "prefix": "/api/v2/merchant", },
        "fetch": {"endpoint": "/tasks", "prefix": "/api/v2/merchant", }
    },
    "taskactivity": {
        "create": {"endpoint": "/taskactivities", "prefix": "/api/v2/merchant",  "has_signature": True},
        "get": {"endpoint": "/taskactivities/{id}", "prefix": "/api/v2/merchant", },
        "fetch": {"endpoint": "/taskactivities", "prefix": "/api/v2/merchant", }
    },
    "wallet": {
        "create": {"endpoint": "/wallets", "prefix": "/api/v2/merchant",  "has_signature": True},
        "get": {"endpoint": "/wallets/{id}", "prefix": "/api/v2/merchant", },
        "fetch": {"endpoint": "/wallets", "prefix": "/api/v2/merchant", }
    },
    "wallettransaction": {
        "create": {"endpoint": "/wallettransactions", "prefix": "/api/v2/merchant",  "has_signature": True},
        "get": {"endpoint": "/wallettransactions/{id}", "prefix": "/api/v2/merchant", },
        "fetch": {"endpoint": "/wallettransactions", "prefix": "/api/v2/merchant", }
    }
}
