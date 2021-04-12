# Copyright (C) 2019 Spiralworks Technologies Inc.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import base64
import os
import requests
import json
from robotlibcore import HybridCore, keyword
from PIL import Image
from CaptchaLibrary.version import VERSION
from CaptchaLibrary.services import ForgotCaptcha, SimpleCaptcha
from CaptchaLibrary.utils import Img


class CaptchaLibrary(HybridCore):
    """ ``CaptchaLibrary`` is a Robot Framework Test Library \
        for decoding captchas.

    This document explains the usage of each keywords in this test library.
    For more information about Robot Framework, see http://robotframework.org

    == About ==

    Created: 23/09/2019 PST

    Author: Joshua Kim Rivera | joshua.rivera@mnltechnology.com

    Company: Spiralworks Technologies Inc.
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self,
                 TC_API_KEY=None,
                 serviceUrl=None,
                 header={'Content-Type': 'application/x-www-form-urlencoded'},
                 payloadType='base64Captcha',
                 ):
        """CaptchaLibrary requires that you provide the captcha service's url \
            upon import.

        - ``serviceUrl``:
            The Captcha URL Service.
        - ``header``
            (optional) default = Content-Type=application/x-www-form-urlencoded
        - ``payloadType``:
            (optional) default = base64Captcha
        """
        libraries = [
            ForgotCaptcha(serviceUrl, header, payloadType),
            SimpleCaptcha(TC_API_KEY),
            Img()
        ]
        HybridCore.__init__(self, libraries)

    @keyword
    def get_bypass_captcha_token(self, baseURL,
                                 header={'Accept': 'application/json'}):
        """Sends a GET Request to the base URL to retrieve the token to be
            used to bypass the captcha.
        """
        return self._create_get_request_for_captcha_bypass_token(baseURL,
                                                                 header)

    def _create_get_request_for_captcha_bypass_token(self, baseURL, header):
        """ Provide Documentation.
        """
        req = requests.get(baseURL, headers=header)
        req = req.json()
        return req['ResponseData']
