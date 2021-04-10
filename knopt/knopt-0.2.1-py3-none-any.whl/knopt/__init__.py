from argparse import ArgumentParser
import inspect

def arg(*names, **kwargs):
    base = kwargs.get('type', str)
    return type(base.__name__, (base,),
                {**kwargs, 'names': names})

def main(f=None, **kwargs):
    stack = inspect.stack()[1]
    mod = inspect.getmodule(stack[0])

    def decorator(f):
        if mod.__name__ == '__main__':
            run(f, **kwargs)
        else:
            f.main = lambda: run(f, **kwargs)
        return f

    if f is None: return decorator
    return decorator(f)

def run(f, **kwargs):
    version = kwargs.get('version')
    default_method = kwargs.get('default')

    parser_kwargs = {}
    if f.__doc__ is not None:
        parser_kwargs['description'] = f.__doc__
    parser = ArgumentParser(**parser_kwargs)
    if version is not None:
        parser.add_argument('--version', action='version',
                            version=f'%(prog)s {version}')
    if isinstance(f, type):
        init = getattr(f, '__init__')
        if '__init__' in f.__dict__:
            _setup_parser(parser, init, method=True)
        subs = parser.add_subparsers(title=init.__doc__)

        for method in dir(f):
            if method.startswith('_'): continue

            sub = subs.add_parser(method)
            fun = getattr(f, method)
            _setup_parser(sub, fun, method=True)
            sub.set_defaults(_run=fun)

        args = parser.parse_args()
        obj = f(*_build_args(init, args, method=True))

        if '_run' not in args:
            # no subparser selected, just run default
            if default_method is not None:
                fun = getattr(f, default_method)
                sub = subs.choices[fun.__name__]
                if '__init__' in f.__dict__:
                    _setup_parser(sub, init, method=True)
                args = sub.parse_args()
            else:
                raise Exception("no command selected")
        result = _call_with_args(args._run, args, self=obj)
        return result
    else:
        _setup_parser(parser, f)
        args = parser.parse_args()
        return _call_with_args(f, args)

def _arg_name(a, positional):
    a = a.replace('_', '-')
    if not positional:
        if len(a) > 1:
            a = '--' + a
        else:
            a = '-' + a
    return a

def _setup_parser(parser, f, method=False):
    if f.__doc__ is not None:
        parser.description = f.__doc__
    spec = inspect.signature(f).parameters
    args = list(spec.keys())
    if method: args = args[1:]
    for a in args:
        params = [a]
        kwparams = {}
        ann = spec[a].annotation
        if ann != inspect._empty:
            if getattr(ann, 'cast', False):
                kwparams['type'] = ann.type
            else:
                kwparams['type'] = ann
            alts = getattr(ann, 'names', [])
            for alt in alts:
                params.append(alt)
            if hasattr(ann, 'help'):
                kwparams['help'] = getattr(ann, 'help')
            if hasattr(ann, 'action'):
                kwparams['action'] = getattr(ann, 'action')
        default = spec[a].default
        positional = default == inspect._empty
        if not positional:
            kwparams['default'] = default
        params = map(lambda a: _arg_name(a, positional), params)

        parser.add_argument(*params, **kwparams)

def _build_args(f, args, method=False):
    spec = inspect.getfullargspec(f)
    f_args = spec.args
    if method:
        f_args = f_args[1:]
    for a in f_args:
        yield getattr(args, a)

def _call_with_args(f, args, self=None):
    if self is None:
        return f(*_build_args(f, args))
    else:
        return f(self, *_build_args(f, args, method=True))
