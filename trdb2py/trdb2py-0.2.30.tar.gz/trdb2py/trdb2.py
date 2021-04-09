# -*- coding:utf-8 -*-
import grpc
import trdb2py.trading2_pb2
import trdb2py.tradingdb2_pb2
import trdb2py.tradingdb2_pb2_grpc
from trdb2py.utils import str2asset
from trdb2py.trdb2utils import getIndicatorInResult
from datetime import datetime
import time
import pandas as pd


def insCandles(fv: dict, sc: trdb2py.trading2_pb2.Candle,
               dtFormat: str = '%Y-%m-%d', scale: float = 10000.0):
    for i in range(0, len(fv['ts'])):
        if fv['ts'][i] == sc.ts:
            if sc.open:
                fv['open'][i] = sc.open / scale

            if sc.close:
                fv['close'][i] = sc.close / scale

            if sc.high:
                fv['high'][i] = sc.high / scale

            if sc.low:
                fv['low'][i] = sc.low / scale

            return

        if fv['ts'][i] > sc.ts:
            fv['ts'].insert(i, sc.ts)
            fv['date'].insert(i, datetime.fromtimestamp(
                sc.ts).strftime(dtFormat))

            if sc.open:
                fv['open'].insert(i, sc.open / scale)

            if sc.close:
                fv['close'].insert(i, sc.close / scale)

            if sc.high:
                fv['high'].insert(i, sc.high / scale)

            if sc.low:
                fv['low'].insert(i, sc.low / scale)

            return

    fv['ts'].append(sc.ts)
    fv['date'].append(datetime.fromtimestamp(
        sc.ts).strftime(dtFormat))

    if sc.open:
        fv['open'].append(sc.open / scale)

    if sc.close:
        fv['close'].append(sc.close / scale)

    if sc.high:
        fv['high'].append(sc.high / scale)

    if sc.low:
        fv['low'].append(sc.low / scale)


def getAssetCandles(cfg: dict, asset: str, tsStart: int, tsEnd: int, simCandle: trdb2py.trading2_pb2.Candles = None,
                    dtFormat: str = '%Y-%m-%d', scale: float = 10000.0) -> pd.DataFrame:

    channel = grpc.insecure_channel(cfg['servaddr'])
    stub = trdb2py.tradingdb2_pb2_grpc.TradingDB2Stub(channel)

    curasset = str2asset(asset)

    response = stub.getCandles(trdb2py.tradingdb2_pb2.RequestGetCandles(
        market=curasset.market,
        symbol=curasset.code,
        tsStart=tsStart,
        tsEnd=tsEnd,
        basicRequest=trdb2py.trading2_pb2.BasicRequestData(
            token=cfg['token'],
        ),
    ))

    fv = {'date': [], 'close': [], 'open': [], 'high': [], 'low': [], 'ts': []}
    for curres in response:
        for candle in curres.candles.candles:
            fv['ts'].append(candle.ts)
            fv['date'].append(datetime.fromtimestamp(
                candle.ts).strftime(dtFormat))
            fv['open'].append(candle.open / scale)
            fv['close'].append(candle.close / scale)
            fv['high'].append(candle.high / scale)
            fv['low'].append(candle.low / scale)

    if simCandle:
        if curasset.market == simCandle.market and curasset.code == simCandle.symbol:
            for v in simCandle.candles:
                insCandles(fv, v, dtFormat, scale)

    return pd.DataFrame(fv)


def genSimTradingParams(cfg, lstParams: list, ignoreTotalReturn: float = 0, ignoreCache: bool = False,
                        minNums: int = 10, maxIgnoreNums: int = 0):
    for i in range(len(lstParams)):
        yield trdb2py.tradingdb2_pb2.RequestSimTrading(
            basicRequest=trdb2py.trading2_pb2.BasicRequestData(
                token=cfg['token'],
            ),
            params=lstParams[i],
            ignoreCache=ignoreCache,
            index=i,
            ignoreTotalReturn=ignoreTotalReturn,
            minNums=minNums,
            maxIgnoreNums=maxIgnoreNums,
        )


def simTradings(cfg, lstParams: list, ignoreTotalReturn: float = 0, ignoreCache: bool = False,
                minNums: int = 10, maxIgnoreNums: int = 0) -> list:
    channel = grpc.insecure_channel(cfg['servaddr'])
    stub = trdb2py.tradingdb2_pb2_grpc.TradingDB2Stub(channel)

    lstRes = []
    responses = stub.simTrading2(
        genSimTradingParams(cfg, lstParams, ignoreTotalReturn=ignoreTotalReturn,
                            ignoreCache=ignoreCache, minNums=minNums, maxIgnoreNums=maxIgnoreNums))
    for response in responses:
        if len(response.pnl) > 0:
            pnl = response.pnl[0]
            lstRes.append({'title': pnl.title, 'pnl': pnl.total})

    return lstRes


def simTrading(cfg, params: trdb2py.trading2_pb2.SimTradingParams, ignoreCache: bool = False) -> dict:
    channel = grpc.insecure_channel(cfg['servaddr'])
    stub = trdb2py.tradingdb2_pb2_grpc.TradingDB2Stub(channel)

    response = stub.simTrading(trdb2py.tradingdb2_pb2.RequestSimTrading(
        basicRequest=trdb2py.trading2_pb2.BasicRequestData(
            token=cfg['token'],
        ),
        params=params,
        ignoreCache=ignoreCache,
    ))

    if len(response.pnl) > 0:
        pnl = response.pnl[0]
        return {'title': pnl.title, 'pnl': pnl.total}

    return None


def getAssetCandles2(cfg: dict, asset: str, tsStart: int, tsEnd: int, dtFormat: str = '%Y-%m-%d', offset: int = 0,
                     scale: float = 10000.0, indicators: slice = None, simCandle: trdb2py.trading2_pb2.Candles = None, ignoreCache: bool = False) -> dict:

    df = getAssetCandles(cfg, asset, tsStart, tsEnd,
                         simCandle=simCandle, dtFormat=dtFormat, scale=scale)

    ret = {
        'candle': df,
    }

    if indicators != None:
        s0 = trdb2py.trading2_pb2.Strategy(
            name="normal",
            asset=str2asset(asset),
        )

        arrbuy = []

        for v in indicators:
            buy0 = trdb2py.trading2_pb2.CtrlCondition(
                name='indicatorsp',
                operators=['upcross'],
                strVals=[v],
            )

            arrbuy.append(buy0)

        paramsbuy = trdb2py.trading2_pb2.BuyParams(
            perHandMoney=1,
        )

        paramsinit = trdb2py.trading2_pb2.InitParams(
            money=10000,
        )

        s0.buy.extend(arrbuy)
        s0.paramsBuy.CopyFrom(paramsbuy)
        s0.paramsInit.CopyFrom(paramsinit)

        p0 = trdb2py.trading2_pb2.SimTradingParams(
            assets=[str2asset(asset)],
            startTs=tsStart,
            endTs=tsEnd,
            strategies=[s0],
            title='buyandhold',
            indicators=indicators,
            offset=offset,
        )

        ret1 = simTrading(cfg, p0, ignoreCache)
        # print(ret1)
        if ret1 != None:
            for v in indicators:
                idf = getIndicatorInResult(ret1, v, dtFormat, scale)
                if not idf.empty:
                    ret[v] = idf

    return ret
