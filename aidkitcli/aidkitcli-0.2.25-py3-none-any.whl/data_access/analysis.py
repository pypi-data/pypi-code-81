from typing import Dict

from aidkitcli.core.request_model import RequestModel
from aidkitcli.data_access.api import RESTApi


def post_analysis(request_model: RequestModel) -> Dict[str, int]:
    """Post and trigger analysis in aidkit cloud."""
    api = RESTApi()
    return api.post_pipeline_from_dict(toml_dict=request_model.dict)
