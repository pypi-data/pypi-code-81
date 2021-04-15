from typing import Dict

from aidkitcli.core.report import Report
from aidkitcli.core.request_model import RequestModel
from aidkitcli.core.status import Status
from aidkitcli.data_access.api import RESTApi


def post_analysis(request_model: RequestModel) -> Dict:
    """Post and trigger analysis in aidkit cloud."""
    api = RESTApi()
    return api.post_pipeline_from_dict(toml_dict=request_model.dict)


def get_analysis_status(analysis_id: int) -> Status:
    api = RESTApi()
    status_dict = api.get_status(analysis_id=analysis_id)
    status = Status(status_dict.get('status', 'pending'))
    return status


def get_analysis_report(analysis_id: int) -> Report:
    api = RESTApi()
    report = api.get_report(analysis_id=analysis_id)
    return report
