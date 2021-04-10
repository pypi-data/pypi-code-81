##############################################################################
# Copyright (C) 2020 - 2021 Tobias Röttger <dev@roettger-it.de>
#
# This file is part of F4RATK.
#
# F4RATK is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License version 3
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
##############################################################################

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from enum import Enum, unique
from os import PathLike

from pandas import DataFrame

from f4ratk.analyze.evaluation import EvaluatedResults
from f4ratk.domain import AnalysisConfig, Currency, Frame


@unique
class ValueFormat(Enum):
    PRICE = 'Prices'
    RETURN = 'Returns'


@dataclass(frozen=True)
class FileConfig:
    path: PathLike
    currency: Currency
    value_format: ValueFormat


class FileAnalyzer(metaclass=ABCMeta):
    @abstractmethod
    def analyze_file(
        self,
        file_config: FileConfig,
        analysis_config: AnalysisConfig,
    ) -> EvaluatedResults:
        """Analyze file content."""


class FileReader(metaclass=ABCMeta):
    @abstractmethod
    def read(self, file_config: FileConfig, frame: Frame) -> DataFrame:
        """Read file content to DataFrame."""
