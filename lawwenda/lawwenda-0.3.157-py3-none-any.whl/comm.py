# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

"""
Internal communication helpers.
"""

import json
import typing as t

import werkzeug.wrappers.json
import werkzeug.wsgi


class Request(werkzeug.wrappers.Request, werkzeug.wrappers.json.JSONMixin):  # pylint: disable=too-many-ancestors
    """
    A werkzeug request that is able to interpret json data in the response body.
    """


class JsonedResponse(werkzeug.wrappers.Response):  # pylint: disable=too-many-ancestors
    """
    A werkzeug response that serializes response data to json.
    """

    def __init__(self, data: t.Optional[t.Any], **kwargs):
        """
        :param data: Response data. Can be anything that `json` is able to serialize.
        """
        super().__init__(json.dumps(data), mimetype="application/json", **kwargs)
