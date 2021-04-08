import logging

def setLogging(log_level):
    LOGFORMAT = "  s%(levelname)-8s%(reset)s | s%(message)s%(reset)s"
    stream = logging.FileHandler("logs.txt")
    logging.root.setLevel(log_level)
    stream.setLevel(log_level)

    try:
        from colorlog import ColoredFormatter
        LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | s%(message)s%(reset)s"
        formatter = ColoredFormatter(LOGFORMAT)
        stream.setFormatter(formatter)
    except:
        pass

    logger = logging.getLogger()
    logger.setLevel(log_level)
    logger.addHandler(stream)
