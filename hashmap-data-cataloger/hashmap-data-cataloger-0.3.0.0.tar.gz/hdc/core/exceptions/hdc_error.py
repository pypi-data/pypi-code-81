#  Copyright © 2020 Hashmap, Inc
#  #
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  #
#      http://www.apache.org/licenses/LICENSE-2.0
#  #
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

class HdcError(Exception):
    """
    Error class for hdc library.
    """

    def __init__(self, message, **kwargs):
        self.message = message
        self.additional_args = kwargs

    def __str__(self) -> str:
        if self.message:
            return f"{self.__class__.__name__} :: {self.message}"

    def print_extended(self):
        if self.additional_args is not None:
            print(f"{self.__class__.__name__} :: {self.message} :: \n {self.additional_args}")

    def print_traceback(self):
        if 'traceback' in self.additional_args.keys():
            print(self.additional_args.get('traceback'))
        else:
            print('traceback not available')
