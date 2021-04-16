from craygraph import apply_with_kwargs
from .meta import Stage, StageModel, DataFlow
from .meta import Cache, NoCache

__all__ = [
  'stage',
  'dataflow'
]

class ConfigurableStage(Stage):
  def __init__(self, f, *incoming, cache: Cache=NoCache(), name=None):
    self.f = f
    self.cache = cache

    super(ConfigurableStage, self).__init__(*incoming, name=name)

  def load(self, **modes):
    return apply_with_kwargs(self.cache.load, **modes)

  def save(self, obj, **modes):
    return apply_with_kwargs(self.cache.save, obj, **modes)

  def get_output_for(self, *inputs, **modes):
    return self.f(*inputs, **modes)

  def __matmul__(self, cache):
    return ConfigurableStage(
      self.f, *self.incoming(), cache=cache, name=self.name
    )

class ConfigurableStageModel(StageModel):
  def __init__(self, f, cache: Cache=NoCache(), name=None):
    self.f = f
    self.cache = cache
    self.name = name

  def __call__(self, *incoming):
    return ConfigurableStage(self.f, *incoming, cache=self.cache, name=self.name)

  def __matmul__(self, cache):
    return ConfigurableStageModel(
      self.f, cache=cache, name=self.name
    )

def stage(name=None, cache=NoCache()):
  def s(f):
    return ConfigurableStageModel(f, cache=cache, name=name)
  return s

def dataflow(*definition):
  from .lang import achain

  def get_config(node: Stage, kwargs):
    config = dict()
    if 'common' in kwargs:
      config.update(kwargs['common'])

    name = node.name()
    if name is not None and name in kwargs:
      config.update(kwargs[name])

    return config

  def load(node, kwargs):
    config = get_config(node, kwargs)
    return apply_with_kwargs(node.load, **config)

  def get_output(node, args, kwargs):
    config = get_config(node, kwargs)
    return node.get_output_for(*args, **config)

  def save(node, obj, kwargs):
    config = get_config(node, kwargs)
    return apply_with_kwargs(node.save, obj, **config)

  return DataFlow(
    achain(*definition)(),
    get_output=get_output,
    load=load,
    save=save
  )