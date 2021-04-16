# Instantiate PyMom and report on brokers.

pymom = PyMom()
logger.error("Brokers = {}".format(pymom.bootstrap_brokers()))
sys.exit(0)
