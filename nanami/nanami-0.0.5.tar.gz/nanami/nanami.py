
import sys
from pathlib import Path

from nanami.utils import *

class Nanami(object):
    def __init__(self, image, workspace, entrypoint, gpus='', argument='', cache=False, queue_id=None):
        self.image = image

        self.workspace = Path(workspace).absolute()
        self._check_workspace()

        self.container_entrypoint = join('/workspace', entrypoint)
        self.entrypoint = join(self.workspace, entrypoint)
        self._check_entrypoint()

        self.requirements = join(self.workspace, 'requirements.txt')
        self._check_requirements()
        self.argument = argument
        self.command = f"python {self.container_entrypoint} {argument}"
        self.setup_command = f"pip install -r {join('/workspace', 'requirements.txt')}"

        self.gpus = gpus
        self.device_requests = gpu_check(gpus=gpus, verbose=False)
        self.cache = cache
        self.queue_id = queue_id
        self._check_image()

    def _check_entrypoint(self):
        if not exists(self.entrypoint):
            raise FileNotFoundError(self.entrypoint)
        if not check_entrypoint(self.entrypoint):
            raise NotImplementedError(f"Can't find nanami.start() and nanami.end() in {self.entrypoint}.")

    def _check_requirements(self):
        _requirements = join(self.workspace, 'requirements.txt')
        if exists(_requirements):
            with open(_requirements) as f:
                _requirements_list = f.read().splitlines()
            logger.info(f'Found requirements.txt: {_requirements_list}')
        else:
            logger.info('Not found requirements.txt')

    def _check_workspace(self):
        if not exists(self.workspace):
            raise FileNotFoundError(self.workspace)

    def _check_image(self):
        if not image_search(image=self.image):
            raise NotImplementedError(f"{self.image} is not found.")

    def save(self, apikey, port):
        if sys.platform == 'linux':
            localhost = f"http://127.0.0.1:{port}"
        elif sys.platform == "darwin":
            localhost = f'http://host.docker.internal:{port}'

        with open(join(self.workspace, 'nanami.json'), 'w') as fp:
            json.dump({
                'apikey': apikey,
                'queue_info' : {
                    'queue_id': self.queue_id,
                    'image': self.image,
                    'workspace': str(self.workspace),
                    'entrypoint': str(self.entrypoint),
                    'gpus': self.gpus,
                    'argument': self.argument,
                    'cache': self.cache,
                },
                'localhost': localhost
            }, fp, indent=4)