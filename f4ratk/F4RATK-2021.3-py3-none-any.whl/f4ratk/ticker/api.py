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

from pandas import DataFrame

from f4ratk.analyze.evaluation import EvaluatedResults
from f4ratk.domain import AnalysisConfig, Currency, Frame


@dataclass(frozen=True)
class Stock:
    ticker_symbol: str
    currency: Currency = Currency.USD


class NoTickerData(IOError):
    def __init__(self, symbol: str):
        super().__init__(f"No data fetched for symbol '{symbol}'.")


class TickerAnalyzer(metaclass=ABCMeta):
    @abstractmethod
    def analyze_ticker_symbol(
        self, stock: Stock, analysis_config: AnalysisConfig
    ) -> EvaluatedResults:
        """Analyze ticker symbol data."""


class TickerReader(metaclass=ABCMeta):
    @abstractmethod
    def read_ticker(self, stock: Stock, frame: Frame) -> DataFrame:
        """Read ticker symbol data to DataFrame."""
