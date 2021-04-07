# file matrixb/columnnormalizer.py

# Copyright (c) 2019-2020 Kevin Crouse
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# @license: http://www.apache.org/licenses/LICENSE-2.0
# @author: Kevin Crouse (krcrouse@gmail.com)

import sys

import datacleaner
import re
# - there may be a better way to do this in the future
# but right now we pull from the join function for the core data cleaner
underscorejoin = datacleaner.datacleaner.underscorejoin

class ColumnNormalizer(datacleaner.SnakeCase):
    default_translations = {None:'<blank>'}

    def __init__(self, shorthand_name='default', **kwargs):

        super().__init__(**kwargs)

        # handle additional/special resolution cases
        special_underscores = r'[:\|\-\.\,\(\)\[\]\{\}\/]'
        if shorthand_name is None:
            pass
        elif shorthand_name == 'default' or shorthand_name == False:
            # just add the typical functionality
            self.prepend_transliterations([
                (special_underscores, '_'),
                (r'(\w)[^\w\'\s](\w)', underscorejoin),
                (r'[^\s\w\-\%\#]', ''),
                (r'([a-z])([\%\#])', underscorejoin),
                (r'([\%\#])([a-z])', underscorejoin),
            ])
        elif shorthand_name == 'conservative':
            # only eliminate parens and similary containers
            self.prepend_transliterations([
                (special_underscores, '_'),
            ])
        elif shorthand_name == 'ascii':
            # convert whitespace to underscores. eliminate all non-characters.
            self.prepend_transliterations([
                (special_underscores, '_'),
                (r'[^\w\s]', ''),
            ])
        else:
            raise Exception("Do not have a shorthand column normalizer definition for '" + shorthand_name + "'")
