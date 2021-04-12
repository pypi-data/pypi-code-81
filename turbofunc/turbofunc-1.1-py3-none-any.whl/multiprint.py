def multiprint(stuffToPrint, *args, **kwargs):
    """
    Accepts a dictionary. With key/value pairs text/function.
    For example, you might pass {"Welcome to ": cprint.info, "Palc": cprint.ok, "!" + MANYSPACE: cprint.info}
    which will run cprint.info("Welcome to ");cprint.ok("Palc");cprint.info("!" + MANYSPACE)
    The *args and **kwargs are given to EVERY function. Useful as an "end=True" or similar.
    """
    for item in stuffToPrint:
        stuffToPrint[item](item, *args, **kwargs)
