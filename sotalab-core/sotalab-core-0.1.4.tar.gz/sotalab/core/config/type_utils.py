import inspect

__all__ = ["get_full_arg_spec"]


def get_full_arg_spec(cls):
    assert inspect.isclass(cls), cls

    argspec = inspect.getfullargspec(cls.__init__)
    # skip `self`
    args = argspec.args[1:] + argspec.kwonlyargs

    defaults = {}
    if argspec.defaults is not None:
        for k, v in zip(argspec.args[-len(argspec.defaults) :], argspec.defaults):
            defaults[k] = v
    if argspec.kwonlydefaults is not None:
        defaults.update(argspec.kwonlydefaults)

    annotations = argspec.annotations

    spec = {}
    for arg in args:
        assert arg in annotations, f"{cls} -> {arg}"
        spec[arg] = annotations[arg]

    return spec, defaults
