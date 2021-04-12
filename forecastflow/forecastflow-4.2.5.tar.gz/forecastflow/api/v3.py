import json
import logging
from typing import IO, Any, Dict, List, Optional, Union

import requests

from .. import config
from ..enums import DataSourceLabel, FileType
from ..exceptions import ForecastFlowError
from ..firebase_api import storage
from ..training import TrainingSettings

logger = logging.getLogger(__name__)


def _get(id_token: str, endpoint: str, params: Dict[str, Any]) -> Any:
    response = requests.get(
        f"{config.forecastflow['api_base_url']}/{endpoint}",
        params=params,
        headers={"Authorization": f"Bearer {id_token}"},
    )
    try:
        response_json = response.json()
    except ValueError:
        raise ForecastFlowError(response.text)
    raise_error_from_response(response_json)
    return response_json


def _post(id_token: str, endpoint: str, data: Dict[str, Any]) -> Any:
    response = requests.post(
        f"{config.forecastflow['api_base_url']}/{endpoint}",
        json=data,
        headers={"Authorization": f"Bearer {id_token}"},
    )
    try:
        response_json = response.json()
    except ValueError:
        raise ForecastFlowError(response.text)
    raise_error_from_response(response_json)
    return response_json


def raise_error_from_response(response: Dict[str, Any]):
    if response.get('status') not in (0, 200):
        raise ForecastFlowError(
            f'{response["error"]["reason"]}: {response["error"]["message"]}'
        )


def create_data_source(
    id_token: str,
    pid: str,
    name: str,
    label: DataSourceLabel,
    filetype: 'FileType',
    description: Optional[str] = None,
) -> str:
    """
    Create data source in project.
    NOTE: This function doesn't create profile.
    """
    response = _post(
        id_token,
        "v3/createdatasource",
        data={
            'idToken': id_token,
            'pid': pid,
            'name': name,
            'desc': description or '',
            'label': label.value,
            'type': filetype.value,
        },
    )
    logger.info('Successfully created data source')
    return response['message']['did']


def profile(
    id_token: str,
    pid: str,
    did: str,
):
    _post(
        id_token,
        "/v3/profile",
        data={'idToken': id_token, 'pid': pid, 'did': did},
    )
    logger.info('ForecastFlow profiler is starting')


def create_data_source_from_files(
    id_token: str,
    uid: str,
    pid: str,
    files: Union[List[str], List[IO]],
    filetype: 'FileType',
    name: str,
    label: DataSourceLabel,
    description: Optional[str] = None,
) -> str:
    """
    Create data source and profile from file
    """
    if len(files) > 999:
        raise ValueError('Too many files to create datasource.')
    did = create_data_source(
        id_token=id_token,
        pid=pid,
        name=name,
        label=label,
        filetype=filetype,
        description=description,
    )
    storage.upload_files_to_data_source(
        files=files, filetype=filetype, id_token=id_token, uid=uid, did=did
    )
    return did


def create_model(
    id_token: str,
    name: str,
    train_settings: Union[dict, 'TrainingSettings'],
    train_pid: str,
    train_did: str,
    test_pid: Optional[str] = None,
    test_did: Optional[str] = None,
    test_frac: Optional[float] = None,
    description: Optional[str] = None,
) -> str:
    if isinstance(train_settings, TrainingSettings):
        train_settings = train_settings.to_dict()
    if not isinstance(train_settings, dict):
        raise TypeError('train_settings must be dict or TrainingSettings')

    data: Dict[str, Any] = {
        'idToken': id_token,
        'name': name,
        'desc': description or '',
        'trainData': {'pid': train_pid, 'did': train_did},
        'trainSettings': train_settings,
    }

    if isinstance(test_frac, float):
        data['percentTest'] = int(100 * test_frac)
    elif test_pid is not None and test_did is not None:
        data['testData'] = {'pid': test_pid, 'did': test_did}
    else:
        raise ValueError('Lack of information for test data')

    response = _post(id_token, 'v3/createmodel', data=data)
    return response['mid']


def create_prediction(
    id_token: str,
    name: str,
    description: str,
    pid: str,
    did: str,
    mid: str,
    filetype: 'FileType',
) -> str:
    response = _post(
        id_token,
        'v3/createpredict',
        data={
            'idToken': id_token,
            'name': name,
            'desc': description,
            'did': did,
            'mid': mid,
            'pid': pid,
            'type': filetype.value,
        },
    )
    return response['rid']


def get_predict(id_token: str, uid: str, pid: str, rid: str) -> List[str]:
    response = _get(
        id_token,
        'v3/predict',
        params={'uid': uid, 'pid': pid, 'rid': rid},
    )
    return response['result']['uris']
