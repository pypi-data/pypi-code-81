from time import sleep

from aidkitcli.core.report import Report
from aidkitcli.core.request_model import RequestModel
from aidkitcli.core.status import Status
from aidkitcli.data_access.analysis import (get_analysis_report, get_analysis_status, post_analysis)


class AnalysisFailed(Exception):
    def __init__(self, message="Execution of analysis failed."):
        self.message = message
        super().__init__(self.message)


def execute_analysis(request_model: RequestModel) -> Report:
    trigger_result = post_analysis(request_model=request_model)

    if not trigger_result:
        raise Exception('could not post analysis')

    analysis_id = trigger_result['id']

    def get_results(sleep_duration: int = 1) -> Report:
        try:
            status = get_analysis_status(analysis_id=analysis_id)
        except:
            sleep(sleep_duration)
            return get_results(sleep_duration=sleep_duration)

        if status in (Status.pending, Status.computing):
            return get_results()
        elif status is Status.done:
            result = get_analysis_report(analysis_id=analysis_id)
            return result
        else:
            raise AnalysisFailed()

    return get_results()
