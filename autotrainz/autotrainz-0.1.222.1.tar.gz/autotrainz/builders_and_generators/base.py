# Copyright © 2020 Hashmap, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import inspect
import logging
import sys
from typing import Type

from autotrainz.logger.ml_log import MLLog


class Base:
    def __init__(self):
        self._logger = MLLog(type(self).__name__, logging.DEBUG, True).logger

    def _handle_error(self, exception_message: str, exception_class: Type[Exception] = None) -> None:
        self._logger.exception(exception_message)
        if exception_class:
            raise exception_class(exception_message)

    def _log_start(self):
        print(inspect.stack()[1][3])
        self._logger.info(f'Starting execution of {inspect.stack()[1][0].f_locals["self"].__class__.__name__}.{inspect.stack()[1][3]}.')

    def _log_stop(self):
        self._logger.info(f'Finishing execution of {inspect.stack()[1][0].f_locals["self"].__class__.__name__}.{inspect.stack()[1][3]}.')
