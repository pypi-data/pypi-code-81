import random
import os
import pickle

# Rather than having the `rmsfact()` function parse the source file each time, using a closure like
# this allows us to offload the parsing and data validation (not that there is any at the moment)
# and save time when `rmsfact()` is called.
#
# TODO: Is there an advantage to using `pickle` or similar to store a binary version of the `facts`
#       object rather than parsing the text file every time the package is loaded?


def _new_rmsfact():
    """
    Generate an `rmsfact()` function

    This function runs when the package is imported. It parses the source file containing the facts,
    removes comments and creates a list of facts.

    Returns
    -------
    function : A function that, when called, returns a random fact.
    """
    # TODO: Is there a more Pythonic way of referring to the file?
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.normpath(f"{ROOT_DIR}/data")
    FACT_FILE = os.path.normpath(f"{DATA_DIR}/rmsfact.dat")
    # TODO: Error handling needed here?
    with open(FACT_FILE, "rb") as f:
        facts = pickle.load(f)

    n_facts = len(facts)

    def rmsfact():
        """
        Return a random fact about Richard M. Stallman

        Returns
        -------

        string : A randomly-selected fact.
        """
        idx = random.randint(0, n_facts)
        return facts[idx]

    return rmsfact
