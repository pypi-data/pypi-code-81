import functools


def get_first_arg_url_domain(func):
    """If the first argument is a url, get the domain of the url and pass that into the function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        from d8s_urls import is_url, url_domain

        domain_arg = args[0]
        other_args = args[1:]

        if is_url(domain_arg):
            domain_arg = url_domain(domain_arg)

        return func(domain_arg, *other_args, **kwargs)

    return wrapper
