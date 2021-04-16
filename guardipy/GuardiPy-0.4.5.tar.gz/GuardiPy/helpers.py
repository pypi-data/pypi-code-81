""" Internal helper objects. """
import logging
from datetime import datetime, timedelta


def epoch_ms_to_datetime(epoch_milliseconds: int = None) -> datetime:
    """
        This converts an integer representing Epoch time milliseconds (native timestamp used by GC API) to a Python-
        native DateTime object.
    """
    if epoch_milliseconds is None:
        epoch_milliseconds = 0
    epoch_time = epoch_milliseconds / 1000
    time = datetime.fromtimestamp(epoch_time)
    return time


def datetime_to_epoch_ms(dt: datetime) -> int:
    epoch_time = dt.timestamp()
    epoch_ms = epoch_time * 1000
    return int(epoch_ms)


class CentraApiPayload:  # TODO - Pagination wrapper; query (CentraObject.*.list(sort_*)) wrapper.
    """
        Context object that describes how a given entity/object should be queried through the API.
        Specifically, HTTP method; URL; Query string parameters (and a workaround for them in get_querystring_params);
        request payload/data; and what class/object type to return when parsing the response.

        This object is meant to be fed into Centra.execute()
    """

    def get_querystring_params(self):
        """ Default Python requests behavior takes iterable qs param values, and declares them multiple times.

            ie {'test': [1,2]} will be ?test=1&test=2
            GuardiCore Centra's API expects ?test=1,2.

            Besides styles, also handles various other type constraints, such as epoch millisec for timestamps. """

        remapped = {}  # Seed query parameter dict.

        for k, v in self.params.items():
            if isinstance(v, timedelta):  # if time delta, get integer of current epoch millisec vs that delta
                epoch_value = int((datetime.utcnow() + v).timestamp() * 1000)
                remapped[k] = epoch_value

            elif isinstance(v, datetime):  # if a datetime, get integer of that time as epoch millisec
                remapped[k] = int(v.timestamp() * 1000)

            elif isinstance(v, (list, tuple)):  # if a list or tuple, convert to comma delimited string basically.
                logging.debug(f"Re-formatting total of {len(v)} values for querystring parameter '{k}'.")
                formatted_value = ",".join(str(qs_value) for qs_value in v)
                logging.debug(f"end result is:  {formatted_value}")  # end result would be ?test=1,2
                remapped[k] = formatted_value

            else:
                remapped[k] = v

        return remapped

    def __init__(self,
                 return_type,
                 path: str = "/CentraObjectName",
                 method: str = "GET",
                 params: dict = None,
                 data: dict = None,
                 response_pagination: bool = True):
        self.path = path
        self.method = method
        self.params: dict = params or dict()
        self.data: dict = data or dict()
        self.return_type = return_type
        self.response_pagination = response_pagination


class CentraApiExportable(CentraApiPayload):
    """
        This context can be passed to Centra.export() method instead of Centra.execute().
        This method extends regular .execute() to include the URL suffix used for getting a raw CSV export.
        Additionally, the view_name is used to so we can query for the export task status.

        Here, __init__() is a re-declare of CentraApiPayload with additional parameters for exportability.
            This is done instead of a super().__init__(**kwargs) so that type hinting still applies.
    """

    def __init__(self,
                 return_type,
                 path: str = "/CentraObjectName",
                 export_suffix: str = "/export",
                 export_view_name: str = "exportable",
                 method: str = "GET",  # TODO - GET only supported method as of now... More TBD...
                 params: dict = None,
                 data: dict = None):

        super().__init__(return_type=return_type, path=path, method=method, params=params, data=data)
        self.export_suffix: str = export_suffix
        self.export_view_name: str = export_view_name


class CentraExportResults:
    """
        This object is returned from calling Centra.export() and is used to deliver the CSV payload but also
        metadata about the export process.
    """

    def __init__(
            self,
            csv: str,
            author_username: str,
            author_description: str,
            records_written: int,
            csv_guid: str,
            task_guid: str
    ):
        self.csv = csv
        self.author_username = author_username
        self.author_description = author_description
        self.records_written = records_written
        self.csv_guid = csv_guid
        self.task_guid = task_guid


class CentraEntity:
    """
        Base type for objects you can interact with through the Centra API. Used for type hints.
    """
    _path: str
    _export_suffix: str
    _export_view_name: str
