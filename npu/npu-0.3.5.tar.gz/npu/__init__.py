"""
:synopsis: The main npu api
.. moduleauthor:: Naval Bhandari <naval@neuro-ai.co.uk>
"""


from .npu import api, predict, compile, train, export, upload_data, export_task_result, print
from . import vision, optim, loss, metrics
from .core import DataLoader
from .version import __version__, _module


api.__module__ = _module
predict.__module__ = _module
compile.__module__ = _module
train.__module__ = _module
export.__module__ = _module
export_task_result.__module__ = _module
upload_data.__module__ = _module
print.__module__ = _module
