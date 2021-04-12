def multiprint(stuffToPrint, _=None, **kwargs):
    """
    Accepts a dictionary. With key/value pairs text/function.
    For example, you might pass {"Welcome to ": cprint.info, "Palc": cprint.ok, "!" + MANYSPACE: cprint.info}
    which will run cprint.info("Welcome to ");cprint.ok("Palc");cprint.info("!" + MANYSPACE)
    Setting gettext to True will run whateverFunctionYouPassed(_(item), *args, **kwargs) instead of just whateverFunctionYouPassed(item, *args, **kwargs). 
    The **kwargs is given to EVERY function. Useful as an "end=True" or similar.
    """
    if _ is None:
        def _(string):
            return string
    for item in stuffToPrint:
        stuffToPrint[item](_(item), **kwargs)

