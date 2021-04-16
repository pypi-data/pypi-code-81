from craygraph import apply_with_kwargs

from .meta import Stage, StageModel, DataFlow
from .meta import Cache, NoCache

__all__ = [
  'GenericStage', 'GenericStageModel', 'stage',
  'dataflow'
]

class GenericStage(Stage):
  def __init__(self, f, *incoming, cache: Cache=NoCache(), name=None):
    self.f = f
    self.cache = cache

    super(GenericStage, self).__init__(*incoming, name=name)

  def load(self, **modes):
    return apply_with_kwargs(self.cache.load, **modes)

  def save(self, obj, **modes):
    return apply_with_kwargs(self.cache.save, obj, **modes)

  def get_output_for(self, *inputs, **modes):
    result = apply_with_kwargs(
      self.f, *inputs, **modes
    )
    return result

  def __matmul__(self, cache):
    return GenericStage(
      self.f, *self.incoming(), cache=cache, name=self.name
    )

class GenericStageModel(StageModel):
  def __init__(self, f, cache: Cache=NoCache(), name=None):
    self.f = f
    self.cache = cache
    self.name = name

  def __call__(self, *incoming):
    return GenericStage(self.f, *incoming, cache=self.cache, name=self.name)

  def __matmul__(self, cache):
    return GenericStageModel(
      self.f, cache=cache, name=self.name
    )

def stage(name=None, cache=NoCache()):
  def s(f):
    return GenericStageModel(f, cache=cache, name=name)
  return s

def dataflow(*definition):
  from .lang import achain
  return DataFlow(achain(*definition)())