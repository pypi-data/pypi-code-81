from dataclasses import dataclass

from .._version import VERSION

# Same naming scheme as our widgets.
# Keep in sync with convertQueryResultToWidgetMimeType in widgetMimeType.ts.
CONVERT_QUERY_RESULT_TO_WIDGET_MIME_TYPE = f"application/vnd.atoti.convert-query-result-to-widget.v{VERSION.split('.')[0]}+json"


@dataclass(frozen=True)
class WidgetConversionDetails:
    mdx: str
    session_name: str
    widget_creation_code: str
