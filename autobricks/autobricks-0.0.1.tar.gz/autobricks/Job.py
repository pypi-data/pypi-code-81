from .ApiUtils import (
    api_get,
    api_post,
    base64_decode,
    base64_encode,
    format_path_for,
    OS as OsEnum,
)
import json
import os
from uuid import UUID, uuid4
import time
import datetime
import logging

endpoint = "jobs"
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(f"autobricks.{endpoint}")


def job_run_get(run_id: int):

    try:
        response = api_get(endpoint, "runs/get", query=f"run_id={run_id}")
    except Exception as e:
        response = {"run_id": -1, "message": str(e)}

    return response


def job_runs_list():

    response = api_get(endpoint, "runs/list")

    return response


def job_run_delete(run_id: int):
    data = {"run_id": run_id}
    try:
        response = api_post(endpoint, "runs/delete", data)
    except Exception as e:
        response = {}

    return response


def job_run_submit(
    notebook_path: str,
    run_name: str = "default",
    spark_version: str = "7.3.x-scala2.12",
    node_type_id: str = "Standard_DS3_v2",
    driver_node_type_id: str = "Standard_DS3_v2",
    num_workers: int = 1,
    timeout_seconds: int = 900,
    idempotency_token: UUID = None,
    cluster_id: str = None,
):

    fmt_notebook_path = format_path_for(notebook_path, OsEnum.LINUX)

    data = {
        "notebook_task": {"notebook_path": fmt_notebook_path},
        "run_name": run_name,
        "libraries": [],
        "timeout_seconds": timeout_seconds,
    }

    if cluster_id:
        logger.info(
            f"Configuring job {fmt_notebook_path} to run on existing cluster {cluster_id}"
        )
        data["existing_cluster_id"] = cluster_id

    else:
        logger.info(
            f"Configuring job {fmt_notebook_path} to run on a new cluster {node_type_id}"
        )
        data["new_cluster"] = {
            "spark_version": spark_version,
            "node_type_id": node_type_id,
            "driver_node_type_id": driver_node_type_id,
            "num_workers": num_workers
            # "autotermination_minutes": autotermination_minutes
        }

    if idempotency_token:
        data["idempotency_token"] = str(idempotency_token)

    logger.info(f"Submitting job for notebook {fmt_notebook_path}")
    return api_post(endpoint, "runs/submit", data)


def job_run_notebook(
    notebook_path: str,
    name: str = "default",
    idempotency_token: UUID = None,
    cluster_id: str = None,
    wait_seconds: int = 5,
):

    fmt_notebook_path = format_path_for(notebook_path, OsEnum.LINUX)

    start_time = time.time()
    response = job_run_submit(
        fmt_notebook_path,
        name,
        idempotency_token=idempotency_token,
        cluster_id=cluster_id,
    )

    run_id = response["run_id"]
    previous_state = {"run_id": run_id}

    logger.info(f"Notebook {fmt_notebook_path} job has start on run {run_id}")

    try:
        run_page_url = None

        while True:

            response = job_run_get(run_id)

            state = response["state"]
            life_cycle_state = response["state"]["life_cycle_state"]
            run_page_url = response["run_page_url"]

            if state != previous_state:
                logger.info(
                    f"Notebook:{fmt_notebook_path} State:{life_cycle_state} Url:{run_page_url}"
                )
                previous_state = state

            time.sleep(wait_seconds)

            if life_cycle_state == "TERMINATED":
                break

    except Exception as e:
        msg = f"Notebook:{fmt_notebook_path} State:ERROR Url:{run_page_url} Message:{str(e)}"
        logger.error(msg)
        raise Exception(msg)

    return state
