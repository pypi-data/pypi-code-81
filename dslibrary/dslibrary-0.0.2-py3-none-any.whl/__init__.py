"""
DSLIBRARY - run your data science code anywhere.

"""
__version__ = "0.0.1"

# environment variables
from .front import ENV_DSLIBRARY_TARGET, ENV_DSLIBRARY_SPEC, ENV_DSLIBRARY_TOKEN
# main base class
from .front import DSLibrary
# run models
from .run_models import ModelRunner

# if a package called 'mmlibrary' is installed it becomes the default target
try:
    import mmlibrary
except ImportError:
    mmlibrary = None


def instance():
    """
    Get an instance of mmlibrary methods.  Configuration is through environment variables.

    To run locally in the current folder:   (this is the default)
      DSLIBRARY_TARGET=local

    To run locally with a specific default folder:
      DSLIBRARY_TARGET=local:<folder>

    To run against a REST API:
      DSLIBRARY_TARGET=https://hostname:port/path/to/api/
      DSLIBRARY_TOKEN=<access token, or credentials>

    To use a custom implementation:
      DSLIBRARY_TARGET=package.ClassName:value:name=value

    Parameter values and data input/output locations/formats and such are defined by setting this variable to
    JSON (see ModelRunner).
      DSLIBRARY_SPEC={...}

    :returns:  An instance of the MMLibrary() base class.
    """
    from .to_local import DSLibraryLocal
    from .transport.to_rest import DSLibraryViaREST
    from .transport.to_volume import DSLibraryViaVolume
    from .transport.to_mmlibrary import DSLibraryViaMMLibrary

    import importlib
    import json
    import os
    spec = json.loads(os.environ.get(ENV_DSLIBRARY_SPEC) or "{}")
    target = os.environ.get(ENV_DSLIBRARY_TARGET) or ("mmlibrary" if mmlibrary else "local")
    target_parts = target.split(":")
    # point to a REST API
    if target_parts[0] in ("http", "https"):
        token = os.environ.get(ENV_DSLIBRARY_TOKEN)
        return DSLibraryViaREST(url=target, token=token)
    # gather arguments
    args = []
    kwargs = {}
    for arg in target_parts[1:]:
        arg_parts = arg.split('=', maxsplit=1)
        if len(arg_parts) == 1:
            args.append(arg)
        else:
            kwargs[arg_parts[0]] = arg_parts[1]
    if spec:
        kwargs["spec"] = spec
    # a strictly local instance
    if target_parts[0] == "local":
        return DSLibraryLocal(*args, **kwargs)
    # delegation to 'mmlibrary'
    if target_parts[0] == "mmlibrary":
        return DSLibraryViaMMLibrary(*args, **kwargs)
    # writes through a shared volume, i.e. so that a sidecar can perform communications for us
    if target_parts[0] == "volume":
        return DSLibraryViaVolume(*args, **kwargs)
    # we fall through to custom implementation support
    cls_parts = target_parts[0].split(".")
    try:
        module = importlib.import_module('.'.join(cls_parts[:-1]))
        cls = getattr(module, cls_parts[-1])
        return cls(*args, **kwargs)
    except ImportError:
        raise ValueError(f"Unrecognized {ENV_DSLIBRARY_TARGET} implementation: {target_parts[0]}")
