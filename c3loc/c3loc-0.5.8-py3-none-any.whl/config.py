from binascii import unhexlify
import os
from uuid import UUID

CONFIG = {
    'DB_NAME': os.getenv('DB_NAME', ''),
    'DB_USER': os.getenv('DB_USER', 'c3loc'),
    'DB_PASSWORD': os.getenv('DB_PASSWORD', 'c3letmein'),
    'DB_HOST': os.getenv('DB_HOST', ''),
    'LA_UUID': os.getenv('LA_UUID', UUID(bytes=b'c3wirelesslocanc')),
    'API_RESULT_LIMIT': int(os.getenv('API_RESULT_LIMIT', 100)),
    'LOCATION_UPDATE_MS': 1000,
    'MAX_FRAME_SIZE': int(os.getenv('MAX_FRAME_SIZE', 5 * 1024 * 1024)),  # 5MiB
    'SSR_KEY': unhexlify(os.getenv('SSR_KEY', b'c3wirelesslocanc'.hex())),
    'STATS_INTERVAL': int(os.getenv('STATS_INTERVAL', 60)),
    'MAX_DB_CONNECTIONS': int(os.getenv('MAX_DB_CONNECTIONS', 4)),
    'MAX_QUEUED_PACKETS': int(os.getenv('MAX_QUEUED_PACKETS', 100)),
    'LAST_SEEN_RESOLUTION_SECS': int(os.getenv('LAST_SEEN_RESOLUTION_SECS', 5)),
}
