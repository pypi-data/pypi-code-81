import datetime
from typing import List, Optional, Union

import pydantic


class TimeDefinition(pydantic.BaseModel):
    timezone: str
    gmtoffset: int
    start: datetime.datetime
    end: datetime.datetime


class CurrentTradingPeriod(pydantic.BaseModel):
    pre: TimeDefinition
    regular: TimeDefinition
    post: TimeDefinition


class TradingPeriods(pydantic.BaseModel):
    pre: List[List[TimeDefinition]]
    post: List[List[TimeDefinition]]
    regular: List[List[TimeDefinition]]


class Meta(pydantic.BaseModel):
    currency: str
    symbol: str
    exchangeName: str
    instrumentType: str
    firstTradeDate: int
    regularMarketTime: int
    gmtoffset: int
    timezone: str
    exchangeTimezoneName: str
    regularMarketPrice: float
    chartPreviousClose: float
    previousClose: float
    scale: int
    priceHint: int
    currentTradingPeriod: CurrentTradingPeriod
    tradingPeriods: Union[List[List[TimeDefinition]], TradingPeriods]
    dataGranularity: str
    range: str
    validRanges: List[str]


class QuoteItem(pydantic.BaseModel):
    open: List[Optional[float]]
    close: List[Optional[float]]
    high: List[Optional[float]]
    low: List[Optional[float]]
    volume: List[Optional[int]]


class Indicators(pydantic.BaseModel):
    quote: List[QuoteItem]


class ResultItem(pydantic.BaseModel):
    meta: Meta
    timestamp: List[datetime.datetime]
    indicators: Indicators


class Error(pydantic.BaseModel):
    code: str
    description: str


class Chart(pydantic.BaseModel):
    result: Optional[List[ResultItem]]
    error: Optional[Error]


class Model(pydantic.BaseModel):
    chart: Chart
