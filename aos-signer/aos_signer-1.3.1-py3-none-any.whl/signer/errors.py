#
#  Copyright (c) 2018-2019 Renesas Inc.
#  Copyright (c) 2018-2019 EPAM Systems Inc.
#


class SignerError(Exception):
    pass


class SignerConfigError(SignerError):
    pass


class NoAccessError(SignerError):
    pass
