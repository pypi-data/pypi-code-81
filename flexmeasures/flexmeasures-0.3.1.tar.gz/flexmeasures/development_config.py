SQLALCHEMY_DATABASE_URI = "postgresql://a1:a1dev@127.0.0.1/a1"
# SQLALCHEMY_ECHO = True

LOGGING_LEVEL = "INFO"

MAIL_SERVER = "w01a109a.kasserver.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = "a1-bvp@seita.nl"
MAIL_DEFAULT_SENDER = ("FlexMeasures", "no-reply@seita.nl")
MAIL_PASSWORD = "Yf75c854813a6fbcb7d5bf13702a"

CORS_ORIGINS = ["null"]  # to allow local HTML files access

DARK_SKY_API_KEY = "38d0bf8e538f023f053f42fc16638daa"
MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw"

# FLEXMEASURES_PLATFORM_NAME = "BeeVeePee"
FLEXMEASURES_MODE = "demoo"
FLEXMEASURES_PUBLIC_DEMO_CREDENTIALS = ("nic at bla.com", "superpass")
FLEXMEASURES_TASK_CHECK_AUTH_TOKEN = "dev-token"
# Staging: 0
# Demo: 1
# Live: 2
# Play: 3
# seita.fm live: 4
# Nic dev: 10
# Felix dev: 11
FLEXMEASURES_REDIS_URL = "52.144.45.80"
FLEXMEASURES_REDIS_PORT = 6379
FLEXMEASURES_REDIS_DB_NR = 1  # Redis per default has 16 databases, [0-15]
FLEXMEASURES_REDIS_PASSWORD = "D0lEyyf4QCKZ"

SECURITY_PASSWORD_SALT = (
    "$2b$1327VlhOJrcPjFYdxWix07pNO"  # "$2b$1224VchOCrdnjFYdCWhx07pEO"
)
