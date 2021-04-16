from lumipy.navigation.atlas import Atlas
import pandas as pd
import os
import json
from test.unit.utilities.temp_file_manager import TempFileManager

from lumipy.client import Client


def get_atlas_test_data():
    file_dir = os.path.dirname(os.path.abspath(__file__))
    test_data_dir = file_dir + '/data/'
    return pd.read_csv(test_data_dir+'test_atlas.csv')


def make_test_atlas():

    atlas_df = get_atlas_test_data()

    sample_secrets = {
        "api": {
            "tokenUrl": "sample",
            "username": "sample",
            "password": "sample",
            "clientId": "sample",
            "clientSecret": "sample",
            "apiUrl": "sample",
            "lumiApiUrl": "sample"
        }
    }

    secrets_file = TempFileManager.create_temp_file(sample_secrets)

    client = Client(secrets_path=secrets_file.name)

    provider_descriptions = client.build_provider_defs(atlas_df)

    TempFileManager.delete_temp_file(secrets_file)

    return Atlas(
        provider_descriptions,
        atlas_type='All available data providers'
    )


def assert_locked_lockable(test_case, instance):

    from lumipy.common.lockable import Lockable
    test_case.assertTrue(issubclass(type(instance), Lockable))

    with test_case.assertRaises(TypeError) as ar:
        instance.new_attribute = 'some new attribute'
    e = str(ar.exception)

    str1 = "Can't change attributes on "
    str2 = "they are immutable."
    test_case.assertTrue(str1 in e)
    test_case.assertTrue(str2 in e)

    test_case.assertFalse(hasattr(instance, 'new_attribute'))


def standardise_sql_string(sql_str):
    return " ".join(sql_str.split())


def load_secrets_into_env_if_local_run():

    if 'LOCAL_INT_TEST_SECRETS_PATH' in os.environ:
        path = os.environ['LOCAL_INT_TEST_SECRETS_PATH']
        env_var_map = {
            'lumiApiUrl': 'FBN_LUMI_API_URL',
            'tokenUrl': 'FBN_TOKEN_URL',
            'username': 'FBN_USERNAME',
            'password': 'FBN_PASSWORD',
            'clientId': 'FBN_CLIENT_ID',
            'clientSecret': 'FBN_CLIENT_SECRET'
        }

        os.environ['FBN_DRIVE_API_URL'] = 'https://fbn-ci.lusid.com/drive/'
        with open(path, 'r') as f:
            creds = json.load(f)['api']
            for k1, k2 in env_var_map.items():
                os.environ[k2] = creds[k1]
