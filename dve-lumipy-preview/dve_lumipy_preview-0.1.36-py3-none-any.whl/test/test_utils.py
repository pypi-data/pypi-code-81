from lumipy.navigation.atlas import Atlas
import pandas as pd
import os
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
