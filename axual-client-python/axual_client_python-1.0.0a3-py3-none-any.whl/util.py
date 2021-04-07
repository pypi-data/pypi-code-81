# -*- coding: utf-8 -*-
#
#      Copyright (C) 2020 Axual B.V.
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import json


def parse_list(arg) -> list:
    """ Accepts a (optionally comma separated) string or list of strings, returns a list. """
    if isinstance(arg, str):
        return [x.strip() for x in arg.split(',')]
    if not isinstance(arg, list):
        raise TypeError('Expected str or list')
    return arg


def dict_to_str(dictionary) -> str:
    return json.dumps(dictionary, default=str, indent=2)
