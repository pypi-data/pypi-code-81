import datetime
import os
import sys
import time

import baostock as bs
import pandas as pd
import pretty_errors
from tqdm import tqdm

sys.path.append(os.path.dirname(__file__) + os.sep + '../')
try:
    from ..log.SlyLog import slog, sprint
    from .GetDate import GetDate
except:
    from log.SlyLog import slog, sprint
    from GetDate import GetDate


class StockData(object):
    """get stock data
    Args:
        names (list, optional): stock list. Defaults to ['贵州茅台', '隆基股份'].
        start_date (str, optional): start date. Defaults to '2020-12-01'.
        end_date (str, optional): end date. Defaults to '2020-12-31'.
        frequency (str, optional): frequency. Defaults to "w".
    """

    def __init__(self, names=['贵州茅台', '隆基股份'],
                 start_date='2020-12-01', end_date='2020-12-31',
                 frequency="w",
                 cache=False):
        self.cache = cache
        if self.cache == True:
            try:
                os.makedirs('./cache')
            except:
                pass
        self.sprint = sprint()
        self.slog = slog('stock info')
        self.start_date = start_date
        self.end_date = end_date
        self.frequency = frequency
        if type(names) == str:
            self.names = [names]
        elif type(names) == list:
            self.names = names
        self.sprint.hide()
        bs.login()
        self.sprint.show()
        self.slog.log(f'time: {self.start_date} ~~ {self.end_date}', mode=1)
        self.slog.log(f'stocks: {self.names}', mode=1)
        self.slog.log(f'frequency: {self.frequency}', mode=1)

    @property
    def stock_pair(self):
        self.sprint.pink('getting stock pair...')
        lists = []
        for i in tqdm(self.names):
            rs = bs.query_stock_industry()
            rs = bs.query_stock_basic(code_name=i)
            industry_list = []
            while (rs.error_code == '0') & rs.next():
                industry_list.append(rs.get_row_data())
            info = pd.DataFrame(industry_list, columns=rs.fields)
            lists.append(info)
        df = pd.concat(lists)
        stocks = {}
        for i, j in df[['code', 'code_name', 'ipoDate']].iterrows():
            if j[2] >= self.start_date:
                self.sprint.red(
                    f"{j[1]}'s ipo date is {j[2]},which is after {self.start_date}.")
                #raise ValueError(
                #    "The start date should be after the ipo date!")
            stocks[j[1]] = j[0]
            self.slog.log(f'{j[1]}——{j[0]}', mode=1)
        return stocks  # {'贵州茅台': 'sh.600519', '隆基股份': 'sh.601012'}

    @property
    def stock_data(self, info="date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg"):

        stock_pair = self.stock_pair
        codes = list(stock_pair.values())
        # 交换stock_pair键值对
        Name = dict(zip(stock_pair.values(), stock_pair.keys()))
        lists = []
        self.sprint.yellow('getting stock data...')
        for i in tqdm(codes):
            rs = bs.query_history_k_data_plus(i, info,
                                              start_date=self.start_date, end_date=self.end_date,
                                              frequency=self.frequency, adjustflag="3")
            data_list = []
            while (rs.error_code == '0') & rs.next():
                data_list.append(rs.get_row_data())
            result = pd.DataFrame(data_list, columns=rs.fields)
            result['name'] = Name[i]
            lists.append(result)
        df = pd.concat(lists)
        #df = df[['date', 'name', 'code', 'open', 'close',
        #         'volume', 'amount', 'adjustflag', 'turn', 'pctChg']]
        df = df.apply(pd.to_numeric, errors='ignore')
        if self.cache == True:
            df.to_csv(f'cache\\{self.names}.csv', encoding='utf8', index=False)
        return (codes,  # ['sh.600519', 'sh.601012']
                stock_pair,  # {'贵州茅台': 'sh.600519', '隆基股份': 'sh.601012'}
                df)

    def quit(self):
        self.sprint.hide()
        bs.logout()
        self.sprint.show()


