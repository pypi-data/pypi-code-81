#
#  Copyright (c) 2018-2019 Renesas Inc.
#  Copyright (c) 2018-2019 EPAM Systems Inc.
#
import json
import sys

import importlib_resources as pkg_resources
import requests
from colorama import Fore, Style

from aos_signer.service_config.service_configuration import ServiceConfiguration
from aos_signer.signer.user_credentials import UserCredentials


def run_upload():
    config = ServiceConfiguration('meta/config.yaml')
    uc = UserCredentials(config)
    uc.find_upload_key_and_cert()

    upload_data = {'service': config.publish.service_uid}
    version = config.publish.version

    if version:
        upload_data['version'] = version

    server_certificate = pkg_resources.files('aos_signer') / 'files/1rootCA.crt'
    with pkg_resources.as_file(server_certificate) as server_certificate_path:
        resp = requests.post(
            'https://{}:10000/api/v1/services/versions/'.format(config.publish.url),
            files={'file': open('service.tar.gz', 'rb')},
            data=upload_data,
            cert=(uc.upload_cert_path, uc.upload_key_path),
            verify=server_certificate_path)

    if resp.status_code == 201:
        print(Fore.GREEN + 'Upload DONE.' + Style.RESET_ALL)
        sys.exit(0)
    else:
        print('{}Server returned error while uploading:{}'.format(Fore.RED, Style.RESET_ALL))
        try:
            errors = json.loads(resp.text)
            for key, value in errors.items():
                print(f'   {key}: {value}')
        except Exception:
            print(resp.text)
        sys.exit(1)
