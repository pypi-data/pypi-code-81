import os
import text_unidecode
from robot.api import logger


def extract_type_from(locator):
    return locator.split(":")[0]


def extract_name_from(locator):
    return locator.split(":", 1)[1]


def sanitize_camel_case(name: str):
    if name is not None:
        name = ''.join(c for c in name.title() if not c.isspace())
        name = name.translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+\"\'"})
        name = text_unidecode.unidecode(name)
    return name


def execute(cmd: str):
    res = os.system(cmd)
    cmdlog = f'EXECUTED: "{cmd}" WITH RESULT {res}'
    logger.info(cmdlog)
    print(cmdlog)
