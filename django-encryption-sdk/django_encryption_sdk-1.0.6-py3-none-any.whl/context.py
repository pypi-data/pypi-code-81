import contextvars

_context = contextvars.ContextVar("data_keeper_sig_ctx")


class Context(object):
    @staticmethod
    def set(**kwargs):
        return _context.set(kwargs)

    @staticmethod
    def get():
        return _context.get()

    @staticmethod
    def reset():
        _context.set(dict())
