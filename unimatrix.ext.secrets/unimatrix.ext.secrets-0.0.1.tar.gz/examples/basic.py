import asyncio
import os

import ioc
import unimatrix.runtime
import unimatrix.ext.secrets as secrets
from unimatrix.ext.secrets.__boot__ import setup_ioc


setup_ioc()
secrets.setup({
    'default': {
        'class': 'unimatrix.ext.secrets.loaders.google.GoogleSecretLoader',
        'prefetch': True,
        'options': {
            'project': os.getenv('GOOGLE_TEST_PROJECT')
        }
    }
})

if __name__ == '__main__':
    repo = ioc.require('SecretRepository')
    asyncio.run(repo.prefetch())
    print(repo.get('default-signing-key'))
