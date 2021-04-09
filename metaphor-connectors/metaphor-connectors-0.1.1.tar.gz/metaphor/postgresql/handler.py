try:
    import unzip_requirements
except ImportError:
    pass

from metaphor.common.handler import handle_api
from metaphor.postgresql import PostgresqlExtractor, PostgresqlRunConfig


def handle(event, context):
    return handle_api(event, context, PostgresqlRunConfig, PostgresqlExtractor)
