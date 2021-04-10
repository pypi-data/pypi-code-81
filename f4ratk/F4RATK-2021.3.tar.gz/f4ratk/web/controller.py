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

import logging
from dataclasses import dataclass
from json import loads
from typing import List, Tuple

from flask import Response, after_this_request, current_app as app, jsonify, request
from pandas import DataFrame, concat
from statsmodels.regression.linear_model import RegressionResultsWrapper

# noinspection PyPackageRequirements
from werkzeug.datastructures import FileStorage

from f4ratk.analyze.evaluation import EvaluatedResult
from f4ratk.cli.types import RegionChoice
from f4ratk.domain import AnalysisConfig, Currency, Frame, Frequency
from f4ratk.file.api import FileAnalyzer
from f4ratk.file.reader import FileConfig, ValueFormat
from f4ratk.infrastructure import di
from f4ratk.ticker.api import TickerAnalyzer
from f4ratk.ticker.reader import Stock
from f4ratk.web.infrastructure import server_cache

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class Coefficient:
    name: str
    weight: float
    standardError: float
    probability: float


@dataclass(frozen=True)
class AnalysisReport:
    coefficients: Tuple[Coefficient]
    adjustedRSquared: float
    observations: int
    excessReturn: float


_DEFAULT_QUERY_CACHE = 60 * 60 * 24 * 14


@app.route('/v0/tickers/<symbol>;region=<region>', methods=['GET'])
@server_cache.cached(timeout=_DEFAULT_QUERY_CACHE)
def tickers(symbol, region) -> Response:
    stock = Stock(ticker_symbol=symbol, currency=Currency.USD)

    analysis_config = AnalysisConfig(
        region=RegionChoice().convert(region, None, None),
        frame=Frame(frequency=Frequency.MONTHLY, start=None, end=None),
    )

    results = di[TickerAnalyzer].analyze_ticker_symbol(
        stock=stock,
        analysis_config=analysis_config,
    )

    report = to_report(results.ff6)

    @after_this_request
    def add_cache_control(response):
        response.headers['Cache-Control'] = f'max-age={_DEFAULT_QUERY_CACHE}'
        return response

    return jsonify(report)


@app.route('/v0/files', methods=['POST'])
def files() -> Response:
    received_files: List[FileStorage] = request.files.getlist(
        key='file', type=FileStorage
    )
    config = loads(request.form.get(key='config', default=None, type=str))
    file = next(file for file in received_files)

    results = di[FileAnalyzer].analyze_file(
        FileConfig(file, Currency.USD, ValueFormat.PRICE),
        AnalysisConfig(
            RegionChoice().convert(config['region'], None, None),
            Frame(Frequency.MONTHLY, None, None),
        ),
    )

    report = to_report(results.ff6)

    return jsonify(report)


def to_report(result: EvaluatedResult) -> AnalysisReport:
    return AnalysisReport(
        coefficients=to_coefficients(result.model),
        adjustedRSquared=result.model.rsquared_adj,
        observations=int(result.model.nobs),
        excessReturn=result.evaluation,
    )


def to_coefficients(model: RegressionResultsWrapper) -> Tuple[Coefficient]:
    concated: DataFrame = concat((model.params, model.bse, model.pvalues), axis=1)

    return tuple(
        Coefficient(name, weight, std, probability)
        for name, weight, std, probability in concated.itertuples()
    )
