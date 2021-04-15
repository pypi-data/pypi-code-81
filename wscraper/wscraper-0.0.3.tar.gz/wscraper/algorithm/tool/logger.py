# Copyright (c) 2021 T.Furukawa
# This software is released under the MIT License, see LICENSE.

import sys


class Logger:

    logger_name = None

    @classmethod
    def log(cls, string):
        if cls.logger_name is not None:
            prefix = f"[{cls.logger_name}] "
        else:
            prefix = ""

        sys.stdout.write(prefix + string + "\n")
        sys.stdout.flush()
