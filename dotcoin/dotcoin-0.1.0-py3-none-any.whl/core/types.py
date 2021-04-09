from typing import List
from dataclasses import dataclass


@dataclass(frozen=True)
class Market:
    quote: str
    base: str


@dataclass
class Context:
    market: Market
    exchange: str


@dataclass
class Ticker:
    context: Context
    last: float
    bid: float
    ask: float
    volume: float
    var: float


@dataclass
class Order:
    quote: float
    base: float
    price: float


@dataclass
class Book:
    context: Context
    bids: List[Order]
    asks: List[Order]


@dataclass
class Table:
    header: List[str]
    content: List[List[str]]
