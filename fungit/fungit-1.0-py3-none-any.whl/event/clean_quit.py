from ..term import Term
from .key import Key


def quit_app():
    Term.clear()
    Key.stop()
    raise SystemExit()
    pass
