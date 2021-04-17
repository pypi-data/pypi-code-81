import random
import os


def _new_rmsfact():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.normpath(f"{ROOT_DIR}/data")
    FACT_FILE = os.path.normpath(f"{DATA_DIR}/rmsfact.txt")
    with open(FACT_FILE, "r") as f:
        lines = f.readlines()
        facts = [line.strip("\n")
                 for line in lines if not line.startswith("#")]

    n_facts = len(facts)

    def rmsfact():
        idx = random.randint(0, n_facts)
        return facts[idx]

    return rmsfact
