from __future__ import absolute_import
import os
from .resnet34 import Resnet34
from orientation_recognition.utils.tools import get_cfg,download_url

__model_factory = {
    # face detection models
    'resnet-34': Resnet34,
}


_model_urls = {
    'resnet-34': '1yfONEwolcK-PMC27kurn__SqRF2-htlE',
}

_data_urls = {
    'sample': '1pQ3CUfhMQts1YEgu1QmkGSO9UlMz7KHU'
}

def show_avai_models():
    """Displays available models.

    Examples::
        >>> from orientation_recognition import models
        >>> models.show_avai_models()
    """
    print(list(__model_factory.keys()))


def build_model(name: str, cfg_path: str = ""):
    """A function wrapper for building a model.

    Args:
        name (str): model name
        cfg_path (str): path to config file
    Returns:
        model instance.
    """
    avai_models = list(__model_factory.keys())
    if name not in avai_models:
        raise KeyError(
            'Unknown model: {}. Must be one of {}'.format(name, avai_models)
        )
    if not len(cfg_path):
        raise RuntimeError(
            'Please input the path config file'
        )
    # Load config file
    config = get_cfg(cfg_path)

    # Check the models are existed or not
    if not os.path.exists('training/models'):
        os.makedirs("training/models")
        download_url(_model_urls['resnet-34'], name='resnet-34', dst = "training/models")
        
    if not os.path.exists('training/train'):
        os.makedirs("training/train")
        download_url(_data_urls['sample'],name='sample', dst='training')

    return __model_factory[name](config)
