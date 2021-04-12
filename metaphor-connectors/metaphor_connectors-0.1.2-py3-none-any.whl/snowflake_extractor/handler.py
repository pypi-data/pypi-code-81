try:
    import unzip_requirements
except ImportError:
    pass

from metaphor.common.handler import handle_api
from metaphor.snowflake_extractor import SnowflakeExtractor, SnowflakeRunConfig


def handle(event, context):
    return handle_api(event, context, SnowflakeRunConfig, SnowflakeExtractor)
