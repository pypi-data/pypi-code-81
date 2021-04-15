import json
import os
import sys

import pandas as pd
import parsel
import requests
from tqdm import tqdm

sys.path.append(os.path.dirname(__file__) + os.sep + '../')
try:
    from ..log.SlyLog import slog, sprint
    from .GetData import StockData
except:
    from log.SlyLog import slog, sprint

    from GetData import StockData


class FinancialStatements(object):
    """get financial statement
    Args:
        names (list, optional): stock list. Defaults to ['贵州茅台', '隆基股份'].
        start_year (int, optional): start year. Defaults to 2018.
        start_quater (int, optional): start quater. Defaults to 1.
        end_year (int, optional): end year. Defaults to 2019.
        end_quater (int, optional): end quater. Defaults to 4.
    """

    def __init__(self, names=['贵州茅台', '隆基股份'],
                 start_year=2018, start_quater=1,
                 end_year=2019, end_quater=4):
        self.sprint = sprint()
        if type(names) == str:
            self.names = [names]
        elif type(names) == list:
            self.names = names
        self.stock_pair = StockData(names=self.names).stock_pair
        self.main_url = 'http://f10.eastmoney.com/NewFinanceAnalysis/'
        self.profit_statement_url = self.main_url+'lrbAjaxNew?'
        self.cash_flow_url = self.main_url+'xjllbAjaxNew?'
        self.balance_url = self.main_url+'zcfzbAjaxNew?'
        self.url_mode = {
            '现金流量表': self.cash_flow_url,
            '资产负债表': self.balance_url,
            '利润表': self.profit_statement_url
        }
        self.headers = {
            "Host": "f10.eastmoney.com",
            "Pragma": "no-cache",
            "Referer": "http://f10.eastmoney.com/NewFinanceAnalysis",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.76",
            "X-Requested-With": "XMLHttpRequest"
        }
        date = {1: '-03-31', 2: '-06-30', 3: '-09-30', 4: '-12-31'}
        Range = []
        if end_year-start_year >= 2:
            for i in range(start_quater, 5):
                Range.append(f'{start_year}{date[i]}')
            for i in range(start_year+1, end_year):
                for j in range(1, 5):
                    Range.append(f'{i}{date[j]}')
            for i in range(1, end_quater+1):
                Range.append(f'{end_year}{date[i]}')
        elif end_year == start_year:
            for i in range(start_quater, end_quater+1):
                Range.append(f'{end_year}{date[i]}')
        else:
            for i in range(start_quater, 5):
                Range.append(f'{start_year}{date[i]}')
            for i in range(1, end_quater+1):
                Range.append(f'{end_year}{date[i]}')
        self.Range = Range

    def params_list(self):
        self.sprint.cyan('getting financial statement...')
        RangeList = [self.Range[i:i+5] for i in range(0, len(self.Range), 5)]
        params_list = []
        for name in self.stock_pair.values():
            for Range in RangeList:
                params_list.append(
                    {
                        "companyType": "4",
                        "reportDateType": "0",
                        "reportType": "1",
                        "dates": ','.join(Range),
                        "code": name[0:2].upper()+name[3:]
                    })
        return params_list[::-1]

    def request(self, url, params):
        response = requests.get(url, headers=self.headers, params=params)
        response.encoding = response.apparent_encoding
        return json.loads(response.text)

    def get_data(self, mode='利润表'):
        for params in tqdm(self.params_list()):
            data = self.request(url=self.url_mode[mode], params=params)
            for i in data['data']:
                yield i

    def profit_data(self, mode='利润表'):
        pass
        self.profit_dict = {
            '报告日期': 'REPORT_DATE',
            '报告形式': 'REPORT_TYPE',  # 一季报,中报,三季报,年报
            '营业总收入': 'TOTAL_OPERATE_INCOME',
            '营业收入': 'OPERATE_INCOME',
            '利息收入': 'INTEREST_INCOME',
            '实收保险费': 'EARNED_PREMIUM',
            '手续费及佣金收入': 'FEE_COMMISSION_INCOME',
            '其他营业收入': 'OTHER_BUSINESS_INCOME',
            '营业总成本': 'TOTAL_OPERATE_COST',
            '营业成本': 'OPERATE_COST',
            '研发费用': 'RESEARCH_EXPENSE',
            '营业税金及附加': 'OPERATE_TAX_ADD',
            '销售费用': 'SALE_EXPENSE',
            '管理费用': 'MANAGE_EXPENSE',
            '财务费用': 'FINANCE_EXPENSE',
            '财务费用中利息费用': 'FE_INTEREST_EXPENSE',
            '财务费用中利息收入': 'FE_INTEREST_INCOME',
            '资产减值损失': 'ASSET_IMPAIRMENT_LOSS',
            '信用减值损失': 'CREDIT_IMPAIRMENT_LOSS',
            '其他经营收益': 'TOC_OTHER',
            '公允价值变动收益': 'FAIRVALUE_CHANGE_INCOME',
            '投资收益': 'INVEST_INCOME',
            '对联营企业和合营企业的投资收益': 'INVEST_JOINT_INCOME',
            '净投资收入': 'NET_EXPOSURE_INCOME',
            '汇兑收益': 'EXCHANGE_INCOME',
            '资产处置损益': 'ASSET_DISPOSAL_INCOME',
            '资产减值收入': 'ASSET_IMPAIRMENT_INCOME',
            '其他经营收益中信用减值损失': 'CREDIT_IMPAIRMENT_INCOME',
            '其他收益': 'OTHER_INCOME',
            '营业利润': 'OPERATE_PROFIT',
            '营业外收入': 'NONBUSINESS_INCOME',
            '营业外支出': 'NONBUSINESS_EXPENSE',
            '利润总额': 'TOTAL_PROFIT',
            '所得税': 'INCOME_TAX',
            '净利润': 'NETPROFIT',
            '持续经营净利润': 'CONTINUED_NETPROFIT',
            '非持续经营净利润': 'DISCONTINUED_NETPROFIT',
            '归属于母公司股东的净利润': 'PARENT_NETPROFIT',
            '少数股东权益': 'MINORITY_INTEREST',
            '扣除非经常性损益后的净利润': 'DEDUCT_PARENT_NETPROFIT',
            '其他净利润': 'NETPROFIT_OTHER',
            '基本每股收益': 'BASIC_EPS',
            '稀释每股收益': 'DILUTED_EPS',
            '其他综合收益': 'OTHER_COMPRE_INCOME',
            '归属于母公司股东的其他综合收益': 'PARENT_OCI',
            '少数股东的其他综合收益': 'MINORITY_OCI',
            '综合收益总额': 'TOTAL_COMPRE_INCOME',
            '归属于母公司股东的综合收益总额': 'PARENT_TCI',
            '归属于少数股东的综合收益总额': 'MINORITY_TCI',
            '归属于母公司股东的其他综合收益总额': 'PRECOMBINE_TCI',
            '审计意见': 'OPINION_TYPE',
        }
        #keys = tuple(self.profit_dict.values())
        # for i in list(self.get_data(mode=mode)):
        #    yield [i[key] for key in keys]

    def statement(self, mode='利润表'):
        """
        Args:
            mode (str, optional): '利润表' or '现金流量表' or '资产负债表'. Defaults to '利润表'.

        Returns:
            [type]: dataframe
        """
        result = []
        flag = False
        for i in self.get_data(mode=mode):
            if not flag:
                columns = i.keys()
                flag = True
            result.append(i)
        df = pd.DataFrame(result, columns=columns)
        return df


if __name__ == '__main__':
    fc = FinancialStatements(start_year=2018, start_quater=1,
                             end_year=2019, end_quater=4)
    # fc.get_profit_data()
    fc.statement().to_csv('temp.csv', encoding='utf8', index=False)
