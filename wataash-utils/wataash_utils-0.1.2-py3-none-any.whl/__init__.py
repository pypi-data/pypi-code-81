# SPDX-License-Identifier: Apache-2.0

from wataash_utils.logger import logger
import wataash_utils.logger
import wataash_utils.pycharm
import wataash_utils.str


def warn_cr(file: str, txt: str) -> None:
    pos_cr = txt.find('\r')
    if pos_cr != -1:
        msg = (f'file {file}: '
               f'carriage-return (CR; 0x0d) character found at byte:{pos_cr} '
               f'(made on Windows?); '
               f'only line-feed (LF; 0x0a) is supported as the new-line '
               f'character')
        logger.warning(msg)


del logger
