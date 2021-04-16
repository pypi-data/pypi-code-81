
from typing import List, Optional, Tuple, Union, Dict
from collections import defaultdict
import datetime
import json
import io
import traceback
import math

import numpy as np
import pandas as pd

from sqlalchemy.orm import sessionmaker

from ...util.singleton import Singleton
from ...util.wechat_bot import WechatBot
from ...util.calculator import Calculator
from ...util.aip_calc import xirr
from ...constant import HoldingAssetType, FOFTradeStatus
from ..api.basic import BasicDataApi
from ..api.derived import DerivedDataApi
from ..view.basic_models import HedgeFundInfo, FOFInfo, HedgeFundNAV, FOFInvestorPosition, FOFInvestorPositionSummary
from ..view.derived_models import FOFNavCalc, FOFPosition, FOFInvestorData, FOFPositionDetail
from ..wrapper.mysql import BasicDatabaseConnector, DerivedDatabaseConnector
from ..nav_reader.hedge_fund_nav_reader import HedgeFundNAVReader


class FOFDataManagerLite(metaclass=Singleton):

    _DAYS_PER_YEAR_FOR_INTEREST = 360

    def __init__(self):
        # pd.set_option('display.max_rows', None)
        # pd.set_option('display.max_columns', None)
        # pd.set_option('display.float_format', lambda x: '%.4f' % x)
        self._start_date: Optional[str] = None
        self._end_date: Optional[str] = None
        self._date_list: Optional[np.ndarray] = None
        self._fof_scale: Optional[pd.DataFrame] = None
        self._fof_redemp: Optional[pd.DataFrame] = None
        self._asset_allocation: Optional[pd.DataFrame] = None
        self._hedge_pos: Optional[pd.DataFrame] = None
        self._hedge_nav: Optional[pd.DataFrame] = None
        self._fund_pos: Optional[pd.DataFrame] = None
        self._manually: Optional[pd.DataFrame] = None
        self._fof_nav: Optional[pd.DataFrame] = None
        self._fof_position: Optional[pd.DataFrame] = None
        self._fof_investor_pos: Optional[pd.DataFrame] = None
        self._fof_position_details: Optional[pd.DataFrame] = None
        self._total_net_assets: float = None
        self._total_shares: float = None

        self._wechat_bot = WechatBot()

    def _get_days_this_year_for_fee(self, the_date: datetime.date) -> int:
        '''计算今年一共有多少天'''
        return pd.Timestamp(year=the_date.year, month=12, day=31).dayofyear

    @staticmethod
    def _do_calc_v_net_value(nav: Union[pd.Series, pd.DataFrame, float], unit_total, acc_nav: pd.Series, init_water_line: pd.Series, incentive_fee_ratio: Union[pd.Series, float], decimals: Union[pd.Series, float]) -> pd.Series:
        # 盈利
        excess_ret = acc_nav - init_water_line
        # 盈 或 亏
        earn_con = (excess_ret > 0).astype('int')
        # 费
        pay_mng_fee = ((unit_total * excess_ret * earn_con).round(2) * incentive_fee_ratio).round(2)
        # 通过MV来算出净值
        unit_total_sum = unit_total.sum()
        mv = (nav * unit_total_sum).round(2)
        mv -= pay_mng_fee.sum()
        v_nav = (mv / unit_total_sum).round(decimals)
        return v_nav

    @staticmethod
    def _do_calc_v_net_value_by_nav(nav: Union[pd.Series, pd.DataFrame, float], acc_nav: pd.Series, init_water_line: pd.Series, incentive_fee_ratio: Union[pd.Series, float], decimals: Union[pd.Series, float]) -> pd.Series:
        # 盈利
        excess_ret = acc_nav - init_water_line
        # 盈 或 亏
        earn_con = (excess_ret > 0).astype('int')
        # 费
        pay_mng_fee = ((excess_ret * earn_con).round(2) * incentive_fee_ratio).round(2)
        # 净值
        v_nav = (nav - pay_mng_fee).round(decimals)
        return v_nav

    @staticmethod
    def _calc_virtual_net_value(manager_id, fof_id, fund_list, asset_allocation=None):
        '''计算虚拟净值'''
        fund_info = FOFDataManagerLite.get_hedge_fund_info(fund_list)
        # TODO: 目前只支持高水位法计算
        fund_info = fund_info.loc[fund_info.incentive_fee_mode == '高水位法']
        fund_info = fund_info.set_index('fund_id')
        incentive_fee_ratio = fund_info['incentive_fee_ratio'].to_dict()
        v_nav_decimals = fund_info['v_nav_decimals'].to_dict()

        df = FOFDataManagerLite.get_hedge_fund_nav(fund_list)
        df = df[df.fund_id.isin(fund_info.index.array)]

        if asset_allocation is None:
            asset_allocation = FOFDataManagerLite.get_fof_asset_allocation(manager_id, [fof_id])
        asset_allocation = asset_allocation.loc[(asset_allocation.asset_type == HoldingAssetType.HEDGE) & (asset_allocation.fund_id.isin(fund_list)), :]
        df = df.append(asset_allocation.loc[asset_allocation.event_type.isin([FOFTradeStatus.PURCHASE, FOFTradeStatus.SUBSCRIBE]), ['datetime', 'fund_id', 'water_line', 'nav']].rename(columns={'water_line': 'acc_unit_value', 'nav': 'net_asset_value'}))
        df = df.drop_duplicates(subset=['fund_id', 'datetime'])
        asset_allocation = asset_allocation.set_index('datetime')

        date_list: np.ndarray = pd.date_range(df.datetime.sort_values().array[0], datetime.datetime.now().date()).date
        nav = df.pivot(index='datetime', columns='fund_id', values=['net_asset_value', 'acc_unit_value'])
        nav = nav.reindex(date_list).ffill().stack().reset_index(level='fund_id')

        v_nav_result = []
        datas_to_calc_v = defaultdict(list)
        for row in nav.itertuples():
            try:
                one = asset_allocation.loc[[row.Index], :]
                one = one.loc[one.fund_id == row.fund_id, :]
            except KeyError:
                pass
            else:
                for one_in_date in one.itertuples():
                    if one_in_date.event_type in (FOFTradeStatus.DEDUCT_REWARD_AND_DIVIDEND_VOLUME, FOFTradeStatus.DEDUCT_REWARD):
                        assert one_in_date.fund_id in datas_to_calc_v, '!!!!'
                        fund_data = datas_to_calc_v[one_in_date.fund_id]
                        if one_in_date.event_type == FOFTradeStatus.DEDUCT_REWARD_AND_DIVIDEND_VOLUME:
                            total_share = one_in_date.share
                        else:
                            total_share = -one_in_date.share
                        for a_trade in fund_data:
                            assert a_trade[1] < one_in_date.Index, '!!!'
                            total_share += a_trade[2]
                        datas_to_calc_v[one_in_date.fund_id] = [(one_in_date.fund_id, one_in_date.Index, total_share, one_in_date.water_line)]
                    if one_in_date.event_type in (FOFTradeStatus.PURCHASE, FOFTradeStatus.SUBSCRIBE, FOFTradeStatus.DIVIDEND_VOLUME):
                        datas_to_calc_v[one_in_date.fund_id].append((one_in_date.fund_id, one_in_date.Index, one_in_date.share, one_in_date.water_line if not pd.isnull(one_in_date.water_line) else one_in_date.nav))

            df = pd.DataFrame(datas_to_calc_v[row.fund_id], columns=['fund_id', 'datetime', 'unit_total', 'water_line'])
            if df.empty:
                continue
            v_nav = FOFDataManagerLite._do_calc_v_net_value(row.net_asset_value, df.unit_total.iloc[[-1]], row.acc_unit_value, df.water_line.iloc[[-1]], incentive_fee_ratio[row.fund_id], v_nav_decimals[row.fund_id])
            v_nav_result.append({'datetime': row.Index, 'fund_id': row.fund_id, 'v_nav': v_nav})
        df = pd.DataFrame.from_dict(v_nav_result)
        if not df.empty:
            df = df.pivot(index='datetime', columns='fund_id', values='v_nav')
        return df

    def _calc_adj_nav_for_a_fund(df: pd.DataFrame):
        net_asset_value = df.net_asset_value
        if df.shape[0] < 2:
            return pd.Series({'datetime': df.datetime.array[-1], 'ta_factor': 1, 'adj_nav': net_asset_value.array[-1]})

        acc_unit_value = df.acc_unit_value
        last_diff = round(acc_unit_value.array[-2] - net_asset_value.array[-2], 6)
        this_diff = round(acc_unit_value.array[-1] - net_asset_value.array[-1], 6)
        assert math.isclose(this_diff - last_diff, 0) or (this_diff > last_diff), f'!!!(fund_id){df.fund_id.array[0]} (this_diff){this_diff} (last_diff){last_diff}'

        if math.isclose(last_diff, this_diff):
            ta_factor = df.ta_factor.array[-2]
        else:
            dividend = this_diff - last_diff
            ta_factor = df.ta_factor.array[-2] * (1 + dividend / (net_asset_value.array[-2] - dividend))
        if ta_factor is None:
            ta_factor = 1
        adj_nav = net_asset_value.array[-1] * ta_factor
        return pd.Series({'datetime': df.datetime.array[-1], 'ta_factor': ta_factor, 'adj_nav': adj_nav})

    @staticmethod
    def _calc_adjusted_net_value(fund_list: List[str]):
        '''计算复权净值'''

        df = FOFDataManagerLite.get_hedge_fund_nav(fund_list)
        return df.groupby(by='fund_id', sort=False).apply(FOFDataManagerLite._calc_adj_nav_for_a_fund)

    def _init(self, manager_id: str, fof_id: str, debug_mode=False):
        def _calc_water_line_and_confirmed_nav(x):
            x = x.reset_index()
            x_with_water_line = x[x.water_line.notna()]
            return pd.Series({'confirmed_nav': json.dumps(x[['share', 'nav']].to_dict(orient='records')),
                              'water_line': json.dumps(x_with_water_line[['share', 'water_line']].to_dict(orient='records'))})

        # 获取fof基本信息
        fof_info: Optional[pd.DataFrame] = FOFDataManagerLite.get_fof_info(manager_id, [fof_id])
        assert fof_info is not None, f'get fof info for {manager_id}/{fof_id} failed'

        self._MANAGEMENT_FEE_PER_YEAR = fof_info.management_fee
        self._CUSTODIAN_FEE_PER_YEAR = fof_info.custodian_fee
        self._ADMIN_SERVICE_FEE_PER_YEAR = fof_info.administrative_fee
        self._DEPOSIT_INTEREST_PER_YEAR = fof_info.current_deposit_rate if fof_info.current_deposit_rate is not None else 0.003
        self._SUBSCRIPTION_FEE = fof_info.subscription_fee
        self._ESTABLISHED_DATE = fof_info.established_date
        self._INCENTIVE_FEE_MODE = fof_info.incentive_fee_mode
        if debug_mode:
            print(f'fof info: (manager_id){manager_id} (fof_id){fof_id} (management_fee){self._MANAGEMENT_FEE_PER_YEAR} (custodian_fee){self._CUSTODIAN_FEE_PER_YEAR} '
                  f'(admin_service_fee){self._ADMIN_SERVICE_FEE_PER_YEAR} (current_deposit_rate){self._DEPOSIT_INTEREST_PER_YEAR} (subscription_fee){self._SUBSCRIPTION_FEE} '
                  f'(incentive_fee_mode){self._INCENTIVE_FEE_MODE} (established_date){self._ESTABLISHED_DATE})')

        # 获取FOF份额变化信息
        fof_scale = DerivedDataApi().get_hedge_fund_investor_pur_redemp(manager_id, [fof_id])
        # 客户认购/申购记录
        self._fof_scale = fof_scale[fof_scale.event_type.isin([FOFTradeStatus.SUBSCRIBE, FOFTradeStatus.PURCHASE])].set_index('datetime')
        self._start_date = self._fof_scale.index.min()
        # 客户赎回记录
        self._fof_redemp = fof_scale[fof_scale.event_type.isin([FOFTradeStatus.REDEEM, ])].set_index('datetime')

        # trading_day_list = BasicDataApi().get_trading_day_list(start_date=self._start_date, end_date=datetime.datetime.now().date())
        # 将昨天作为end_date
        self._end_date = datetime.datetime.now().date() - datetime.timedelta(days=1)
        if debug_mode:
            print(f'(start_date){self._start_date} (end_date){self._end_date}')
        self._date_list: np.ndarray = pd.date_range(self._start_date, self._end_date).date

        # 获取fof持仓
        self._asset_allocation: Optional[pd.DataFrame] = FOFDataManagerLite.get_fof_asset_allocation(manager_id, [fof_id])
        assert self._asset_allocation is not None, f'get fof pos for {manager_id}/{fof_id} failed'

        positions = self._asset_allocation.loc[self._asset_allocation.event_type.isin([FOFTradeStatus.PURCHASE, FOFTradeStatus.SUBSCRIBE]), :]
        self._water_line_and_confirmed_nav = positions.groupby(by='fund_id', sort=False).apply(_calc_water_line_and_confirmed_nav)
        self._total_cost = positions.pivot(index='datetime', columns=['fund_id'], values='amount').sum()
        positions = positions.pivot(index='datetime', columns=['asset_type', 'fund_id'], values='share')
        positions = positions.reindex(index=self._date_list).cumsum().ffill()
        # 持仓中的公募基金
        try:
            self._fund_pos = positions[HoldingAssetType.MUTUAL]
        except KeyError:
            print('no fund pos found')

        # 持仓中的私募基金
        try:
            self._hedge_pos = positions[HoldingAssetType.HEDGE]
        except KeyError:
            print('no hedge pos found')

        # 获取私募基金净值数据
        if self._hedge_pos is not None:
            hedge_fund_list = list(self._hedge_pos.columns.unique())
            hedge_fund_nav = FOFDataManagerLite.get_hedge_fund_nav(hedge_fund_list)
            hedge_fund_nav = hedge_fund_nav.pivot(index='datetime', columns='fund_id').reindex(index=self._date_list)
            self._hedge_nav = hedge_fund_nav['v_net_value']
            self._all_latest_nav = hedge_fund_nav['net_asset_value'].ffill().iloc[-1, :]
            self._all_latest_acc_nav = hedge_fund_nav['acc_unit_value'].ffill().iloc[-1, :]
            self._latest_nav_date = hedge_fund_nav['net_asset_value'].apply(lambda x: x[x.notna()].index.array[-1])

            # 我们自己算一下虚拟净值 然后拿它对_hedge_nav查缺补漏
            v_nav_calcd = FOFDataManagerLite._calc_virtual_net_value(manager_id, fof_id, hedge_fund_list, self._asset_allocation)
            # 最后再ffill
            # self._hedge_nav = self._hedge_nav.combine_first(v_nav_calcd.reindex(index=self._date_list)).ffill()
            # TODO: 这里虚拟净值只能先全用自己算的
            self._hedge_nav = v_nav_calcd.reindex(index=self._date_list).ffill()
            if debug_mode:
                print(self._hedge_nav)
            self._hedge_latest_v_nav = self._hedge_nav.iloc[-1, :]
        else:
            self._all_latest_nav = None
            self._latest_nav_date = None
            self._all_latest_acc_nav = None
            self._hedge_latest_v_nav = None

        # 获取人工手工校正信息
        manually = BasicDataApi().get_fof_assert_correct(manager_id, fof_id)
        self._manually = manually.set_index('date')

    def _get_hedge_mv(self):
        if self._hedge_pos is None:
            return
        else:
            return (self._hedge_nav * self._hedge_pos).round(2).sum(axis=1).fillna(0)

    def _get_fund_mv(self):
        if self._fund_pos is None:
            return
        else:
            return (self._fund_pos * self._fund_nav).round(2).sum(axis=1).fillna(0)

    def calc_fof_nav(self, manager_id: str, fof_id: str, dump_to_db=True, is_from_excel=False, debug_mode=False):
        self._init(manager_id=manager_id, fof_id=fof_id, debug_mode=debug_mode)

        if self._fund_pos is not None:
            fund_list: List[str] = self._fund_pos.columns.to_list()
            fund_info: Optional[pd.DataFrame] = BasicDataApi().get_fund_info(fund_list=fund_list)
            assert fund_info is not None, f'get fund info of {fund_list} failed'
            monetary_fund: List[str] = fund_info[fund_info.wind_class_1.isin(['货币市场型基金'])].fund_id.to_list()

            # 根据公募基金持仓获取相应基金的净值
            fund_nav: Optional[pd.DataFrame] = BasicDataApi().get_fund_nav_with_date_range(start_date=self._start_date, end_date=self._end_date, fund_list=fund_list)
            assert fund_nav is not None, f'get fund nav of {fund_list} failed'
            fund_nav = fund_nav.pivot(index='datetime', columns='fund_id')
            if self._latest_nav_date is not None:
                self._latest_nav_date = self._latest_nav_date.append(fund_nav['unit_net_value'].apply(lambda x: x[x.notna()].index.array[-1].date()))
            else:
                self._latest_nav_date = fund_nav['unit_net_value'].apply(lambda x: x[x.notna()].index.array[-1].date())
            fund_nav = fund_nav.reindex(index=self._date_list)
            self._monetary_daily_profit = fund_nav['daily_profit'][monetary_fund].fillna(0)
            fund_nav = fund_nav.ffill()
            if self._all_latest_acc_nav is not None:
                self._all_latest_acc_nav = self._all_latest_acc_nav.append(fund_nav['acc_net_value'].iloc[-1, :])
            else:
                self._all_latest_acc_nav = fund_nav['acc_net_value'].iloc[-1, :]
            self._fund_nav = fund_nav['unit_net_value']
            if self._all_latest_nav is not None:
                self._all_latest_nav = self._all_latest_nav.append(self._fund_nav.iloc[-1, :])
            else:
                self._all_latest_nav = self._fund_nav.iloc[-1, :]
        else:
            self._monetary_daily_profit = None
        # 公募基金总市值
        fund_mv: pd.DataFrame = self._get_fund_mv()

        # 获取FOF资产配置信息
        asset_alloc = self._asset_allocation.set_index('datetime')

        hedge_fund_mv = self._get_hedge_mv()

        # 循环遍历每一天来计算
        shares_list = pd.Series(dtype='float64', name='share')
        other_assets_list = pd.Series(dtype='float64', name='cash')
        fof_nav_list = pd.Series(dtype='float64', name='nav')
        today_fund_mv_list = pd.Series(dtype='float64', name='total_fund_mv')
        today_hedge_mv_list = pd.Series(dtype='float64', name='total_hedge_mv')
        net_assets_list = pd.Series(dtype='float64', name='net_asset')
        net_assets_fixed_list = pd.Series(dtype='float64', name='net_asset_fixed')
        management_fee_list = pd.Series(dtype='float64', name='management_fee')
        custodian_fee_list = pd.Series(dtype='float64', name='custodian_fee')
        administrative_fee_list = pd.Series(dtype='float64', name='administrative_fee')
        deposit_interest_list = pd.Series(dtype='float64', name='interest')
        positions_list = pd.Series(dtype='float64', name='position')
        investor_pos_list = []
        for date in self._date_list:
            total_amount = 0
            share_increased = 0

            try:
                scale_data = self._fof_scale.loc[[date], :]
            except KeyError:
                pass
            else:
                # 后边都是汇总信息了 所以在这里先加一下记录
                to_append_to_investor_pos = scale_data.loc[:, ['fof_id', 'investor_id', 'purchase_amount', 'raising_interest', 'share_changed', 'event_type']]
                to_append_to_investor_pos['purchase_amount'] = to_append_to_investor_pos.purchase_amount.add(to_append_to_investor_pos.raising_interest, fill_value=0)
                investor_pos_list.append(to_append_to_investor_pos.rename(columns={'purchase_amount': 'amount'}))

                purchase_sum = scale_data.purchase_amount.sum() + scale_data.raising_interest.sum()
                share_sum = scale_data.share_changed.sum()
                assert not pd.isnull(purchase_sum), '!!!'
                total_amount += purchase_sum
                assert not pd.isnull(share_sum), '!!!'
                share_increased += share_sum

            if other_assets_list.empty:
                other_assets = 0
            else:
                other_assets = other_assets_list.iat[-1]
            other_assets += total_amount

            try:
                # 看看当天有没有卖出FOF
                redemp_data = self._fof_redemp.loc[[date], :]
            except KeyError:
                # 处理没有赎回的情况
                total_amount_redemp = 0
            else:
                # 后边都是汇总信息了 所以在这里先加一下记录
                investor_pos_list.append(redemp_data.loc[:, ['fof_id', 'investor_id', 'redemp_confirmed_amount', 'share_changed', 'event_type']].rename(columns={'redemp_confirmed_amount': 'amount'}))

                # TODO 处理水位线
                # 汇总今天所有的赎回资金
                total_amount_redemp = redemp_data.redemp_confirmed_amount.sum()
                share_increased += redemp_data.share_changed.sum()
                other_assets -= total_amount_redemp
            finally:
                share_increased = round(share_increased, 2)
                other_assets = round(other_assets, 2)

            if not math.isclose(total_amount, 0) or not math.isclose(total_amount_redemp, 0):
                if debug_mode:
                    print(f'{manager_id}/{fof_id} share changed (date){date} (amount){total_amount} (redemp_amount){total_amount_redemp} (share){share_increased}')

            # 这个日期之后才正式成立，所以在此之前都不需要处理后续步骤
            if date < self._ESTABLISHED_DATE:
                other_assets_list.loc[date] = other_assets
                if not math.isclose(share_increased, 0):
                    shares_list.loc[date] = share_increased
                continue

            try:
                expenses = 0
                today_asset_alloc = asset_alloc.loc[[date], :]
                for row in today_asset_alloc.itertuples():
                    if row.event_type in (FOFTradeStatus.PURCHASE, FOFTradeStatus.SUBSCRIBE):
                        assert not pd.isnull(row.amount), '!!!'
                        expenses += row.amount
                    if row.event_type in (FOFTradeStatus.DEDUCT_REWARD, FOFTradeStatus.DIVIDEND_VOLUME, FOFTradeStatus.DEDUCT_REWARD_AND_DIVIDEND_VOLUME):
                        assert not pd.isnull(row.share), '!!!'
                        if row.event_type in (FOFTradeStatus.DIVIDEND_VOLUME, FOFTradeStatus.DEDUCT_REWARD_AND_DIVIDEND_VOLUME):
                            if row.asset_type == HoldingAssetType.HEDGE:
                                self._hedge_pos.loc[self._hedge_pos.index >= date, row.fund_id] += row.share
                            elif row.asset_type == HoldingAssetType.MUTUAL:
                                self._fund_pos.loc[self._fund_pos.index >= date, row.fund_id] += row.share
                        else:
                            if row.asset_type == HoldingAssetType.HEDGE:
                                self._hedge_pos.loc[self._hedge_pos.index >= date, row.fund_id] -= row.share
                            elif row.asset_type == HoldingAssetType.MUTUAL:
                                self._fund_pos.loc[self._fund_pos.index >= date, row.fund_id] -= row.share
                        # 重刷hedge_fund_mv
                        hedge_fund_mv = self._get_hedge_mv()
                        fund_mv = self._get_fund_mv()
                    if row.event_type == FOFTradeStatus.DIVIDEND_CASH:
                        other_assets += row.amount
                assert other_assets >= expenses, f'no enough cash to buy asset!! (date){date} (total cash){total_cash}'
                other_assets -= expenses
            except KeyError:
                pass

            try:
                today_asset_redemp = asset_alloc.loc[[date], :]
                for row in today_asset_redemp.itertuples():
                    if row.event_type in (FOFTradeStatus.REDEEM, ):
                        if row.asset_type == HoldingAssetType.HEDGE:
                            self._hedge_pos.loc[self._hedge_pos.index >= date, row.fund_id] -= row.share
                            hedge_fund_mv = self._get_hedge_mv()
                        elif row.asset_type == HoldingAssetType.MUTUAL:
                            redemp_share = row.share
                            if self._monetary_daily_profit is not None and row.fund_id in self._monetary_daily_profit.columns:
                                redemp_share += round(redemp_share * self._monetary_daily_profit.shift(1).at[date, row.fund_id] / 10000, 2)
                            self._fund_pos.loc[self._fund_pos.index >= date, row.fund_id] -= redemp_share
                            fund_mv = self._get_fund_mv()
                        other_assets += row.amount
            except KeyError:
                pass

            # 处理货基
            if self._monetary_daily_profit is not None:
                for fund_id, col in self._monetary_daily_profit.iteritems():
                    if not pd.isnull(self._fund_pos.at[date, fund_id]) and not math.isclose(self._fund_pos.at[date, fund_id], 0):
                        self._fund_pos.loc[self._fund_pos.index >= date, fund_id] += round(self._fund_pos.at[date, fund_id] * col[date] / 10000, 2)
                fund_mv = self._get_fund_mv()

            # 计提管理费, 计提行政服务费, 计提托管费
            if not net_assets_list.empty:
                management_fee_list.loc[date] = round(net_assets_list.iat[-1] * self._MANAGEMENT_FEE_PER_YEAR / self._get_days_this_year_for_fee(date), 2)
                custodian_fee_list.loc[date] = round(net_assets_list.iat[-1] * self._CUSTODIAN_FEE_PER_YEAR / self._get_days_this_year_for_fee(date), 2)
                administrative_fee_list.loc[date] = round(net_assets_list.iat[-1] * self._ADMIN_SERVICE_FEE_PER_YEAR / self._get_days_this_year_for_fee(date), 2)
                misc_fees = management_fee_list.array[-1] + custodian_fee_list.array[-1] + administrative_fee_list.array[-1]
            else:
                misc_fees = 0

            # 应收银行存款利息
            deposit_interest = round(other_assets_list.iat[-1] * self._DEPOSIT_INTEREST_PER_YEAR / self._DAYS_PER_YEAR_FOR_INTEREST, 2)
            deposit_interest_list.loc[date] = deposit_interest

            other_assets += (deposit_interest - misc_fees)
            other_assets_list.loc[date] = other_assets

            # 获取持仓中当日公募、私募基金的MV
            if fund_mv is not None:
                try:
                    today_fund_mv = fund_mv.loc[date]
                except KeyError:
                	today_fund_mv = 0
            else:
                today_fund_mv = 0
            today_fund_mv_list.loc[date] = today_fund_mv

            if hedge_fund_mv is not None:
            	try:
                	today_hedge_mv = hedge_fund_mv.loc[date]
            	except KeyError:
                	today_hedge_mv = 0
            else:
                today_hedge_mv = 0
            today_hedge_mv_list.loc[date] = today_hedge_mv

            # 计算净资产
            today_net_assets = today_fund_mv + today_hedge_mv + other_assets
            net_assets_list.loc[date] = today_net_assets

            if self._fund_pos is not None:
            	try:
                	fund_pos_info = pd.concat([self._fund_pos.loc[date, :].rename('share'), self._fund_nav.loc[date, :].rename('nav')], axis=1)
                	fund_pos_info = fund_pos_info[fund_pos_info.share.notna()]
                	fund_pos_info['asset_type'] = HoldingAssetType.MUTUAL
            	except KeyError:
                	fund_pos_info = None
            else:
                fund_pos_info = None

            if self._hedge_pos is not None:
            	try:
                	hedge_pos_info = pd.concat([self._hedge_pos.loc[date, :].rename('share'), self._hedge_nav.loc[date, :].rename('nav')], axis=1)
                	hedge_pos_info = hedge_pos_info[hedge_pos_info.share.notna()]
                	hedge_pos_info['asset_type'] = HoldingAssetType.HEDGE
            	except KeyError:
                	hedge_pos_info = None
            else:
            	hedge_pos_info = None

            if fund_pos_info is not None or hedge_pos_info is not None:
                position = pd.concat([fund_pos_info, hedge_pos_info], axis=0).rename_axis(index='fund_id').reset_index()
                position = position[position.share != 0]
                position['mv'] = position.share * position.nav
                positions_list.loc[date] = json.dumps(position.to_dict(orient='records'))

            # 计算修正净资产
            try:
                errors_to_be_fixed = round(self._manually.at[date, 'amount'], 2)
            except KeyError:
                errors_to_be_fixed = 0
            today_net_assets_fixed = today_net_assets + errors_to_be_fixed
            net_assets_fixed_list.loc[date] = today_net_assets_fixed

            # 如果今日有投资人申购fof 记录下来
            if not math.isclose(share_increased, 0):
                shares_list.loc[date] = share_increased
            # 计算fof的nav
            if shares_list.sum() != 0:
                fof_nav = today_net_assets_fixed / shares_list.sum()
            else:
                fof_nav = 1
            fof_nav_list.loc[date] = round(fof_nav, 4)
        # 汇总所有信息
        if debug_mode:
            total_info = pd.concat([shares_list, other_assets_list, fof_nav_list, today_fund_mv_list, today_hedge_mv_list, net_assets_list, net_assets_fixed_list, deposit_interest_list, positions_list], axis=1).sort_index()
            print(total_info)
        self._fof_nav = pd.concat([fof_nav_list, net_assets_fixed_list, shares_list.cumsum(), deposit_interest_list, management_fee_list, custodian_fee_list, administrative_fee_list], axis=1).sort_index().rename_axis('datetime').reset_index()
        self._fof_nav['share'] = self._fof_nav.share.ffill()
        self._fof_nav = self._fof_nav[self._fof_nav.datetime >= self._ESTABLISHED_DATE]
        self._fof_nav['fof_id'] = fof_id
        self._fof_nav['manager_id'] = manager_id
        # TODO: 暂时先直接用 nav 给 acc_net_value 和 adjusted_nav 赋值
        self._fof_nav['acc_net_value'] = self._fof_nav.nav
        self._fof_nav['adjusted_nav'] = self._fof_nav.nav
        self._fof_nav['ret'] = self._fof_nav.adjusted_nav / self._fof_nav.adjusted_nav.array[0] - 1

        self._fof_position = pd.concat([positions_list, other_assets_list.rename('other_assets')], axis=1).rename_axis('datetime').reset_index()
        self._fof_position = self._fof_position[self._fof_position.position.notna()]
        self._fof_position['fof_id'] = fof_id
        self._fof_position['manager_id'] = manager_id
        self._fof_position['deposit_in_bank'] = None

        self._fof_investor_pos = pd.concat(investor_pos_list).rename(columns={'share_changed': 'shares'}).reset_index(drop=True)
        self._fof_investor_pos = self._fof_investor_pos.groupby(by=['fof_id', 'investor_id'], sort=False).sum().reset_index()
        self._fof_investor_pos['datetime'] = date
        self._fof_investor_pos['manager_id'] = manager_id

        self._total_net_assets = net_assets_list.array[-1]
        self._total_shares = shares_list.sum()

        if self._hedge_pos is not None:
            asset_type = pd.Series(HoldingAssetType.HEDGE, index=self._hedge_pos.columns, name='asset_type')
        else:
            asset_type = None
        if self._fund_pos is not None:
            if asset_type is not None:
                asset_type = asset_type.append(pd.Series(HoldingAssetType.MUTUAL, index=self._fund_pos.columns, name='asset_type'))
            else:
                asset_type = pd.Series(HoldingAssetType.MUTUAL, index=self._fund_pos.columns, name='asset_type')
            if self._hedge_pos is not None:
                all_pos = self._hedge_pos.iloc[-1, :].append(self._fund_pos.iloc[-1, :]).rename('total_shares')
            else:
                all_pos = self._fund_pos.iloc[-1, :].rename('total_shares')
        else:
            if self._hedge_pos is not None:
                all_pos = self._hedge_pos.iloc[-1, :].rename('total_shares')
            else:
                all_pos = None
        if all_pos is not None and self._all_latest_nav is not None:
            latest_mv = all_pos * self._all_latest_nav
            dividend = self._asset_allocation.loc[self._asset_allocation.event_type.isin([FOFTradeStatus.DIVIDEND_CASH, FOFTradeStatus.DEDUCT_REWARD_AND_DIVIDEND_CASH]), :].pivot(index='datetime', columns='fund_id', values='amount').sum()
            redemptions = self._asset_allocation.loc[self._asset_allocation.event_type == FOFTradeStatus.REDEEM, :].pivot(index='datetime', columns='fund_id', values='share').sum()
            total_ret = latest_mv.add(dividend, fill_value=0).add(redemptions, fill_value=0).sub(self._total_cost)
            total_rr = total_ret / self._total_cost
        else:
            latest_mv = None
            total_ret = None
            total_rr = None

        fof_position_details_list = [self._latest_nav_date.rename('datetime') if self._latest_nav_date is not None else pd.Series(name='datetime'),
                                     asset_type if asset_type is not None else pd.Series(name='asset_type'),
                                     all_pos if all_pos is not None else pd.Series(name='total_shares'),
                                     total_ret.rename('total_ret') if total_ret is not None else pd.Series(name='total_ret'),
                                     total_rr.rename('total_rr') if total_rr is not None else pd.Series(name='total_rr'),
                                     self._total_cost.rename('total_cost') if self._total_cost is not None else pd.Series(name='total_cost'),
                                     self._all_latest_nav.rename('nav') if self._all_latest_nav is not None else pd.Series(name='nav'),
                                     self._all_latest_acc_nav.rename('acc_nav') if self._all_latest_acc_nav is not None else pd.Series(name='acc_nav'),
                                     self._hedge_latest_v_nav.rename('v_nav') if self._hedge_latest_v_nav is not None else pd.Series(name='v_nav'),
                                     latest_mv.rename('latest_mv') if latest_mv is not None else pd.Series(name='latest_mv')]
        self._fof_position_details = self._water_line_and_confirmed_nav.join(fof_position_details_list, how='outer')
        self._fof_position_details = self._fof_position_details.rename_axis(index='fund_id').reset_index()
        self._fof_position_details['fof_id'] = fof_id
        self._fof_position_details['manager_id'] = manager_id

        if dump_to_db:
            self.dump_fof_nav_and_pos_to_db(manager_id, fof_id, debug_mode)
        else:
            print(self._fof_nav)

    def dump_fof_nav_and_pos_to_db(self, manager_id: str, fof_id: str, debug_mode=False) -> bool:
        ret = False
        if self._fof_nav is not None and not self._fof_nav.empty:
            renamed_fof_nav = self._fof_nav.rename(columns={'net_asset_fixed': 'mv', 'share': 'volume'})
            now_df = DerivedDataApi().get_fof_nav_calc(manager_id, [fof_id])
            if now_df is not None:
                now_df = now_df.drop(columns=['update_time', 'create_time', 'is_deleted']).astype(renamed_fof_nav.dtypes.to_dict())
                # merge on all columns
                df = renamed_fof_nav.round(6).merge(now_df.round(6), how='left', indicator=True, validate='one_to_one')
                df = df[df._merge == 'left_only'].drop(columns=['_merge'])
            else:
                df = renamed_fof_nav
            if debug_mode:
                print(df)
            if not df.empty:
                DerivedDataApi().delete_fof_nav_calc(manager_id=manager_id, fof_id=fof_id, date_list=df[(df.manager_id == manager_id) & (df.fof_id == fof_id)].datetime.to_list())
                df.to_sql(FOFNavCalc.__table__.name, DerivedDatabaseConnector().get_engine(), index=False, if_exists='append')
                # self._wechat_bot.send_fof_nav_update(df)
                ret = True
            fof_nav = self._fof_nav.set_index('datetime').sort_index()
            fof_nav = fof_nav.nav
            nav = fof_nav.array[-1]
            if self._fof_scale is not None and self._fof_redemp is not None:
                mv = (self._fof_scale.share_changed.sum() - self._fof_redemp.share_changed.sum()) * nav
            else:
                mv = np.nan
            total_ret = fof_nav.array[-1] / fof_nav.array[0] - 1
            res_status = Calculator.get_stat_result(fof_nav.index, fof_nav.array)
            print('[dump_fof_nav_and_pos_to_db] dump nav done')
        else:
            res_status = None
            print('[dump_fof_nav_and_pos_to_db] no nav, should calc it first')

        if self._fof_position is not None:
            now_df = DerivedDataApi().get_fof_position(manager_id, [fof_id])
            if now_df is not None:
                now_df = now_df.drop(columns=['update_time', 'create_time', 'is_deleted']).astype(self._fof_position.dtypes.to_dict())
                # merge on all columns
                df = self._fof_position.round(6).merge(now_df.round(6), how='left', indicator=True, validate='one_to_one')
                df = df[df._merge == 'left_only'].drop(columns=['_merge'])
            else:
                df = self._fof_position
            if debug_mode:
                print(df)
            if not df.empty:
                DerivedDataApi().delete_fof_position(manager_id=manager_id, fof_id=fof_id, date_list=df[(df.manager_id == manager_id) & (df.fof_id == fof_id)].datetime.to_list())
                df.to_sql(FOFPosition.__table__.name, DerivedDatabaseConnector().get_engine(), index=False, if_exists='append')
            print('[dump_fof_nav_and_pos_to_db] dump position done')
        else:
            print('[dump_fof_nav_and_pos_to_db] no position, should calc it first')

        if self._fof_position_details is not None:
            now_df = DerivedDataApi().get_fof_position_detail(manager_id, [fof_id])
            if now_df is not None:
                now_df = now_df.drop(columns=['update_time', 'create_time', 'is_deleted']).astype(self._fof_position_details.dtypes.to_dict())
                # merge on all columns
                df = self._fof_position_details.round(4).merge(now_df.round(4), how='left', indicator=True, validate='one_to_one')
                df = df[df._merge == 'left_only'].drop(columns=['_merge'])
            else:
                df = self._fof_position_details
            if debug_mode:
                print(df)
            if not df.empty:
                DerivedDataApi().delete_fof_position_detail(manager_id=manager_id, fof_id_to_delete=fof_id, fund_id_list=df[(df.manager_id == manager_id) & (df.fof_id == fof_id)].fund_id.to_list())
                df.to_sql(FOFPositionDetail.__table__.name, DerivedDatabaseConnector().get_engine(), index=False, if_exists='append')
            print('[dump_fof_nav_and_pos_to_db] dump position detail done')
        else:
            print('[dump_fof_nav_and_pos_to_db] no position detail, should calc it first')

        investor_return_df = FOFDataManagerLite().get_investor_return(manager_id=manager_id, fof_id=fof_id)
        if investor_return_df is not None:
            investor_return_df = investor_return_df.drop(columns=['total_rr']).rename(columns={'latest_mv': 'mv'})
            investor_return_df['manager_id'] = manager_id
            now_df = FOFDataManagerLite().get_fof_investor_position(manager_id, [fof_id])
            if now_df is not None:
                now_df = now_df.drop(columns=['update_time', 'create_time', 'is_deleted'])
                now_df = now_df.astype(investor_return_df.dtypes.to_dict())
                # merge on all columns
                df = investor_return_df.reset_index().round(4).merge(now_df.round(4), how='left', indicator=True, validate='one_to_one')
                df = df[df._merge == 'left_only'].drop(columns=['_merge'])
            else:
                df = investor_return_df
            if debug_mode:
                print(df)
            if not df.empty:
                BasicDataApi().delete_fof_investor_position(manager_id=manager_id, fof_id_to_delete=fof_id, investor_id_list=df[(df.manager_id == manager_id) & (df.fof_id == fof_id)].investor_id.to_list())
                df.to_sql(FOFInvestorPosition.__table__.name, BasicDatabaseConnector().get_engine(), index=False, if_exists='append')
            print('[dump_fof_nav_and_pos_to_db] dump investor position done')

            investor_data = investor_return_df[['fof_id', 'amount', 'manager_id']]
            now_df = FOFDataManagerLite().get_fof_investor_data(manager_id, [fof_id])
            if now_df is not None:
                now_df = now_df.drop(columns=['update_time', 'create_time', 'is_deleted'])
                # merge on all columns
                df = investor_data.rename(columns={'amount': 'total_investment'}).reset_index().round(4).merge(now_df.round(4), how='left', indicator=True, validate='one_to_one')
                df = df[df._merge == 'left_only'].drop(columns=['_merge'])
            else:
                df = investor_data
            if debug_mode:
                print(df)
            if not df.empty:
                DerivedDataApi().delete_fof_investor_data(manager_id=manager_id, fof_id_to_delete=fof_id, investor_id_list=df[(df.manager_id == manager_id) & (df.fof_id == fof_id)].investor_id.to_list())
                df.to_sql(FOFInvestorData.__table__.name, DerivedDatabaseConnector().get_engine(), index=False, if_exists='append')
            print('[dump_fof_nav_and_pos_to_db] dump investor data done')
        else:
            print('[dump_fof_nav_and_pos_to_db] get investor position failed')

        investor_summary_df = FOFDataManagerLite().get_investor_pos_summary(manager_id, fof_id)
        if investor_summary_df is not None:
            now_df = FOFDataManagerLite().get_fof_investor_position_summary(manager_id)
            if now_df is not None:
                now_df = now_df.drop(columns=['update_time', 'create_time', 'is_deleted']).astype(investor_summary_df.dtypes.to_dict())
                # merge on all columns
                df = investor_summary_df.round(6).merge(now_df.round(6), how='left', indicator=True, validate='one_to_one')
                df = df[df._merge == 'left_only'].drop(columns=['_merge'])
            else:
                df = investor_summary_df
            if debug_mode:
                print(df)
            if not df.empty:
                for investor_id in df.investor_id.unique():
                    BasicDataApi().delete_fof_investor_position_summary(manager_id=manager_id, investor_id=investor_id, date_list=df[(df.manager_id == manager_id) & (df.investor_id == investor_id)].datetime.to_list())
                df.to_sql(FOFInvestorPositionSummary.__table__.name, BasicDatabaseConnector().get_engine(), index=False, if_exists='append')
            print('[dump_fof_nav_and_pos_to_db] dump investor summary done')
        else:
            print('[dump_fof_nav_and_pos_to_db] get investor summary failed')

        # ret = True
        # if ret:
        #     if res_status is not None:
        #         try:
        #             fof_data = {
        #                 'start_date': res_status.start_date.isoformat(),
        #                 'days': (fof_nav.index.array[-1] - res_status.start_date).days,
        #                 'mv': mv,
        #                 'nav': round(nav, 4),
        #                 'total_ret': f'{round(total_ret * 100, 2)}%',
        #                 'sharpe': round(res_status.sharpe, 6),
        #                 'annualized_ret': f'{round(res_status.annualized_ret * 100, 2)}%',
        #                 'mdd': f'{round(res_status.mdd * 100, 2)}%',
        #                 'annualized_vol': round(res_status.annualized_vol, 6),
        #             }
        #             self._wechat_bot.send_fof_info(fof_id, fof_nav.index.array[-1], fof_data)
        #         except Exception as e:
        #             traceback.print_exc()
        #             self._wechat_bot.send_fof_info_failed(fof_id, e)

        # 把 is_calculating 的标记置为false
        Session = sessionmaker(BasicDatabaseConnector().get_engine())
        db_session = Session()
        fof_info_to_set = db_session.query(FOFInfo).filter((FOFInfo.manager_id == manager_id) & (FOFInfo.fof_id == fof_id)).one_or_none()
        fof_info_to_set.is_calculating = False
        db_session.commit()
        db_session.close()

    def calc_pure_fof_data(self, manager_id: str, fof_id: str, debug_mode=False):
        # 获取FOF份额变化信息
        fof_scale = DerivedDataApi().get_hedge_fund_investor_pur_redemp(manager_id, [fof_id])
        # 客户认购/申购记录
        self._fof_scale = fof_scale[fof_scale.event_type.isin([FOFTradeStatus.SUBSCRIBE, FOFTradeStatus.PURCHASE])].set_index('datetime')
        # 客户赎回记录
        self._fof_redemp = fof_scale[fof_scale.event_type.isin([FOFTradeStatus.REDEEM, ])].set_index('datetime')
        # fof_nav数据优先级更大
        fof_nav = FOFDataManagerLite.get_fof_nav(manager_id=manager_id, fof_id=fof_id)
        fof_nav_public = FOFDataManagerLite.get_fof_nav_public(manager_id=manager_id, fof_id=fof_id)
        if fof_nav is None:
            self._fof_nav = fof_nav_public
        else:
            if fof_nav_public is None:
                self._fof_nav = fof_nav
            else:
                self._fof_nav = fof_nav.combine_first(fof_nav_public)
        self._fof_nav['interest'] = np.nan
        self._fof_nav['management_fee'] = np.nan
        self._fof_nav['custodian_fee'] = np.nan
        self._fof_nav['administrative_fee'] = np.nan
        self.dump_fof_nav_and_pos_to_db(manager_id, fof_id, debug_mode)

    def _gather_asset_info_of_fof(self, manager_id, fof_id, fund_list: List[str], v_nav: pd.DataFrame):
        fof_aa = FOFDataManagerLite.get_fof_asset_allocation(manager_id, [fof_id])
        hedge_nav = FOFDataManagerLite.get_hedge_fund_nav(fund_list)
        trading_day = BasicDataApi().get_trading_day_list(start_date=hedge_nav.datetime.min(), end_date=hedge_nav.datetime.max())
        hedge_info = FOFDataManagerLite.get_hedge_fund_info(fund_list).set_index('fund_id')
        for fund_id in fund_list:
            try:
                fund_fof_aa = fof_aa.loc[fof_aa.fund_id == fund_id, :]
                pur_sub_aa = fund_fof_aa[fund_fof_aa.event_type.isin([FOFTradeStatus.PURCHASE, FOFTradeStatus.SUBSCRIBE])]
                if pur_sub_aa.empty:
                    continue
                redempt_aa = fund_fof_aa[fund_fof_aa.event_type.isin([FOFTradeStatus.REDEEM, ])]
                aa_insentive_info = fund_fof_aa[fund_fof_aa.event_type.isin([FOFTradeStatus.DEDUCT_REWARD, FOFTradeStatus.DEDUCT_REWARD_AND_DIVIDEND_CASH])]
                aa_dividend_reinvestment = fund_fof_aa[fund_fof_aa.event_type.isin([FOFTradeStatus.DIVIDEND_VOLUME, FOFTradeStatus.DEDUCT_REWARD_AND_DIVIDEND_VOLUME])]
                fund_nav = hedge_nav[hedge_nav.fund_id == fund_id]
                # TODO 这里最好应该用复权净值
                fund_auv = fund_nav.set_index('datetime')['acc_unit_value']
                ret_date_with_last_pub = {}
                if fund_auv.size > 2:
                    ret_date_with_last_pub['date'] = fund_auv.index.array[-2]
                    ret_date_with_last_pub['rr'] = f'{round(((fund_auv.array[-1] / fund_auv.array[-2]) - 1) * 100, 2)}%'

                fund_auv = fund_auv.reindex(trading_day[trading_day.datetime.between(fund_auv.index.min(), fund_auv.index.max())].datetime).ffill()
                res_status = Calculator.get_stat_result(fund_auv.index, fund_auv.array)
                total_ret = fund_auv.array[-1] / fund_auv.array[0] - 1
                fund_data = {
                    'start_date': res_status.start_date.isoformat(),
                    'days': (fund_auv.index.array[-1] - res_status.start_date).days,
                    'nav': round(fund_nav.net_asset_value.array[-1], 4),
                    'total_ret': f'{round(total_ret * 100, 2)}%',
                    'sharpe': round(res_status.sharpe, 6),
                    'annualized_ret': f'{round(res_status.annualized_ret * 100, 2)}%',
                    'mdd': f'{round(res_status.mdd * 100, 2)}%',
                    'annualized_vol': round(res_status.annualized_vol, 6),
                }

                latest_nav_date = fund_nav.loc[:, 'datetime'].iat[-1]
                Session = sessionmaker(BasicDatabaseConnector().get_engine())
                db_session = Session()
                fof_info_to_set = db_session.query(HedgeFundInfo).filter(HedgeFundInfo.fund_id == fund_id).one_or_none()
                fof_info_to_set.latest_cal_date = latest_nav_date
                fof_info_to_set.net_asset_value = float(fund_nav.net_asset_value.array[-1]) if not pd.isnull(fund_nav.net_asset_value.array[-1]) else None
                fof_info_to_set.acc_unit_value = float(fund_nav.acc_unit_value.array[-1]) if not pd.isnull(fund_nav.acc_unit_value.array[-1]) else None
                fof_info_to_set.adjusted_net_value = float(fund_nav.adjusted_net_value.array[-1]) if not pd.isnull(fund_nav.adjusted_net_value.array[-1]) else None
                fof_info_to_set.mdd = float(res_status.mdd) if not pd.isnull(res_status.mdd) else None
                fof_info_to_set.ret = float(total_ret) if not pd.isnull(total_ret) else None
                fof_info_to_set.ann_ret = float(res_status.annualized_ret) if not pd.isnull(res_status.annualized_ret) else None
                db_session.commit()
                db_session.close()

                ret_data_with_last_date = {}
                last_date: datetime.date = fund_auv.index.array[-1]
                while last_date == fund_auv.index.array[-1] or last_date.isoweekday() != 5:
                    last_date -= datetime.timedelta(days=1)
                last_date_data = fund_auv[fund_auv.index <= last_date]
                if not last_date_data.empty:
                    last_date_data = last_date_data.iloc[[-1]]
                    ret_data_with_last_date['date'] = last_date_data.index.array[0]
                    ret_data_with_last_date['rr'] = f'{round(((fund_auv.array[-1] / last_date_data.array[0]) - 1) * 100, 2)}%'

                fund_auv = fund_auv[fund_auv.index >= pur_sub_aa.sort_values(by='confirmed_date').confirmed_date.array[0]]
                if not fund_auv.empty:
                    res_status = Calculator.get_stat_result(fund_auv.index, fund_auv.array)
                    mv = (pur_sub_aa.share.sum() - aa_insentive_info.share.sum() + aa_dividend_reinvestment.share.sum()) * fund_nav.net_asset_value.array[-1]
                    real_mv = mv - redempt_aa.share.sum() * fund_nav.net_asset_value.array[-1]
                    total_cost = pur_sub_aa.amount.sum()
                    v_net_value = fund_nav.v_net_value.array[-1]
                    if not pd.isnull(v_net_value):
                        v_net_value = round(float(v_net_value), 4)
                    else:
                        try:
                            v_net_value = f'{round(v_nav[fund_id].iat[-1], 4)}(计算值)'
                        except KeyError:
                            v_net_value = '/'
                    if fund_nav.datetime.array[-1] > pur_sub_aa.confirmed_date.array[-1]:
                        the_xirr = f'{round(xirr(pur_sub_aa.amount.to_list() + [-mv], pur_sub_aa.confirmed_date.to_list() + [fund_nav.datetime.array[-1]]) * 100, 2)}%'
                    else:
                        the_xirr = np.nan
                    holding_data = {
                        'start_date': res_status.start_date.isoformat(),
                        'days': (fund_auv.index.array[-1] - res_status.start_date).days,
                        'mv': real_mv,
                        'total_ret': f'{round((mv / total_cost - 1) * 100, 2)}%',
                        'v_nav': v_net_value,
                        'avg_cost': round(total_cost / (pur_sub_aa.share.sum() - aa_insentive_info.share.sum()), 4),
                        'sharpe': round(res_status.sharpe, 6),
                        'annualized_ret': the_xirr,
                        'mdd': f'{round(res_status.mdd * 100, 2)}%',
                        'annualized_vol': round(res_status.annualized_vol, 6),
                    }
                    self._wechat_bot.send_hedge_fund_info(fof_id, fund_id, hedge_info.at[fund_id, 'brief_name'], latest_nav_date, fund_data, holding_data, ret_data_with_last_date, ret_date_with_last_pub)
            except Exception as e:
                traceback.print_exc()
                self._wechat_bot.send_hedge_fund_info_failed(fof_id, fund_id, e)

    def pull_hedge_fund_nav(self, manager_id: str, fof_id: str):
        import os

        try:
            email_data_dir = os.environ['SURFING_EMAIL_DATA_DIR']
            user_name = os.environ['SURFING_EMAIL_USER_NAME']
            password = os.environ['SURFING_EMAIL_PASSWORD']
        except KeyError as e:
            print(f'[pull_hedge_fund_nav] can not found enough params in env (e){e}')
            return False

        hf_nav_r = HedgeFundNAVReader(email_data_dir, user_name, password)
        nav_df: Optional[pd.DataFrame] = hf_nav_r.read_navs_and_dump_to_db()
        if nav_df is not None:
            fund_list = list(nav_df.index.unique())
            adj_nav = FOFDataManagerLite._calc_adjusted_net_value(fund_list)
            adj_nav = adj_nav[adj_nav.ta_factor.notna()]
            if not adj_nav.empty:
                print(adj_nav)
                Session = sessionmaker(BasicDatabaseConnector().get_engine())
                db_session = Session()
                for row in adj_nav.itertuples():
                    hedge_fund_nav_to_set = db_session.query(HedgeFundNAV).filter(HedgeFundNAV.fund_id == row.Index, HedgeFundNAV.datetime == row.datetime).one_or_none()
                    hedge_fund_nav_to_set.ta_factor = row.ta_factor
                    hedge_fund_nav_to_set.adjusted_net_value = row.adj_nav
                    db_session.commit()
                db_session.close()
            v_nav = FOFDataManagerLite._calc_virtual_net_value(manager_id, fof_id, fund_list)
            self._gather_asset_info_of_fof(manager_id, fof_id, fund_list, v_nav)
        return True

    def calc_all(self, manager_id: str, fof_id: str):
        if not self.pull_hedge_fund_nav(manager_id, fof_id):
            return
        try:
            self.calc_fof_nav(manager_id, fof_id)
        except Exception as e:
            traceback.print_exc()
            self._wechat_bot.send_fof_nav_update_failed(fof_id, f'calc fof nav failed (e){e}')

    @staticmethod
    def _concat_assets_price(main_asset: pd.DataFrame, secondary_asset: pd.Series) -> pd.DataFrame:
        # FIXME 理论上任意资产在任意交易日应该都是有price的 所以这里的判断应该是可以确保之后可以将N种资产的price接起来
        secondary_asset = secondary_asset[secondary_asset.index <= main_asset.datetime.array[0]]
        # 将price对齐
        secondary_asset /= (secondary_asset.array[-1] / main_asset.nav.array[0])
        # 最后一个数据是对齐用的 这里就不需要了
        return pd.concat([main_asset.set_index('datetime'), secondary_asset.iloc[:-1].to_frame('nav')], verify_integrity=True).sort_index().reset_index()

    # 以下是一些获取数据的接口
    @staticmethod
    def get_fof_info(manager_id: str, fof_id: str):
        fof_info = BasicDataApi().get_fof_info(manager_id, [fof_id])
        if fof_id is None:
            return
        return fof_info.sort_values(by=['manager_id', 'fof_id', 'datetime']).iloc[-1]

    @staticmethod
    def get_fof_investor_position(manager_id: str, fof_id: Tuple[str] = ()):
        df = BasicDataApi().get_fof_investor_position(manager_id, fof_id)
        if df is None:
            return
        return df.sort_values(by=['manager_id', 'fof_id', 'investor_id', 'datetime']).drop_duplicates(subset=['manager_id', 'fof_id', 'investor_id'], keep='last')

    @staticmethod
    def get_fof_investor_position_summary(manager_id: str, investor_id: Tuple[str] = ()):
        return BasicDataApi().get_fof_investor_position_summary(manager_id, investor_id)

    @staticmethod
    def get_fof_investor_data(manager_id: str, fof_id: Tuple[str] = ()):
        return DerivedDataApi().get_fof_investor_data(manager_id, fof_id)

    @staticmethod
    def get_fof_asset_allocation(manager_id: str, fof_id: Tuple[str] = ()):
        return BasicDataApi().get_fof_asset_allocation(manager_id, fof_id)

    @staticmethod
    def get_fof_scale_alteration(fof_id: Tuple[str] = ()):
        return BasicDataApi().get_fof_scale_alteration(fof_id)

    @staticmethod
    def get_fof_estimate_fee(fof_id: Tuple[str] = ()):
        return BasicDataApi().get_fof_estimate_fee(fof_id)

    @staticmethod
    def get_fof_estimate_interest(manager_id: str, fof_id: Tuple[str] = ()):
        return BasicDataApi().get_fof_estimate_interest(manager_id, fof_id)

    @staticmethod
    def get_fof_transit_money(fof_id: Tuple[str] = ()):
        return BasicDataApi().get_fof_transit_money(fof_id)

    @staticmethod
    def get_fof_account_statement(manager_id: str, fof_id: Tuple[str] = ()):
        return BasicDataApi().get_fof_account_statement(manager_id, fof_id)

    @staticmethod
    def get_fof_nav(manager_id: str, fof_id: str, *, ref_index_id: str = '', ref_fund_id: str = '') -> Optional[pd.DataFrame]:
        fof_nav = DerivedDataApi().get_fof_nav(manager_id, [fof_id])
        if fof_nav is None:
            return
        fof_nav = fof_nav.drop(columns=['update_time', 'create_time', 'is_deleted'])
        if ref_index_id:
            index_price = BasicDataApi().get_index_price(index_list=[ref_index_id])
            if index_price is None or index_price.empty:
                print(f'[get_fof_nav] get price of index {ref_index_id} failed (fof_id){fof_id}')
                return fof_nav
            return FOFDataManagerLite._concat_assets_price(fof_nav, index_price.drop(columns=['_update_time', 'index_id']).set_index('datetime')['close'])
        elif ref_fund_id:
            fund_nav = BasicDataApi().get_fund_nav_with_date(fund_list=[ref_fund_id])
            if fund_nav is None or fund_nav.empty:
                print(f'[get_fof_nav] get nav of fund {ref_fund_id} failed (fof_id){fof_id}')
                return fof_nav
            return FOFDataManagerLite._concat_assets_price(fof_nav, fund_nav.drop(columns='fund_id').set_index('datetime')['adjusted_net_value'])
        else:
            return fof_nav

    @staticmethod
    def get_fof_nav_public(manager_id: str, fof_id: str) -> Optional[pd.DataFrame]:
        fof_nav = DerivedDataApi().get_fof_nav_public(manager_id, [fof_id])
        if fof_nav is None:
            return
        return fof_nav.drop(columns=['update_time', 'create_time', 'is_deleted'])

    @staticmethod
    def get_hedge_fund_info(fund_id: Tuple[str] = ()):
        return BasicDataApi().get_hedge_fund_info(fund_id)

    @staticmethod
    def get_hedge_fund_nav(fund_id: Tuple[str] = ()):
        df = BasicDataApi().get_hedge_fund_nav(fund_id)
        if df is None:
            return
        return df.sort_values(by=['fund_id', 'datetime', 'insert_time']).drop_duplicates(subset=['fund_id', 'datetime'], keep='last')

    @staticmethod
    def get_investor_pos_summary(manager_id: str, fof_id: str):
        fof_nav = DerivedDataApi().get_fof_nav_calc(manager_id, [fof_id])
        if fof_nav is None:
            return
        if fof_nav.empty:
            return
        fof_nav = fof_nav.pivot(index='datetime', columns='fof_id', values='nav')
        fof_scale_info = DerivedDataApi().get_hedge_fund_investor_pur_redemp(manager_id, [fof_id])
        if fof_scale_info is None:
            return

        investor_pos = {}
        for row in fof_scale_info.itertuples(index=False):
            if row.investor_id not in investor_pos:
                investor_pos[row.investor_id] = {
                    'amount': pd.DataFrame(0, index=fof_nav.index.unique(), columns=fof_scale_info[fof_scale_info.investor_id == row.investor_id].fof_id.unique()),
                    'left_amount': pd.DataFrame(0, index=fof_nav.index.unique(), columns=fof_scale_info[fof_scale_info.investor_id == row.investor_id].fof_id.unique()),
                    'share': pd.DataFrame(0, index=fof_nav.index.unique(), columns=fof_scale_info[fof_scale_info.investor_id == row.investor_id].fof_id.unique()),
                    'left_share': pd.DataFrame(0, index=fof_nav.index.unique(), columns=fof_scale_info[fof_scale_info.investor_id == row.investor_id].fof_id.unique()),
                }

            pos = investor_pos[row.investor_id]
            if row.event_type in (FOFTradeStatus.PURCHASE, FOFTradeStatus.SUBSCRIBE):
                assert not pd.isnull(row.share_changed), '!!!'
                pos['share'].loc[pos['share'].index >= row.datetime, row.fof_id] += row.share_changed
                pos['left_share'].loc[pos['left_share'].index >= row.datetime, row.fof_id] += row.share_changed
                pos['amount'].loc[pos['amount'].index >= row.datetime, row.fof_id] += row.purchase_amount
                pos['left_amount'].loc[pos['left_amount'].index >= row.datetime, row.fof_id] += row.purchase_amount
                if row.event_type == FOFTradeStatus.PURCHASE:
                    pos['amount'].loc[pos['amount'].index >= row.datetime, row.fof_id] += row.raising_interest
                    pos['left_amount'].loc[pos['left_amount'].index >= row.datetime, row.fof_id] += row.raising_interest
            elif row.event_type in (FOFTradeStatus.REDEEM, ):
                assert not pd.isnull(row.share_changed), '!!!'
                pos['left_share'].loc[pos['left_share'].index >= row.datetime, row.fof_id] += row.share_changed
                pos['left_amount'].loc[pos['left_amount'].index >= row.datetime, row.fof_id] -= row.redemp_confirmed_amount

        result_df_list = []
        for investor_id, pos in investor_pos.items():
            left_share = pos['left_share'].sort_index()
            mv = (left_share * fof_nav).sum(axis=1)

            share = pos['share'].sort_index()
            redemp = share - left_share
            real_total_mv = mv + (redemp * fof_nav).sum(axis=1)
            amount = pos['amount'].sort_index().sum(axis=1)
            left_amount = pos['left_amount'].sort_index().sum(axis=1)
            total_ret = real_total_mv - amount
            total_rr = total_ret / amount
            share_sum = share.sum(axis=1)
            left_share_sum = left_share.sum(axis=1)
            whole_df = pd.concat([mv.rename('mv'), amount.rename('amount'), left_amount.rename('left_amount'), share_sum.rename('shares'), left_share_sum.rename('left_shares'), total_ret.rename('total_ret'), total_rr.rename('total_rr')], axis=1)
            whole_df['investor_id'] = investor_id
            result_df_list.append(whole_df)
        df = pd.concat(result_df_list, axis=0).reset_index()
        df = df[df.amount != 0]
        df['manager_id'] = manager_id
        return df

    @staticmethod
    def get_investor_return(manager_id: str, fof_id: str, *, investor_id_list: Tuple[str] = (), start_date: Optional[datetime.date] = None, end_date: Optional[datetime.date] = None) -> Optional[pd.DataFrame]:
        '''计算投资者收益'''
        fof_nav = DerivedDataApi().get_fof_nav(manager_id, [fof_id])
        if fof_nav is None:
            return
        investor_pur_redemp = DerivedDataApi().get_hedge_fund_investor_pur_redemp(manager_id, [fof_id])
        if investor_pur_redemp is None:
            return

        fof_nav = fof_nav.set_index('datetime')
        if start_date:
            fof_nav = fof_nav[fof_nav.index >= start_date]
        if end_date:
            fof_nav = fof_nav[fof_nav.index <= end_date]
        if fof_nav.empty:
            return
        investor_mvs = defaultdict(list)
        for row in investor_pur_redemp.itertuples(index=False):
            if investor_id_list and row.investor_id not in investor_id_list:
                continue
            if row.event_type in (FOFTradeStatus.PURCHASE, FOFTradeStatus.SUBSCRIBE):
                if start_date is not None:
                    actual_start_date = max(row.applied_date, start_date)
                else:
                    actual_start_date = row.applied_date
                try:
                    init_mv = fof_nav.at[actual_start_date, 'nav'] * row.share_changed
                except KeyError:
                    init_mv = row.share_changed
                the_amount = row.purchase_amount
                if row.event_type == FOFTradeStatus.PURCHASE:
                    the_amount += row.raising_interest
                investor_mvs[row.investor_id].append({'trade_ids': [row.id], 'start_date': actual_start_date, 'amount': the_amount, 'left_amount': the_amount, 'share': row.share_changed, 'left_share': row.share_changed, 'init_mv': init_mv, 'water_line': row.acc_unit_value})
            elif row.event_type in (FOFTradeStatus.REDEEM, ):
                share_redemp = row.share_changed
                for one in investor_mvs[row.investor_id]:
                    if one['left_share'] >= share_redemp:
                        one['left_share'] += share_redemp
                        one['trade_ids'].append(row.id)
                        break
                    else:
                        share_redemp -= one['left_share']
                        one['left_share'] = 0
                        one['left_amount'] = 0
                        one['trade_ids'].append(row.id)

        investor_returns = {}
        latest_nav = fof_nav.nav.array[-1]
        for investor_id, datas in investor_mvs.items():
            datas = pd.DataFrame(datas)
            # TODO: hard code 0.2 and 4 and the second param should be acc nav
            # v_nav = FOFDataManagerLite._do_calc_v_net_value(latest_nav, datas.left_share, latest_nav, datas.water_line, 0.2, 4)
            # 这里确保单取的几个Series的顺序不会发生任何变化 这样直接运算才是OK的
            mv = latest_nav * datas.left_share
            latest_mv = mv.sum()
            total_mv = (latest_nav * datas.share).sum()
            total_share = datas.left_share.sum()
            avg_v_nav = latest_mv / total_share
            amount_sum = datas.amount.sum()
            if not math.isclose(amount_sum, 0):
                total_ret = total_mv - amount_sum
                total_rr = total_ret / amount_sum
            else:
                total_ret = np.nan
                total_rr = np.nan
            if not math.isclose(total_share, 0):
                avg_nav_cost = datas.left_amount.sum() / total_share
            else:
                avg_nav_cost = np.nan
            investor_returns[investor_id] = {
                'datetime': fof_nav.index.array[-1], 'fof_id': fof_id, 'v_nav': avg_v_nav, 'cost_nav': avg_nav_cost, 'total_ret': total_ret, 'total_rr': total_rr, 'amount': amount_sum, 'shares': total_share, 'latest_mv': latest_mv,
                'details': datas[['trade_ids', 'amount', 'left_share', 'water_line']].rename(columns={'left_share': 'share'}).join(mv.rename('mv')).to_json(orient='records')
            }
        return pd.DataFrame.from_dict(investor_returns, orient='index').rename_axis(index='investor_id')

    @staticmethod
    def calc_share_by_subscription_amount(manager_id: str, fof_id: str, amount: float, confirmed_date: datetime.date) -> Optional[float]:
        '''根据金额和日期计算申购fof产品的确认份额'''

        fof_info: Optional[pd.DataFrame] = FOFDataManagerLite.get_fof_info(manager_id, [fof_id])
        if fof_info is None:
            return
        fof_nav = DerivedDataApi().get_fof_nav_calc(manager_id, [fof_id])
        if fof_nav is None:
            return
        try:
            # 用申购金额除以确认日的净值以得到份额
            return amount / (1 + fof_info.subscription_fee) / fof_nav.loc[fof_nav.datetime == confirmed_date, 'nav'].array[-1]
        except KeyError:
            return

    @staticmethod
    def remove_hedge_nav_data(fund_id: str, start_date: str = '', end_date: str = ''):
        BasicDataApi().delete_hedge_fund_nav(fund_id_to_delete=fund_id, start_date=start_date, end_date=end_date)

    @staticmethod
    def upload_hedge_nav_data(datas: bytes, file_name: str, hedge_fund_id: str) -> bool:
        '''上传单个私募基金净值数据'''
        '''目前支持：私募排排网 朝阳永续'''

        if not datas:
            return True

        try:
            # 下边这个分支是从私募排排网上多只私募基金净值数据的文件中读取数据
            # if file_type == 'csv':
            #     hedge_fund_info = BasicDataApi().get_hedge_fund_info()
            #     if hedge_fund_info is None:
            #         return
            #     fund_name_map = hedge_fund_info.set_index('brief_name')['fund_id'].to_dict()
            #     fund_name_map['日期'] = 'datetime'
            #     df = pd.read_csv(io.BytesIO(datas), encoding='gbk')
            #     lacked_map = set(df.columns.array) - set(fund_name_map.keys())
            #     assert not lacked_map, f'lacked hedge fund name map {lacked_map}'
            #     df = df.rename(columns=fund_name_map).set_index('datetime').rename_axis(columns='fund_id')
            #     df = df.stack().to_frame('adjusted_net_value').reset_index()
            #     # validate = 'many_to_many'
            try:
                if '产品详情-历史净值' in file_name:
                    df = pd.read_excel(io.BytesIO(datas), usecols=['净值日期', '单位净值', '累计净值', '复权累计净值'], na_values='--')
                    df = df.rename(columns=HedgeFundNAVReader.COLUMNS_DICT)
                    df['fund_id'] = hedge_fund_id
                elif '业绩走势' in file_name:
                    df = pd.read_excel(io.BytesIO(datas), usecols=['净值日期', '净值(分红再投)'], na_values='--')
                    df = df.rename(columns=HedgeFundNAVReader.COLUMNS_DICT)
                    df['fund_id'] = hedge_fund_id
                else:
                    assert False
            except Exception:
                try:
                    try:
                        df = pd.read_excel(io.BytesIO(datas), na_values='--')
                    except Exception:
                        df = pd.read_csv(io.BytesIO(datas), na_values='--')
                except Exception:
                    print(f'[upload_hedge_nav_data] can not read data from this file (file name){file_name} (fund_id){hedge_fund_id}')
                    return False
                else:
                    df = df.rename(columns=HedgeFundNAVReader.COLUMNS_DICT)
                    df['fund_id'] = hedge_fund_id

            df = df[df.drop(columns=['fund_id', 'datetime']).notna().any(axis=1)]
            now_df = BasicDataApi().get_hedge_fund_nav([hedge_fund_id])
            if now_df is not None:
                now_df = now_df.drop(columns=['update_time', 'create_time', 'insert_time', 'is_deleted', 'calc_date']).astype({'net_asset_value': 'float64', 'acc_unit_value': 'float64', 'v_net_value': 'float64', 'adjusted_net_value': 'float64'})
                df = df.reindex(columns=now_df.columns).astype(now_df.dtypes.to_dict())
                df['datetime'] = pd.to_datetime(df.datetime, infer_datetime_format=True).dt.date
                # merge on all columns
                df = df.round(6).merge(now_df, how='left', indicator=True, validate='one_to_one')
                df = df[df._merge == 'left_only'].drop(columns=['_merge'])
            if not df.empty:
                df['insert_time'] = datetime.datetime.now()
                print(f'[upload_hedge_nav_data] try to insert data to db (df){df}')
                df.to_sql(HedgeFundNAV.__table__.name, BasicDatabaseConnector().get_engine(), index=False, if_exists='append')
            else:
                print(f'[upload_hedge_nav_data] empty df, nothing to do')
            return True
        except Exception as e:
            print(f'[upload_hedge_nav_data] failed, got exception {e} (file_name){file_name} (hedge_fund_id){hedge_fund_id}')
            return False

    @staticmethod
    def _do_backtest(fund_nav_ffilled, wgts):
        INITIAL_CASH = 10000000
        INIT_NAV = 1
        UNIT_TOTAL = INITIAL_CASH / INIT_NAV

        positions = []
        mvs = []
        navs = []
        # 初始市值
        mv = INITIAL_CASH
        for index, s in fund_nav_ffilled.iterrows():
            s = s[s.notna()]
            if positions:
                # 最新市值
                mv = (positions[-1][1] * s).sum()

            if not positions or (s.size != positions[-1][1].size):
                # 调仓
                new_wgts = wgts.loc[s.index]
                # 各标的目标权重
                new_wgts /= new_wgts.sum()
                # 新的各标的持仓份数
                shares = (mv * new_wgts) / s
                # shares = (mv / s.size) / s
                positions.append((index, shares))

            nav = mv / UNIT_TOTAL
            mvs.append(mv)
            navs.append(nav)
        return positions, mvs, navs

    @staticmethod
    def virtual_backtest(hedge_fund_ids: Dict[str, float], ref_fund_ids: Dict[str, str], start_date: datetime.date, end_date: Optional[datetime.date] = None, benchmark_ids: Tuple[str] = ()) -> Optional[Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, List[str]]]:
        '''
        对私募基金做虚拟回测

        Parameters
        ----------
        hedge_fund_ids : Dict[str, float]
            私募基金ID列表
        ref_fund_ids : Dict[str, str]
            ref基金ID列表
        start_date: datetime.date
            回测起始日期
        end_date: datetime.date
            回测终止日期
        benchmark_ids : Tuple[str]
            指数ID列表

        Returns
        -------
        Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, List[str]]
        '''

        DEFAULT_INCENTIVE_RATIO = 0.2
        DEFAULT_DECIMAL = 4

        try:
            if end_date is None:
                end_date = datetime.date.today()
            # 获取必要的私募基金信息
            fund_info = BasicDataApi().get_hedge_fund_info(list(hedge_fund_ids.keys()))
            if fund_info is None:
                return
            fund_info = fund_info.set_index('fund_id')

            # 统计一下需要替代的基金的ref ids
            funds_added = [ref for fund, ref in ref_fund_ids.items() if fund in hedge_fund_ids.keys()]
            # 获取私募基金净值数据
            fund_nav = FOFDataManagerLite.get_hedge_fund_nav(list(hedge_fund_ids.keys()) + funds_added)
            if fund_nav is None:
                return

            # 这里首选复权净值
            fund_nav = fund_nav[(fund_nav.fund_id != 'SR9762') | (fund_nav.datetime >= pd.to_datetime('2020-07-01', infer_datetime_format=True).date())]
            adj_nav = fund_nav.pivot(index='datetime', columns='fund_id', values='adjusted_net_value')
            # 处理ref fund
            for fund, ref in ref_fund_ids.items():
                org_nav = adj_nav[fund]
                org_nav = org_nav.ffill().dropna().sort_index()

                # 取出来ref nav在org fund成立之前的净值
                ref_nav = adj_nav.sort_index().loc[adj_nav.index <= org_nav.index.array[0], ref].ffill()
                org_nav *= ref_nav.array[-1]
                adj_nav[fund] = pd.concat([ref_nav.iloc[:-1], org_nav])
            # 最后再删掉所有的ref fund列
            adj_nav = adj_nav.loc[:, set(adj_nav.columns.array) - set(ref_fund_ids.values())]

            # 去掉全是nan的列
            valid_adj_nav = adj_nav.loc[:, adj_nav.notna().any(axis=0)]
            # 计算缺少的列
            adj_nav_lacked = set(adj_nav.columns.array) - set(valid_adj_nav.columns.array)
            if adj_nav_lacked:
                # TODO 如果某只基金完全没有复权净值 需要用累计净值来计算
                # FIXME 这里不能直接用数据库里存的虚拟净值 因为这个是邮件里发过来的单位净值虚拟后净值 而上边算出来的是复权净值虚拟后净值
                acc_nav = fund_nav[fund_nav.fund_id.isin(adj_nav_lacked)].pivot(index='datetime', columns='fund_id', values='acc_unit_value')
                adj_nav = adj_nav.drop(columns=adj_nav_lacked).join(acc_nav, how='outer')
            fund_info = fund_info.reindex(adj_nav.columns)
            lacked_funds = list(set(hedge_fund_ids.keys()) - set(adj_nav.columns.array))
            for one in lacked_funds:
                del hedge_fund_ids[one]

            # 计算虚拟净值
            FOFDataManagerLite._adj_nav = adj_nav
            fund_nav = FOFDataManagerLite._do_calc_v_net_value_by_nav(adj_nav, adj_nav, adj_nav.loc[adj_nav.index >= start_date, :].bfill().iloc[0, :], fund_info.incentive_fee_ratio.fillna(DEFAULT_INCENTIVE_RATIO), fund_info.v_nav_decimals.fillna(DEFAULT_DECIMAL))
            # water_line = pd.Series({'SGM473': 1, 'SGM992': 1, 'SJE335': 1, 'SLC213': 1, 'SNG191': 1, 'SNH765': 1, 'SR9762': 1.1146})
            # fund_nav = FOFDataManagerLite._do_calc_v_net_value_by_nav(adj_nav, adj_nav, water_line, fund_info.incentive_fee_ratio.fillna(DEFAULT_INCENTIVE_RATIO), fund_info.v_nav_decimals.fillna(DEFAULT_DECIMAL))
            # fund_nav = FOFDataManagerLite._do_calc_v_net_value_by_nav(adj_nav, adj_nav, fund_info.water_line.fillna(INIT_NAV), fund_info.incentive_fee_ratio.fillna(DEFAULT_INCENTIVE_RATIO), fund_info.v_nav_decimals.fillna(DEFAULT_DECIMAL))
            FOFDataManagerLite._v_nav = fund_nav

            trading_day = BasicDataApi().get_trading_day_list(start_date=fund_nav.index.array[0], end_date=fund_nav.index.array[-1])
            trading_day = trading_day[trading_day.datetime.between(start_date, end_date)]
            fund_nav_ffilled = fund_nav.reindex(trading_day.datetime).ffill()
            fund_nav_ffilled = fund_nav_ffilled.loc[:, fund_nav_ffilled.notna().any(axis=0)].loc[fund_nav_ffilled.notna().any(axis=1), :]
            FOFDataManagerLite._nav_filled = fund_nav_ffilled

            adj_nav_ffilled = adj_nav.reindex(trading_day.datetime).ffill()
            adj_nav_ffilled = adj_nav_ffilled.loc[:, adj_nav_ffilled.notna().any(axis=0)].loc[adj_nav_ffilled.notna().any(axis=1), :]
            FOFDataManagerLite._adj_nav_filled = adj_nav_ffilled

            wgts = pd.Series(hedge_fund_ids)
            positions, mvs, navs = FOFDataManagerLite._do_backtest(fund_nav_ffilled, wgts)
            FOFDataManagerLite._positions = positions
            fof_nav = pd.Series(navs, index=fund_nav_ffilled.index, name='fof_nav')

            positions_not_v, mvs_not_v, navs_not_v = FOFDataManagerLite._do_backtest(adj_nav_ffilled, wgts)
            FOFDataManagerLite._positions_not_v = positions_not_v
            fof_nav_not_v = pd.Series(navs_not_v, index=adj_nav_ffilled.index, name='fof_nav_no_v')
            FOFDataManagerLite._fof_nav_not_v = fof_nav_not_v

            indicators = []
            if benchmark_ids:
                benchmarks = BasicDataApi().get_index_price(index_list=benchmark_ids)
                benchmarks = benchmarks.pivot(index='datetime', columns='index_id', values='close')
                benchmarks = benchmarks.loc[start_date:end_date, :]
                fof_with_benchmark = [benchmarks[one] for one in benchmarks.columns.array]
            else:
                fof_with_benchmark = []
            fof_with_benchmark.extend([fof_nav, fof_nav_not_v])
            for data in fof_with_benchmark:
                data = data[data.notna()]
                # data.index = pd.to_datetime(data.index).date
                res_status = Calculator.get_stat_result(data.index, data.array)
                data.index = pd.to_datetime(data.index)
                to_calc_win_rate = data.resample(rule='1W').last().diff()
                weekly_win_rate = (to_calc_win_rate > 0).astype('int').sum() / to_calc_win_rate.size
                indicators.append({
                    'name': data.name,
                    'days': (data.index.array[-1] - data.index.array[0]).days,
                    'total_ret': (data[-1] / data[0]) - 1,
                    'annualized_ret': res_status.annualized_ret,
                    'annualized_vol': res_status.annualized_vol,
                    'weekly_win_rate': weekly_win_rate,
                    'mdd': res_status.mdd,
                    'sharpe': res_status.sharpe,
                })
            fof_indicators = pd.DataFrame(indicators)
            if len(fof_with_benchmark) > 1:
                fof_with_benchmarks = pd.concat(fof_with_benchmark, axis=1)
                fof_with_benchmarks = fof_with_benchmarks[fof_with_benchmarks.fof_nav.notna() & fof_with_benchmarks.fof_nav_no_v.notna()]
                fof_with_benchmarks = fof_with_benchmarks.set_index(pd.to_datetime(fof_with_benchmarks.index, infer_datetime_format=True))
                fof_with_benchmarks = fof_with_benchmarks.resample('1W').last().ffill()
                fof_with_benchmarks = fof_with_benchmarks / fof_with_benchmarks.iloc[0, :]
                fof_with_benchmarks = fof_with_benchmarks.set_axis(fof_with_benchmarks.index.date, axis=0)
            else:
                fof_with_benchmarks = None
            return fof_nav, fof_indicators, fof_with_benchmarks, lacked_funds
        except Exception as e:
            print(f'[virtual_backtest] failed, got exception {e} (hedge_fund_ids){hedge_fund_ids} (start_date){start_date} (end_date){end_date} (benchmark_ids){benchmark_ids}')
            traceback.print_exc()
            return

    @staticmethod
    def virtual_backtest_sub(hedge_fund_ids: Dict[str, str], start_date: datetime.date, end_date: Optional[datetime.date] = None) -> Optional[Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, List[str]]]:
        DEFAULT_INCENTIVE_RATIO = 0.2
        DEFAULT_DECIMAL = 4
        INIT_NAV = 1

        try:
            if end_date is None:
                end_date = datetime.date.today()
            # 获取必要的私募基金信息
            fund_info = BasicDataApi().get_hedge_fund_info(list(hedge_fund_ids.keys()))
            if fund_info is None:
                return
            fund_info = fund_info.set_index('fund_id')

            # 获取私募基金净值数据
            fund_nav = FOFDataManagerLite.get_hedge_fund_nav(list(hedge_fund_ids.keys()))
            if fund_nav is None:
                return
            # 这里首选复权净值
            adj_nav = fund_nav.pivot(index='datetime', columns='fund_id', values='adjusted_net_value')
            # 去掉全是nan的列
            valid_adj_nav = adj_nav.loc[:, adj_nav.notna().any(axis=0)]
            # 计算缺少的列
            adj_nav_lacked = set(adj_nav.columns.array) - set(valid_adj_nav.columns.array)
            if adj_nav_lacked:
                # TODO 如果某只基金完全没有复权净值 需要用累计净值来计算
                # FIXME 这里不能直接用数据库里存的虚拟净值 因为这个是邮件里发过来的单位净值虚拟后净值 而上边算出来的是复权净值虚拟后净值
                acc_nav = fund_nav[fund_nav.fund_id.isin(adj_nav_lacked)].pivot(index='datetime', columns='fund_id', values='acc_unit_value')
                adj_nav = adj_nav.join(acc_nav, how='outer')
            fund_info = fund_info.reindex(adj_nav.columns)
            lacked_funds = list(set(hedge_fund_ids.keys()) - set(adj_nav.columns.array))
            for one in lacked_funds:
                del hedge_fund_ids[one]

            # 计算虚拟净值
            fund_nav = FOFDataManagerLite._do_calc_v_net_value_by_nav(adj_nav, adj_nav, fund_info.water_line.fillna(INIT_NAV), fund_info.incentive_fee_ratio.fillna(DEFAULT_INCENTIVE_RATIO), fund_info.v_nav_decimals.fillna(DEFAULT_DECIMAL))

            trading_day = BasicDataApi().get_trading_day_list(start_date=fund_nav.index.array[0], end_date=fund_nav.index.array[-1])
            trading_day = trading_day[trading_day.datetime.between(start_date, end_date)]
            fund_nav_ffilled = fund_nav.reindex(trading_day.datetime).ffill()
            fund_nav_ffilled = fund_nav_ffilled.loc[:, fund_nav_ffilled.notna().any(axis=0)].loc[fund_nav_ffilled.notna().any(axis=1), :]

            benchmarks = BasicDataApi().get_index_price(index_list=list(set(hedge_fund_ids.values())))
            benchmarks = benchmarks.pivot(index='datetime', columns='index_id', values='close')
            benchmarks = benchmarks.loc[start_date:end_date, :]

            indicators = []
            for col in fund_nav_ffilled.columns.array:
                temp_nav = fund_nav_ffilled[col].dropna()
                the_benchmark = benchmarks[hedge_fund_ids[col]]
                the_benchmark = the_benchmark.reindex(temp_nav.index).ffill()
                res_status = Calculator.get_benchmark_stat_result(dates=temp_nav.index, values=temp_nav.array, benchmark_values=the_benchmark)
                indicators.append({
                    'fund_name': temp_nav.name,
                    'days': (temp_nav.index.array[-1] - temp_nav.index.array[0]).days,
                    'total_ret': (temp_nav[-1] / temp_nav[0]) - 1,
                    'annualized_ret': res_status.annualized_ret,
                    'annualized_vol': res_status.annualized_vol,
                    'mdd': res_status.mdd,
                    'sharpe': res_status.sharpe,
                    'ir': res_status.ir,
                })
            fund_nav_ffilled = fund_nav_ffilled.set_index(pd.to_datetime(fund_nav_ffilled.index, infer_datetime_format=True))
            fund_nav_ffilled = fund_nav_ffilled.resample('1W').last().ffill()
            fund_nav_ffilled = fund_nav_ffilled / fund_nav_ffilled.iloc[0, :]
            fund_nav_ffilled = fund_nav_ffilled.set_axis(fund_nav_ffilled.index.date, axis=0)
            return pd.DataFrame(indicators), fund_nav_ffilled
        except KeyError as e:
            print(f'[virtual_backtest] failed, got exception {e} (hedge_fund_ids){hedge_fund_ids} (start_date){start_date} (end_date){end_date}')
            return


if __name__ == "__main__":
    MANAGER_ID = 'py1'
    FOF_ID = 'SLW695'

    fof_dm = FOFDataManagerLite()
    # fof_dm.pull_hedge_fund_nav(manager_id=MANAGER_ID, fof_id=FOF_ID)
    fof_dm.calc_fof_nav(manager_id=MANAGER_ID, fof_id=FOF_ID, dump_to_db=True, debug_mode=True)
    # fof_dm.calc_all(manager_id=MANAGER_ID, fof_id=FOF_ID)
