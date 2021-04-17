# pylint: skip-file
import asyncio
import os

import ioc
import unimatrix.runtime


SECRET_STORAGE_BACKENDS = {
    'default': {
        'class': 'unimatrix.ext.secrets.loaders.google.GoogleSecretLoader',
        'prefetch': True,
        'options': {
            'project': os.getenv('GOOGLE_TEST_PROJECT')
        }
    }
}

os.environ['UNIMATRIX_SETTINGS_MODULE'] = __name__


if __name__ == '__main__':
    unimatrix.runtime.on.sync('boot')
    repo = ioc.require('SecretRepository')
    print(repo.get('default-signing-key'))
