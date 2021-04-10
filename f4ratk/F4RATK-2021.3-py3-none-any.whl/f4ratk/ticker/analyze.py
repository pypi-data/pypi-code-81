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

from f4ratk.analyze.api import DataAnalyzer
from f4ratk.analyze.evaluation import EvaluatedResults
from f4ratk.domain import AnalysisConfig
from f4ratk.fama import FamaReader
from f4ratk.history import History
from f4ratk.ticker.api import Stock, TickerAnalyzer, TickerReader


class TickerAnalyzerAdapter(TickerAnalyzer):
    def __init__(
        self,
        fama_reader: FamaReader,
        analyzer: DataAnalyzer,
        history: History,
        ticker_reader: TickerReader,
    ):
        self._fama_reader = fama_reader
        self._analyzer = analyzer
        self._history = history
        self._ticker_reader = ticker_reader

    def analyze_ticker_symbol(
        self, stock: Stock, analysis_config: AnalysisConfig
    ) -> EvaluatedResults:
        data = self._ticker_reader.read_ticker(stock=stock, frame=analysis_config.frame)

        historic_returns = self._history.annualized_returns(
            region=analysis_config.region
        )

        return self._analyzer.analyze(
            data,
            self._fama_reader.fama_data(
                region=analysis_config.region, frequency=analysis_config.frame.frequency
            ),
            historic_returns,
        )
