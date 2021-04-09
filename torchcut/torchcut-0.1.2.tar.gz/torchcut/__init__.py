import warnings
import importlib

imports = {
    'mandatory': {
        'torch': {
            'torch': 'torch',
            'torch.nn': 'nn',
            'torch.nn.functional': 'F',
            'torch.optim': 'optim'
        }
    },
    'optional': {
        'torchvision': {
            'torchvision': 'tv',
            'torchvision.transforms': 'transforms',
        },
        'torchtext': {
            'torchtext': 'tt'
        },
        'numpy': {
            'numpy': 'np'
        },
        'pandas': {
            'pandas': 'pd'
        }
    }
}


def do_imports(definitions, ignore_import_error=False):
    for name, mapping in definitions.items():
        try:
            for package, import_as in mapping.items():
                globals()[import_as] = importlib.import_module(package)
        except ImportError:
            if ignore_import_error:
                warnings.warn('{} is not installed and won\'t be available.'.format(name))


do_imports(imports['mandatory'], ignore_import_error=False)
do_imports(imports['optional'], ignore_import_error=True)


# Setting __all__ explicitly is nasty but required as auto-completion will otherwise not recognize imports.
# In case of PyCharm, might be related to https://youtrack.jetbrains.com/issue/PY-8307.
__all__ = [
    'torch', 'nn', 'F', 'optim',  # torch
    'tv', 'transforms',  # torchvision
    'tt',  # torchtext
    'np', 'pd'  # others
]