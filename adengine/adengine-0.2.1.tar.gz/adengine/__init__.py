import logging
import sys

logger = logging.getLogger('adengine')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)

logger.addHandler(handler)


__all__ = [
    'pt',
    'engine',
]