class HolidayStockData(object):

    def __init__(self, names=['贵州茅台', '隆基股份'],
                 start_date='20200101',
                 end_date='20210101',
                 frequency='d',
                 holiday='国庆节', before=-21, after=21,
                 cache=False):
        self.cache = cache
        if self.cache == True:
            try:
                os.makedirs('./cache')
            except:
                pass
        self.sprint = sprint()
        self.slog = slog('holiday stock info')
        self.holiday = holiday
        self.before = before
        self.after = after
        self.names = names
        self.start_date = start_date
        self.end_date = end_date
        self.frequency = frequency
        self.slog.log(f'time: {self.start_date} ~~ {self.end_date}', mode=1)
        self.slog.log(f'stocks: {self.names}', mode=1)
        self.slog.log(f'frequency: {self.frequency}', mode=1)
        self.slog.log(f'holiday: {self.holiday}', mode=1)

    @property
    def HolidayNearbyDate(self):
        gd = GetDate(start=self.start_date, end=self.end_date)
        Date = gd.Date
        Date = Date[Date['holiday'] == self.holiday]
        if Date.empty == True:
            self.sprint.red(
                f'There are no festivals during {self.start_date}--{self.end_date}')
            raise ValueError('There are no festivals during this period!')
        start = []
        year = 0
        for i, j in Date.iterrows():
            if j[6] != year:
                start.append(str(j[0])[0:10])
            year = j[6]
        end = []
        year = list(Date['year'])[0]
        lastdate = None  # !!!!!!!!!!!!!!!!!!!!!!!!
        for i, j in Date.iterrows():
            if j[6] != year:
                end.append(str(lastdate)[0:10])
            year = j[6]
            lastdate = j[0]
        end.append(str(list(Date['date'])[-1])[0:10])

        def func(date, num):
            d = datetime.datetime.strptime(date, '%Y-%m-%d')
            delta = datetime.timedelta(days=num)
            d = d+delta
            return d.strftime('%Y-%m-%d')
        startbefore = []
        for i in start:
            startbefore.append(func(i, self.before))
        endafter = []
        for i in end:
            endafter.append(func(i, self.after))
        df = pd.DataFrame([startbefore, start, end, endafter], index=[
            'start before', 'start', 'end', 'end after'])
        df = df.T
        return df

    @property
    def HolidayNearbyData(self):
        date = self.HolidayNearbyDate
        lens = date.index.stop
        result = []
        global StockData
        for i in range(0, lens):
            start_date = list(date['start before'])[i]
            end_date = list(date['end after'])[i]
            StockData = StockData(
                names=self.names, start_date=start_date, end_date=end_date, frequency=self.frequency)
            data = StockData.stock_data
            result.append(data[2])
        df = pd.concat(result)
        # StockData.quit()
        self.sprint.show()
        if self.cache == True:
            df.to_csv(f'cache\\{self.names}.csv', encoding='utf8', index=False)
        return (data[0], data[1], df)


class ConstituentStock(object):
    def __init__(self, save=True):
        self.bs = bs
        self.sprint = sprint()
        self.slog = slog('constituent stock info')
        self.sprint.hide()
        self.bs.login()
        self.sprint.show()
        self.save = save
        if self.save:
            try:
                os.makedirs('./result')
            except:
                pass

    def quit(self):
        self.sprint.hide()
        self.bs.logout()
        self.sprint.show()

    def StockIndustry(self, names=None):
        if type(names) is not list:
            names = [names]
        rs = self.bs.query_stock_industry()
        industry_list = []
        while (rs.error_code == '0') & rs.next():
            industry_list.append(rs.get_row_data())
        result = pd.DataFrame(industry_list, columns=rs.fields)
        if names != None:
            lists = []
            for name in names:
                x = result[result['code_name'] == name]
                lists.append(x)
                for j in x.itertuples():
                    for k in j[1:]:
                        self.slog.log(k, mode=2)
                    self.slog.log('')

        df = pd.concat(lists)
        if self.save:
            df.to_csv('result\\industry.csv', index=False, encoding='utf8')
        self.quit()
        return df

    # 上证50成分股
    @property
    def sz50(self):
        rs = bs.query_sz50_stocks()
        sz50_stocks = []
        while (rs.error_code == '0') & rs.next():
            sz50_stocks.append(rs.get_row_data())
        result = pd.DataFrame(sz50_stocks, columns=rs.fields)
        if self.save:
            result.to_csv('result\\sz50.csv', index=False, encoding='utf8')
        self.quit()
        return result

    # 沪深300成分股
    @property
    def hs300(self):
        rs = bs.query_hs300_stocks()
        hs300_stocks = []
        while (rs.error_code == '0') & rs.next():
            hs300_stocks.append(rs.get_row_data())
        result = pd.DataFrame(hs300_stocks, columns=rs.fields)
        if self.save:
            result.to_csv('result\\hs300.csv', index=False, encoding='utf8')
        self.quit()
        return result

    # 中证500成分股
    @property
    def zz500(self):
        rs = bs.query_zz500_stocks()
        zz500_stocks = []
        while (rs.error_code == '0') & rs.next():
            zz500_stocks.append(rs.get_row_data())
        result = pd.DataFrame(zz500_stocks, columns=rs.fields)
        if self.save:
            result.to_csv('result\\zz500.csv', index=False, encoding='utf8')
        self.quit()
        return result


