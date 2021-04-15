import logging

logFormatter = logging.Formatter('%(asctime)s-%(name)s:%(lineno)d - %(levelname)s - %(message)s')
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

