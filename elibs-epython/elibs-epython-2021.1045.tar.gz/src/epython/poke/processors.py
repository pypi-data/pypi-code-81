# -*- coding: utf-8 -*-
"""
Description:
     Post Processors for the Poke module. The intention is to have helper methods that
     speed up the testing of an API.

Author:
    Ray Gomez

Todo:
    * Add callback processors that would help with API validation

Date:
    3/16/21
"""

from requests import Response


class PokeResponse(Response):
    """ A subclassed version of requests.Response, wrapped to help with ease of use."""

    def __init__(self, response):
        # Make sure parent is initialized
        super().__init__()

        # Hacky way to copy the response values
        for key, val in response.__dict__.items():
            self.__dict__[key] = val

##############################################################
# Generic mechanism that allows easy validation of api calls #
##############################################################
