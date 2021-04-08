import dimod
from jijcloud.client import JijCloudClient
from logging import getLogger
from typing import Type, TypeVar, Dict, Any
from jijcloud.response import APIStatus, BaseResponse
import time

logger = getLogger(__name__)

def post_instance_and_query(
        ResponseType: Type[TypeVar('ResponseType', bound='BaseResponse')],
        client: JijCloudClient,
        instance_type: str, instance: Dict[str, Any], solver: str, parameters: dict,
        sync: bool = True):
    
    # Instance を投げる
    logger.info("uploading instance ...")
    instance_id = client.post_instance(instance_type, instance)

    # Solverにqueryをなげる
    logger.info("submitting query ...")
    solver_res = client.submit_solve_query(solver, parameters, instance_id)
    logger.info("submitted to the queue")

    # 同期モードで解を取得
    status = 'PENDING'
    if sync:
        polling_count = 0
        while (status == APIStatus.PENDING.value) or (status == APIStatus.RUNNING.value):
            response = client.fetch_result(solver_res['solution_id'])
            status = response['status']
            if response['status'] == APIStatus.RUNNING.value:
                logger.info("running...")
            elif response['status'] == APIStatus.SUCCESS.value:
                break
            elif response['status'] == APIStatus.FAILED.value:
                return  ResponseType.empty_response(
                            APIStatus.FAILED,
                            client.url, client.token,
                            solver_res['solution_id'],
                            err_dict=response['solution'])

            elif response['status'] == APIStatus.UNKNOWNERROR.value:
                return ResponseType.empty_response(
                            APIStatus.UNKNOWNERROR,
                            client.url, client.token,
                            solver_res['solution_id'])

            time.sleep(2)
            polling_count = polling_count + 1

            if polling_count == 10:
                # show hints if polling is repeated certain times
                logger.info(f'It takes a lot of time to get the solution...')
                logger.info(f'Your solution_id is {solver_res["solution_id"]}.')
                logger.info(f'You can access the solution by')
                logger.info(f'>>> a = XXXSampler(config=...)')
                logger.info(f'>>> a.get_result("{solver_res["solution_id"]}")')

    else:
        return ResponseType.empty_response(
                    APIStatus.PENDING,
                    client.url, client.token,
                    solver_res['solution_id'])

    res_obj = ResponseType.from_json_obj(response['solution'])
    res_obj.set_status(APIStatus.SUCCESS)
    return res_obj
