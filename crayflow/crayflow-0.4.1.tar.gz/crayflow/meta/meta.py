from collections import namedtuple

from craygraph import Node, NodeModel
from craygraph import get_incoming, dynamic_propagate
from craygraph import apply_with_kwargs

__all__ = [
  'Cache', 'NoCache',
  'Stage', 'StageModel',
  'DataFlow'
]

class Flow(object):
  def __call__(self, *args, **kwargs):
    raise NotImplementedError()

  def outputs(self):
    raise NotImplementedError()


class Cache(object):
  def __rmatmul__(self, other):
    from .common import GenericStageModel
    return GenericStageModel(f=other, cache=self)

  def __rlshift__(self, other):
    from .common import GenericStageModel
    return GenericStageModel(f=other, cache=self)

  def __rrshift__(self, other):
    from .common import GenericStageModel
    return GenericStageModel(f=other, cache=self)

  def load(self):
    raise NotImplementedError()

  def save(self, obj):
    raise NotImplementedError()

class NoCache(Cache):
  def __init__(self):
    pass

  def load(self):
    raise FileNotFoundError()

  def save(self, obj):
    pass

no_cache = NoCache()

class Stage(Node):
  def __init__(self, *incoming, name=None):
    super(Stage, self).__init__(*incoming, name=name)

  def load(self):
    raise FileNotFoundError()

  def save(self, obj):
    raise FileNotFoundError()

  def get_output_for(self, *args):
    raise NotImplementedError()

class StageModel(NodeModel):
  pass

Maybe = namedtuple('Maybe', ['value', 'success'])

class DataFlow(object):
  def __init__(
    self,
    outputs,
    get_output=lambda node, args, kwargs: apply_with_kwargs(node.get_output_for, *args, **kwargs),
    load=lambda node, kwargs: apply_with_kwargs(node.load, **kwargs),
    save=lambda node, obj, kwargs: apply_with_kwargs(node.save, obj, **kwargs)
  ):
    self._outputs = outputs
    self._get_output = get_output
    self._load = load
    self._save = save

  def outputs(self):
    if isinstance(self._outputs, (tuple, list)):
      return self._outputs
    else:
      return (self._outputs, )

  def __call__(self, **kwargs):
    def _get_incoming(node : Stage):
      try:
        result = self._load(node, kwargs)
        return tuple(), Maybe(result, True)
      except (KeyError, FileNotFoundError, NotImplementedError):
        return get_incoming(node), Maybe(None, False)

    def get_output(node : Stage, args, result : Maybe):
      if result.success:
        return result.value
      else:
        value = self._get_output(node, args, kwargs)
        try:
          self._save(node, value, kwargs)
        except (KeyError, FileNotFoundError, NotImplementedError):
          pass

        return value

    if isinstance(self._outputs, (list, tuple)):
      result = dynamic_propagate(get_output, self._outputs, incoming=_get_incoming)
      return tuple(result[output] for output in self._outputs)
    else:
      result = dynamic_propagate(get_output, (self._outputs, ), incoming=_get_incoming)
      return result[self._outputs]