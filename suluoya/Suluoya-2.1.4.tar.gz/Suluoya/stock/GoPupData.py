import os
import sys

import pandas as pd
from tqdm import tqdm

sys.path.append(os.path.dirname(__file__) + os.sep + '../')
try:
    from ..log.SlyLog import sprint
except:
    from log.SlyLog import sprint


class Macroeconomic(object):

    def __init__(self):
        import gopup as gp
        self.gp = gp
        self.g = self.gp.pro_api(token='4438684c9995613c2637de7c3264c455')
        self.sprint = sprint()

    def exchange_rate(self, currency_list=['美元', '欧元'],
                      start_date='20201010', end_date='20201015'):
        '''
        汇率
        美元、欧元、日元、英镑、卢布、韩元、澳元、加元、泰铢、港币、台币、新币
        '''
        date_range = pd.date_range(start_date, end_date, freq='1D')
        lists = []
        self.sprint.blue('getting exchange rate data...')
        for date in tqdm(date_range):
            for currency in currency_list:
                df = self.g.exchange_rate(
                    date=str(date.date()), currency=currency)
                lists.append(df)
        return pd.concat(lists)

    @property
    def get_rrr(self):
        '''
        存款准备金率
        公布时间
        生效时间
        大型金融机构 调整前
        大型金融机构 调整后
        大型金融机构 调整幅度
        中小型金融机构 调整前
        中小型金融机构 调整后
        中小型金融机构 调整幅度
        消息公布次日指数涨跌 上证
        消息公布次日指数涨跌 深证
        备注
        '''
        df = self.gp.get_rrr()
        return df


if __name__ == '__main__':
    mc = Macroeconomic()
    mc.get_rrr.to_excel('rate.xlsx',encoding='utf8')
