try:
    from . import version

    __version__ = version.version
except ImportError:
    __version__ = "unknown"

print("testitest")


def me(msg="I am printingpress!"):
    print(msg)
    return msg
