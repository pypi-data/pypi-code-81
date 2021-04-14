from typing import Tuple, List

import pandas as pd
import datetime
from sqlalchemy import func
import numpy as np
from .raw import RawDataApi
from .basic import BasicDataApi
from .derived import DerivedDataApi
from ...util.singleton import Singleton
from ...util.calculator_item import CalculatorBase
from ...util.calculator import Calculator

class PortfolioDataApi(metaclass=Singleton):

    def get_portfolio_nav(self, order_list, fund_type):
        try:
            share_list = {}
            port_amount = 1
            result = []
            group_result = []
            for i in range(len(order_list)):
                trade_date = list(order_list[i].keys())[0]
                if i + 1 < len(order_list):
                    change_date = list(order_list[i + 1].keys())[0]
                else :
                    change_date = datetime.date.today()
                fund_list = list(list(order_list[i].values())[0].keys())
                fund_nav = BasicDataApi().get_fund_nav_with_date(start_date=trade_date,end_date=change_date,fund_list=fund_list)
                fund_nav = fund_nav.pivot_table(index="datetime" , values="adjusted_net_value" , columns="fund_id").dropna()
                dict_share = {}
                for j in range(len(fund_list)):
                    fund_share = port_amount * order_list[i][trade_date][fund_list[j]] / fund_nav.iloc[0][fund_list[j]]
                    dict_share[fund_list[j]] = fund_share
                    fund_nav[fund_list[j]] = fund_nav[fund_list[j]] * fund_share
                
                _result = []
                for index_group, fund_list in fund_type.items():
                    ws = sum([order_list[i][trade_date].get(fund_id,0) for fund_id in fund_list])
                    nav_mul = 1/ws
                    _df = (fund_nav[fund_nav.columns.intersection(fund_list)]*nav_mul).sum(axis=1).to_frame()
                    _df.columns=[index_group]
                    _result.append(_df)
                group_result.append(pd.concat(_result,axis=1))
                share_list[trade_date] =  dict_share 
                port_amount = sum(fund_nav.iloc[-1])
                if i == 0 : 
                    result.append(fund_nav)
                    fund_nav = fund_nav.sum(axis = 1).to_frame()
                    fund_nav.columns = ["组合"]
                    port_mv = fund_nav
                else :
                    result.append(fund_nav)
                    fund_nav = fund_nav.sum(axis = 1).to_frame()
                    fund_nav.columns = ["组合"]
                    port_mv = port_mv.append(fund_nav.iloc[1:])
            port_fund_nav = pd.concat(result)
            port_fund_weight = port_fund_nav.div(port_fund_nav.sum(axis=1), axis=0)
            port_fund_group = pd.concat(group_result)
            data = {
                '净值':port_mv,
                '各基净值':port_fund_nav,
                '各基权重':port_fund_weight,
                '大类净值':port_fund_group,
                '持有信息':share_list,
            }
            return data
        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_portfolio_mv')


    def get_portfolio_benchmark_info(self):
        try:
            index_info = BasicDataApi().get_index_info(index_list=['hs300','national_debt','csi500','gem','sp500rmb','mmf','hsi'])
            res = []
            for r in index_info.itertuples():
                res.append([r.index_id, r.desc_name])
            return res

        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_portfolio_benchmark_info')

    def get_portfolio_mv(self, fund_nav, index_id, begin_date, end_date, time_para):
        try:
            fund_nav.columns=['组合']
            basic = BasicDataApi()
            index_price = basic.get_index_price_dt(index_list=[index_id],start_date=fund_nav.index[0] - datetime.timedelta(days=10),end_date=fund_nav.index[-1]).pivot_table(index='datetime',columns='index_id',values='close')
            index_info = basic.get_index_info([index_id])
            name_dic = index_info.set_index('index_id').to_dict()['desc_name']
            begin_date, end_date = RawDataApi().get_date_range(time_para, begin_date, end_date)
            df = pd.merge(fund_nav.reset_index(), index_price.reset_index(),how='outer').set_index('datetime').sort_index().ffill().dropna()
            df = df.loc[begin_date:end_date]
            df = df / df.iloc[0]
            df.loc[:,'价格比'] = df.组合 / df[index_id]
            df = df.rename(columns=name_dic)
            return df
        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_portfolio_mv')

    def get_portfolio_cur_mdd(self, fund_nav, begin_date, end_date, time_para):
        try:            
            begin_date, end_date = RawDataApi().get_date_range(time_para, begin_date, end_date)
            fund_nav = fund_nav.loc[begin_date:end_date]
            df = fund_nav / fund_nav.cummax() - 1
            df.columns=['历史回撤']
            df_min = df['历史回撤'].min()
            data = {
                '历史回撤': df,
                '最低值': df_min,
            }
            return data
        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_portfolio_cur_mdd')

    def get_portfolio_ret_distribution(self, fund_nav, period, begin_date, end_date, time_para):
        try:
            begin_date, end_date = RawDataApi().get_date_range(time_para, begin_date, end_date)
            fund_nav = fund_nav.loc[begin_date:end_date]    
            fund_nav = CalculatorBase.data_resample_weekly_nav(df=fund_nav, rule=period)
            ret = fund_nav.pct_change(1).iloc[1:]
            ret.columns=['收益']
            result = np.histogram(a=ret['收益'],bins=8)
            data = {'分布_频度':result[0].tolist(),
                '分布_收益':result[1].round(3).tolist(),
                '收益':ret
            }
            return data
        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_portfolio_cur_mdd')

    def get_portfolio_stats(self, fund_nav, index_id):
        try:
            fund_nav.columns=['组合']
            basic = BasicDataApi()
            index_price = basic.get_index_price_dt(index_list=[index_id],start_date=fund_nav.index[0] - datetime.timedelta(days=10),end_date=fund_nav.index[-1]).pivot_table(index='datetime',columns='index_id',values='close')
            index_info = basic.get_index_info([index_id])
            name_dic = index_info.set_index('index_id').to_dict()['desc_name']
            df = pd.merge(fund_nav.reset_index(), index_price.reset_index(),how='outer').set_index('datetime').sort_index().ffill().dropna()
            df = df / df.iloc[0]
            df = df.rename(columns=name_dic)
            result = []
            for col in df:
                res_status = Calculator.get_benchmark_stat_result(dates=df.index,
                                                                values=df[col],
                                                                benchmark_values=df[name_dic[index_id]],
                                                                frequency = '1W',
                                                                risk_free_rate=0.025, )
                
                indicators_tem={
                    '开始日期': res_status.start_date,
                    '截止日期': res_status.end_date,
                    '累计收益': str(round((res_status.last_unit_nav-1)*100,2)) + "%",
                    '最近一月收益':str(round(res_status.recent_1m_ret*100 ,2)) + "%",
                    '年化收益率': str(round(res_status.annualized_ret*100 ,2)) + "%",
                    '年化波动率': str(round(res_status.annualized_vol*100 ,2)) + "%",
                    '夏普比率': round(res_status.sharpe,2),
                    '最大回撤': str(round(res_status.mdd*100 ,2)) + "%",
                    '最大回撤开始日期': res_status.mdd_date1,
                    '最大回撤结束日期': res_status.mdd_date2,
                    '最大回撤持续时长': res_status.mdd_lens,
                    '卡玛比率': round(res_status.ret_over_mdd ,2),
                    '下行标准差': str(round(res_status.downside_std*100 ,2)) + "%",
                    'alpha': str(round(res_status.alpha*100 ,2)) + "%",
                    'beta': round(res_status.beta ,2),
                    '信息比率': round(res_status.ir ,2),
                    'CL模型_alpha': str(round(res_status.alpha_cl*100 ,2)) + "%",
                    'CL模型_beta': str(round(res_status.beta_cl*100 ,2)) + "%",
                    '相对胜率': str(round(res_status.win_rate*100 ,2)) + "%",
                    '绝对胜率': str(round(res_status.win_rate_0*100 ,2)) + "%",
                    'name':col
                }
                if col != '组合':
                    indicators_tem['alpha'] = '-'
                    indicators_tem['beta'] = '-'
                    indicators_tem['信息比率'] = '-'
                    indicators_tem['CL模型_alpha'] = '-'
                    indicators_tem['CL模型_beta'] = '-'
                    indicators_tem['相对胜率'] = '-'
                result.append(indicators_tem)
            df = pd.DataFrame(result).set_index('name').T
            return df
        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_portfolio_stats')

    def get_rolling_corr(self, fund_navs, frequency, windows, step):
        try:
            fund_navs_period = CalculatorBase.data_resample_weekly_nav(df=fund_navs, rule=frequency)
            fund_ret = fund_navs_period.pct_change(1).iloc[1:]  
            # 弱鸡排列
            col_pair = []
            cols = fund_ret.columns.tolist()
            for idx_i, col_i in enumerate(cols):
                cols_list = cols[idx_i+1:]
                for idx_j, col_j in enumerate(cols_list):
                    col_pair.append([col_i,col_j])

            corr_result_df = []
            for col_pair_i in col_pair:
                df = fund_ret[col_pair_i]
                idx_list = df.reset_index().index.tolist()
                corr_result = []
                b = idx_list[0]
                _result = []
                
                # 计算窗口划分 不包含min_windows概念
                while(1):
                    e = b + windows
                    if e > idx_list[-1]:
                        break
                    else:
                        _result.append([b,e])
                        b += step

                # 计算部分
                for idxs in _result:
                    _df = df.iloc[idxs[0]:idxs[1]]
                    corr_result.append({'datetime':_df.index[-1], f'{col_pair_i[0]}_{col_pair_i[1]}':_df.corr().iloc[1,0]})
                df = pd.DataFrame(corr_result).set_index('datetime')
                corr_result_df.append(df)
            df = pd.concat(corr_result_df,axis=1)
            return df
        
        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_rolling_corr')
    
    def get_port_fund_list(self, order_list):
        try:
            fund_list = []
            for order in order_list:
                for d, fund_wgt in order.items():
                    fund_list.extend(list(fund_wgt))
            return list(set(fund_list))
        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_port_fund_list')

    def get_port_fund_pos_date(self,fund_id, order_list,index_id): 
        try:
            basic = BasicDataApi()
            begin_date, end_date = RawDataApi().get_date_range(time_para='ALL', begin_date=None, end_date=None)
            fund_nav = basic.get_fund_nav(fund_list=[fund_id])
            fund_nav = fund_nav.pivot_table(columns='fund_id',index='datetime',values='adjusted_net_value')
            index_price = basic.get_index_price(index_list=[index_id])
            index_price = index_price.pivot_table(columns='index_id',index='datetime',values='close')
            nav_df = fund_nav.join(index_price).ffill().dropna()
            
            result = []
            for order in order_list:
                for d, fund_wgt in order.items():
                    fund_wgt['datetime'] = d
                    result.append(fund_wgt)

            weight_df = pd.DataFrame(result).set_index('datetime')
            pos_con = 1 - weight_df[fund_id].isnull()
            result = []
            is_empty = True
            for r in pos_con.iteritems():
                if is_empty and r[1] == 1:
                    dic = {'begin_date':r[0]}
                    is_empty = False
                elif not is_empty and r[1] == 0:
                    dic['end_date'] = r[0]
                    result.append(dic)
                    dic = {}
                    is_empty = True
            if not is_empty:
                dic['end_date'] = end_date
                result.append(dic)
            data = {
                '净值':nav_df,
                '持有期':result}
            return data
        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_port_fund_pos_date')

    def get_port_ret_resolve_date_range(self, order_list):
        try:
            
            begin_date, end_date = RawDataApi().get_date_range(time_para='ALL', begin_date=None, end_date=None)
            begin_date = list(order_list[0].keys())[0]
            data = {'begin_date':begin_date,'end_date':end_date}
            return data
        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_port_ret_resolve_date_range')
    
    def get_port_ret_resolve(self, share_list , begin_date , end_date):
        try:
            basic = BasicDataApi()
            all_ret_dict = []
            for i in range(len(list(share_list.keys()))):
                this_date = list(share_list.keys())[i]
                if i+1 < len(list(share_list.keys())) :
                    next_date = list(share_list.keys())[i+1]
                else :
                    next_date = datetime.date.today()

                if next_date <= begin_date: 
                    continue
                elif next_date <= end_date: 
                    cal_end = next_date
                elif next_date > end_date: 
                    cal_end = end_date

                if this_date >= end_date: 
                    break
                elif this_date <= begin_date: 
                    cal_start = begin_date
                elif this_date > begin_date: 
                    cal_start = this_date
                ret_dict = {}
                for fund_id in list(share_list[this_date].keys()):
                    fund_share = share_list[this_date][fund_id]
                    fund_nav = basic.get_fund_nav_with_date(start_date=cal_start,end_date=cal_end,fund_list=[fund_id])
                    fund_nav = fund_nav.pivot_table(index="datetime" , values="adjusted_net_value" , columns="fund_id").dropna()
                    fund_ret = round((fund_nav.iloc[-1].values[0] * fund_share - fund_nav.iloc[0].values[0] * fund_share)*100,2)
                    ret_dict[fund_id] = fund_ret
                all_ret_dict.append(ret_dict)
            return all_ret_dict
        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_port_ret_resolve')

    def get_port_fund_weight(self, fund_wgt, fund_type):
        try:
            fund_info = BasicDataApi().get_fund_info(fund_wgt.columns.tolist())
            name_dic = fund_info.set_index('fund_id').to_dict()['desc_name']
            fund_wgt = fund_wgt.rename(columns=name_dic)
            result = {}
            for types, fund_list in fund_type.items():
                result[types] = [name_dic[_] for _ in fund_list]
            data = {
                '权重':fund_wgt,
                '类型':result,
            }
            return data
        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_port_fund_weight')