class StockAbility(object):

    def __init__(self, names=['贵州茅台', '隆基股份'],
                 start_year=2018, start_quater=1,
                 end_year=2019, end_quater=4):
        self.sprint = sprint()
        self.slog = slog('stock ability')
        self.sprint.red(
            'Please make sure that all the data has already existed!')
        self.names = names
        self.start_year = start_year
        self.end_year = end_year
        self.start_quater = start_quater
        self.end_quater = end_quater
        self.slog.log(
            f'time: {self.start_year},{self.start_quater} ~~ {self.end_year},{self.end_quater}', mode=1)
        self.slog.log(f'stocks: {self.names}', mode=1)
        Range = []
        if end_year-start_year >= 2:
            for i in range(start_quater, 5):
                Range.append([start_year, i])
            for i in range(start_year+1, end_year):
                for j in range(1, 5):
                    Range.append([i, j])
            for i in range(1, end_quater+1):
                Range.append([end_year, i])
        elif end_year == start_year:
            for i in range(start_quater, end_quater+1):
                Range.append([end_year, i])
        else:
            for i in range(start_quater, 5):
                Range.append([start_year, i])
            for i in range(1, end_quater+1):
                Range.append([end_year, i])
        self.Range = Range
        self.StockData = StockData(names=self.names)
        self.stock_pair = self.StockData.stock_pair

    # 盈利能力
    @property
    def profit(self):
        intro = '''
        季频盈利能力
        code	证券代码	
        pubDate	公司发布财报的日期	
        statDate	财报统计的季度的最后一天, 比如2017-03-31, 2017-06-30	
        roeAvg	净资产收益率(平均)(%)	归属母公司股东净利润/[(期初归属母公司股东的权益+期末归属母公司股东的权益)/2]*100%
        npMargin	销售净利率(%)	净利润/营业收入*100%
        gpMargin	销售毛利率(%)	毛利/营业收入*100%=(营业收入-营业成本)/营业收入*100%
        netProfit	净利润(元)	
        epsTTM	每股收益	归属母公司股东的净利润TTM/最新总股本
        MBRevenue	主营营业收入(元)	
        totalShare	总股本	
        liqaShare	流通股本
        '''
        self.slog.log(intro)
        profit = []
        self.sprint.blue('getting profit data')
        for i, j in self.stock_pair.items():
            self.sprint.cyan(i)
            for k in tqdm(self.Range):
                profit_list = []
                profit_list.append(i)
                profit_list.append(k[0])
                profit_list.append(k[1])
                rs_profit = bs.query_profit_data(
                    code=j, year=k[0], quarter=k[1])
                while (rs_profit.error_code == '0') & rs_profit.next():
                    profit_list = profit_list+rs_profit.get_row_data()
                columns = ['name', 'year', 'quater']
                columns = columns+rs_profit.fields
                result_profit = pd.DataFrame([profit_list], columns=columns)
                profit.append(result_profit)
        df = pd.concat(profit)
        return df

    # 营运能力
    @property
    def operation(self):
        intro = '''
        季频营运能力
        code	证券代码	
        pubDate	公司发布财报的日期	
        statDate	财报统计的季度的最后一天, 比如2017-03-31, 2017-06-30	
        NRTurnRatio	应收账款周转率(次)	营业收入/[(期初应收票据及应收账款净额+期末应收票据及应收账款净额)/2]
        NRTurnDays	应收账款周转天数(天)	季报天数/应收账款周转率(一季报：90天，中报：180天，三季报：270天，年报：360天)
        INVTurnRatio	存货周转率(次)	营业成本/[(期初存货净额+期末存货净额)/2]
        INVTurnDays	存货周转天数(天)	季报天数/存货周转率(一季报：90天，中报：180天，三季报：270天，年报：360天)
        CATurnRatio	流动资产周转率(次)	营业总收入/[(期初流动资产+期末流动资产)/2]
        AssetTurnRatio	总资产周转率	营业总收入/[(期初资产总额+期末资产总额)/2]
        '''
        self.slog.log(intro)
        operation = []
        self.sprint.blue('getting operation data')
        for i, j in self.stock_pair.items():
            self.sprint.cyan(i)
            for k in tqdm(self.Range):
                operation_list = []
                operation_list.append(i)
                operation_list.append(k[0])
                operation_list.append(k[1])
                rs_operation = bs.query_operation_data(
                    code=j, year=k[0], quarter=k[1])
                while (rs_operation.error_code == '0') & rs_operation.next():
                    operation_list = operation_list+rs_operation.get_row_data()
                columns = ['name', 'year', 'quater']
                columns = columns+rs_operation.fields
                result_operation = pd.DataFrame(
                    [operation_list], columns=columns)
                operation.append(result_operation)
        df = pd.concat(operation)
        return df

    # 成长能力
    @property
    def growth(self):
        intro = '''
        季频成长能力
        code	证券代码	
        pubDate	公司发布财报的日期	
        statDate	财报统计的季度的最后一天, 比如2017-03-31, 2017-06-30	
        YOYEquity	净资产同比增长率	(本期净资产-上年同期净资产)/上年同期净资产的绝对值*100%
        YOYAsset	总资产同比增长率	(本期总资产-上年同期总资产)/上年同期总资产的绝对值*100%
        YOYNI	净利润同比增长率	(本期净利润-上年同期净利润)/上年同期净利润的绝对值*100%
        YOYEPSBasic	基本每股收益同比增长率	(本期基本每股收益-上年同期基本每股收益)/上年同期基本每股收益的绝对值*100%
        YOYPNI	归属母公司股东净利润同比增长率	(本期归属母公司股东净利润-上年同期归属母公司股东净利润)/上年同期归属母公司股东净利润的绝对值*100%
        '''
        self.slog.log(intro)
        growth = []
        self.sprint.blue('getting growth data')
        for i, j in self.stock_pair.items():
            self.sprint.cyan(i)
            for k in tqdm(self.Range):
                growth_list = []
                growth_list.append(i)
                growth_list.append(k[0])
                growth_list.append(k[1])
                rs_growth = bs.query_growth_data(
                    code=j, year=k[0], quarter=k[1])
                while (rs_growth.error_code == '0') & rs_growth.next():
                    growth_list = growth_list+rs_growth.get_row_data()
                columns = ['name', 'year', 'quater']
                columns = columns+rs_growth.fields
                result_growth = pd.DataFrame([growth_list], columns=columns)
                growth.append(result_growth)
        df = pd.concat(growth)
        return df

    # 偿债能力
    @property
    def balance(self):
        intro = '''
        季频偿债能力
        code	证券代码	
        pubDate	公司发布财报的日期	
        statDate	财报统计的季度的最后一天, 比如2017-03-31, 2017-06-30	
        currentRatio	流动比率	流动资产/流动负债
        quickRatio	速动比率	(流动资产-存货净额)/流动负债
        cashRatio	现金比率	(货币资金+交易性金融资产)/流动负债
        YOYLiability	总负债同比增长率	(本期总负债-上年同期总负债)/上年同期中负债的绝对值*100%
        liabilityToAsset	资产负债率	负债总额/资产总额
        assetToEquity	权益乘数	资产总额/股东权益总额=1/(1-资产负债率)        
        '''
        self.slog.log(intro)
        balance = []
        self.sprint.blue('getting balance data')
        for i, j in self.stock_pair.items():
            self.sprint.cyan(i)
            for k in tqdm(self.Range):
                balance_list = []
                balance_list.append(i)
                balance_list.append(k[0])
                balance_list.append(k[1])
                rs_balance = bs.query_balance_data(
                    code=j, year=k[0], quarter=k[1])
                while (rs_balance.error_code == '0') & rs_balance.next():
                    balance_list = balance_list+rs_balance.get_row_data()
                columns = ['name', 'year', 'quater']
                columns = columns+rs_balance.fields
                result_balance = pd.DataFrame([balance_list], columns=columns)
                balance.append(result_balance)
        df = pd.concat(balance)
        return df

    # 现金流量
    @property
    def cash_flow(self):
        intro = '''
        季频现金流量
        code	证券代码	
        pubDate	公司发布财报的日期	
        statDate	财报统计的季度的最后一天, 比如2017-03-31, 2017-06-30	
        CAToAsset	流动资产除以总资产	
        NCAToAsset	非流动资产除以总资产	
        tangibleAssetToAsset	有形资产除以总资产	
        ebitToInterest	已获利息倍数	息税前利润/利息费用
        CFOToOR	经营活动产生的现金流量净额除以营业收入	
        CFOToNP	经营性现金净流量除以净利润	
        CFOToGr	经营性现金净流量除以营业总收入
        '''
        self.slog.log(intro)
        cash_flow = []
        self.sprint.blue('getting cash flow data')
        for i, j in self.stock_pair.items():
            self.sprint.cyan(i)
            for k in tqdm(self.Range):
                cash_flow_list = []
                cash_flow_list.append(i)
                cash_flow_list.append(k[0])
                cash_flow_list.append(k[1])
                rs_cash_flow = bs.query_cash_flow_data(
                    code=j, year=k[0], quarter=k[1])
                while (rs_cash_flow.error_code == '0') & rs_cash_flow.next():
                    cash_flow_list = cash_flow_list+rs_cash_flow.get_row_data()
                columns = ['name', 'year', 'quater']
                columns = columns+rs_cash_flow.fields
                result_cash_flow = pd.DataFrame(
                    [cash_flow_list], columns=columns)
                cash_flow.append(result_cash_flow)
        df = pd.concat(cash_flow)
        return df

    # 杜邦指数
    @property
    def dupont_data(self):
        intro = '''
        季频杜邦指数
        code	证券代码	
        pubDate	公司发布财报的日期	
        statDate	财报统计的季度的最后一天, 比如2017-03-31, 2017-06-30	
        dupontROE	净资产收益率	归属母公司股东净利润/[(期初归属母公司股东的权益+期末归属母公司股东的权益)/2]*100%
        dupontAssetStoEquity	权益乘数，反映企业财务杠杆效应强弱和财务风险	平均总资产/平均归属于母公司的股东权益
        dupontAssetTurn	总资产周转率，反映企业资产管理效率的指标	营业总收入/[(期初资产总额+期末资产总额)/2]
        dupontPnitoni	归属母公司股东的净利润/净利润，反映母公司控股子公司百分比。如果企业追加投资，扩大持股比例，则本指标会增加。	
        dupontNitogr	净利润/营业总收入，反映企业销售获利率	
        dupontTaxBurden	净利润/利润总额，反映企业税负水平，该比值高则税负较低。净利润/利润总额=1-所得税/利润总额	
        dupontIntburden	利润总额/息税前利润，反映企业利息负担，该比值高则税负较低。利润总额/息税前利润=1-利息费用/息税前利润
        dupontEbittogr	息税前利润/营业总收入，反映企业经营利润率，是企业经营获得的可供全体投资人（股东和债权人）分配的盈利占企业全部营收收入的百分比
        '''
        self.slog.log(intro)
        dupont_data = []
        self.sprint.blue('getting dupont data')
        for i, j in self.stock_pair.items():
            self.sprint.cyan(i)
            for k in tqdm(self.Range):
                dupont_data_list = []
                dupont_data_list.append(i)
                dupont_data_list.append(k[0])
                dupont_data_list.append(k[1])
                rs_dupont_data = bs.query_dupont_data(
                    code=j, year=k[0], quarter=k[1])
                while (rs_dupont_data.error_code == '0') & rs_dupont_data.next():
                    dupont_data_list = dupont_data_list+rs_dupont_data.get_row_data()
                columns = ['name', 'year', 'quater']
                columns = columns+rs_dupont_data.fields
                result_dupont_data = pd.DataFrame(
                    [dupont_data_list], columns=columns)
                dupont_data.append(result_dupont_data)
        df = pd.concat(dupont_data)
        return df

    @property
    def AllAbility(self):
        profit = self.profit
        operation = self.operation
        growth = self.growth
        balance = self.balance
        cash_flow = self.cash_flow
        dupont_data = self.dupont_data
        lists = [growth, balance, cash_flow, dupont_data]
        df = pd.merge(profit, operation, how='outer', on=[
            'code', 'name', 'year', 'quater', 'pubDate', 'statDate'])
        for i in lists:
            df = pd.merge(df, i, how='outer', on=[
                'code', 'name', 'year', 'quater', 'pubDate', 'statDate'])
        return df


if __name__ == '__main__':
    StockData = StockData(names=['隆基股份'],
                 start_date='2001-12-01', end_date='2020-12-31',
                 frequency="w")
    # print(StockData.stock_pair)
    # HolidayStockData=HolidayStockData()
    # print(HolidayStockData.HolidayNearbyData)
    #cs = ConstituentStock()
    print(StockData.stock_data)
