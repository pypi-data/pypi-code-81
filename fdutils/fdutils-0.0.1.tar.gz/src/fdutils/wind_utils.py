#  -*- coding: utf-8 -*-
# @author: zhangping

import datetime as dt
from WindPy import w


class WindUtil:

    @classmethod
    def tdays(cls, start_date, end_date=None):
        '''
        获取交易日
        ~~~~~~~~~~~~~~~~
        l = WindUtil.tdays('2020-03-07')
        l = WindUtil.tdays('2020-03-07', end_date='2020-04-07')
        '''
        cls.init()
        start_date = cls.get_date_str(start_date)
        end_date = cls.get_date_str(end_date)
        l = w.tdays(start_date, end_date, "").Data
        return l[0] if l is not None and len(l) > 0 else []

    @classmethod
    def sectors(cls, sectorid, date=None):
        '''
        获取Wind板块成分
        ~~~~~~~~~~~~~~~~
        df = WindUtil.sectors('a001010100000000') #当前全部A股
        df = WindUtil.sectors('1000010084000000', date='2020-08-28') #国内商品品种
        '''
        cls.init()
        date = cls.get_date_str(date)
        return w.wset("sectorconstituent", "sectorid={0};date={1}".format(sectorid, date), usedf=True)[1]

    @classmethod
    def sectors_by_code(cls, wind_code, date=None):
        '''
        通过Wind代码获取板块成分
        ~~~~~~~~~~~~~~~~
        df = WindUtil.sectors_by_code('APFI.WI', date='2020-08-28') #Wind农产品指数
        df = WindUtil.sectors_by_code('000300.SH') #沪深300成分股
        '''
        date = cls.get_date_str(date)
        return w.wset("sectorconstituent", "windcode={0};date={1}".format(wind_code, date), usedf=True)[1]

    @classmethod
    def fu_contracts(cls, wind_code, start_date=None, end_date=None):
        '''
        获取品种期货合约
        ~~~~~~~~~~~~~~~~
        df = WindUtil.fu_contracts('A.DCE') #获取品种合约
        '''
        start_date = cls.get_date_str(start_date)
        end_date = cls.get_date_str(end_date)
        return w.wset("futurecc", "wind_code={0};startdate={1};enddate={2}".format(wind_code, start_date, end_date),
                      usedf=True)[1]

    @classmethod
    def fu_hiscode(cls, wind_code, trade_date=None):
        '''
        获取主力合约代码
        ~~~~~~~~~~~~~~~~
        code = WindUtil.fu_hiscode('A.DCE') #获取品种合约
        '''
        start_date = cls.get_date_str(trade_date, '%Y%m%d')
        df = w.wss(wind_code, "trade_hiscode", "tradeDate={0}".format(start_date), usedf=True)[1]
        return df['TRADE_HISCODE'][0] if wind_code != df['TRADE_HISCODE'][0] else None

    @classmethod
    def get_date_str(cls, date, format='%Y-%m-%d'):
        date = date if date is not None else dt.datetime.today()
        date = date if type(date) == str else date.strftime(format)
        return date

    @classmethod
    def init(cls):
        if not w.isconnected():
            w.start()
