
from typing import Dict, Any, Tuple, List
import math
import json
import io
import re
import datetime

import numpy as np
import pandas as pd

from sqlalchemy.orm import sessionmaker

from ...util.singleton import Singleton
from ...constant import FOFTradeStatus, DividendCalcMethod
from ..view.derived_models import HedgeFundInvestorPurAndRedemp, HedgeFundInvestorDivAndCarry, HedgeFundCustodianData
from ..wrapper.mysql import DerivedDatabaseConnector
from ..api.basic import BasicDataApi
from ..api.derived import DerivedDataApi


class HedgeFundDataManager(metaclass=Singleton):

    def __init__(self):
        pass

    def _get_total_share(self, manager_id: str, fof_id: str, investor_id: str = '', exclude1: List[int] = [], exclude2: List[str] = []) -> Tuple[float, pd.DataFrame]:
        part1 = DerivedDataApi().get_hedge_fund_investor_pur_redemp(manager_id, [fof_id])
        assert part1 is not None, '!!!!'
        part1 = part1[~part1.id.isin(exclude1)]
        part1_total_share = part1.share_changed.sum()
        if investor_id:
            part1 = part1.loc[part1.investor_id == investor_id, :]

        part2 = DerivedDataApi().get_hedge_fund_investor_div_carry(manager_id, [fof_id])
        part2 = part2[~part2.id.isin(exclude2)]
        assert part2 is not None, '!!!!'
        part2_total_share = part2.share_changed.sum()
        if investor_id:
            part2 = part2.loc[part2.investor_id == investor_id, :]

        total_share = part1_total_share + part2_total_share
        share_separate = part1[['investor_id', 'share_changed']].groupby(by='investor_id', sort=False).sum().add(part2[['investor_id', 'share_changed']].groupby(by='investor_id', sort=False).sum(), fill_value=0)
        return total_share, share_separate

    def _refresh_datas_after_updating(self, manager_id: str, fof_id: str, investor_id: str, datetime):
        datetime: datetime.date = pd.to_datetime(datetime, infer_datetime_format=True).date()

        part1 = DerivedDataApi().get_hedge_fund_investor_pur_redemp(manager_id, [fof_id])
        assert part1 is not None, '!!!!'
        part1 = part1[part1.investor_id == investor_id].sort_values(by='datetime')
        last_valid_share: float = part1[part1.datetime <= datetime].iloc[-1, :].share_after_trans

        to_refresh = part1.loc[part1.datetime > datetime, :]
        to_refresh = to_refresh.set_index('id').share_changed.cumsum() + last_valid_share

        Session = sessionmaker(DerivedDatabaseConnector().get_engine())
        db_session = Session()
        for row in db_session.query(HedgeFundInvestorPurAndRedemp).filter(
            HedgeFundInvestorPurAndRedemp.manager_id == manager_id,
            HedgeFundInvestorPurAndRedemp.fof_id == fof_id,
            HedgeFundInvestorPurAndRedemp.investor_id == investor_id,
            HedgeFundInvestorPurAndRedemp.datetime > datetime,
        ).all():
            row.share_after_trans = float(to_refresh.at[row.id])
        db_session.commit()
        db_session.close()

    def _calc_share_details(self, fof_info, manager_id: str, fof_id: str, investor_id: str) -> List[Dict[str, Any]]:
        part1 = DerivedDataApi().get_hedge_fund_investor_pur_redemp(manager_id, [fof_id])
        assert part1 is not None, '!!!!'
        part1 = part1.loc[part1.investor_id == investor_id, ['datetime', 'event_type', 'share_changed', 'net_asset_value', 'acc_unit_value']]

        part2 = DerivedDataApi().get_hedge_fund_investor_div_carry(manager_id, [fof_id])
        assert part2 is not None, '!!!!'
        part2 = part2.loc[(part2.investor_id == investor_id) & (part2.event_type.isin([FOFTradeStatus.DIVIDEND_VOLUME, FOFTradeStatus.DEDUCT_REWARD])), ['datetime', 'event_type', 'share_changed', 'net_asset_value', 'acc_unit_value']]

        total = pd.concat([part1, part2]).sort_values(by='datetime')
        share_details = []
        for row in total.itertuples(index=False):
            if row.event_type in (FOFTradeStatus.PURCHASE, FOFTradeStatus.SUBSCRIBE, FOFTradeStatus.DIVIDEND_VOLUME):
                share_details.append({'datetime': row.datetime, 'share': row.share_changed, 'water_line': row.acc_unit_value})
            elif row.event_type == FOFTradeStatus.REDEEM:
                share_changed = abs(row.share_changed)
                for one in share_details:
                    assert share_changed > 0, f'!!! {share_changed}'
                    if one['share'] >= share_changed:
                        one['share'] -= share_changed
                        break
                    else:
                        share_changed -= one['share']
                        one['share'] = 0
                else:
                    assert False, 'not enough shares to redeem in history'
            elif row.event_type == FOFTradeStatus.DEDUCT_REWARD:
                for one in share_details:
                    if math.isclose(one['share'], 0):
                        continue
                    if one['acc_unit_value'] >= row.acc_unit_value:
                        # 当前水位线未超过该笔份额的水位线 不需要计提业绩报酬
                        continue
                    carry = self._calc_carry(row.acc_unit_value, one['acc_unit_value'], fof_info.incentive_fee_type, fof_info.incentive_fee_str) * one['share'] / row.net_asset_value
                    assert one['share'] >= carry, f'!!!'
                    one['share'] -= carry
                    # 水位线变成本次计提时的水位线了
                    one['acc_unit_value'] = row.acc_unit_value
            else:
                assert False, f'invalid event type {row.event_type} during doing carry calc'
        return share_details

    def investor_pur_redemp_update(self, datas: Dict[str, Any]) -> int:
        '''
        申赎记录更新/添加

        Parameters
        ----------
        datas : Dict[str, Any]
            数据, keys:
                id : 如果是添加 则不需要该字段; 否则则需要
                fof_id : 产品ID
                manager_id : 管理端ID
                datetime : 交易日期
                event_type : 交易类型(认购/申购/赎回)
                investor_id : 投资人ID
                net_asset_value : 单位净值
                acc_unit_value : 累计净值
                amount : 申购金额/认购金额
                raising_interest : 募集期利息
                redemp_share : 赎回份额
                redemp_fee : 赎回费

        Returns/Exceptions
        -------
        throw excepion if failed, or return id (an integer) if succeed
        '''
        fof_info = BasicDataApi().get_fof_info(datas['manager_id'], fof_id_list=[datas['fof_id']])
        assert fof_info is not None, '!!!!'
        assert fof_info.shape[0] == 1, f"invalid fof id {[datas['fof_id']]}"
        fof_info = fof_info.iloc[-1, :]

        event_type = datas['event_type']
        if event_type == FOFTradeStatus.PURCHASE:
            # 认购
            datas['purchase_amount'] = datas['amount']
            datas['share_changed'] = (datas['amount'] + datas['raising_interest']) / datas['net_asset_value']
        elif event_type == FOFTradeStatus.SUBSCRIBE:
            # 申购
            datas['purchase_amount'] = datas['amount']
            datas['share_changed'] = datas['amount'] / datas['net_asset_value']
        elif event_type == FOFTradeStatus.REDEEM:
            # 赎回
            datas['share_changed'] = -datas['redemp_share']
            datas['redemp_confirmed_amount'] = datas['redemp_share'] * datas['net_asset_value'] - datas['redemp_fee']

            # 计算业绩报酬计提
            carry_sum = 0
            share_details = self._calc_share_details(fof_info, datas['manager_id'], datas['fof_id'], datas['investor_id'])
            for one in share_details:
                if math.isclose(one['share'], 0):
                    continue
                if one['share'] >= datas['redemp_share']:
                    one['share'] -= datas['redemp_share']
                    if datas['acc_unit_value'] > one['water_line']:
                        carry_sum += self._calc_carry(datas['acc_unit_value'], one['water_line'], fof_info.incentive_fee_type, fof_info.incentive_fee_str) * datas['redemp_share']
                    break
                else:
                    datas['redemp_share'] -= one['share']
                    if datas['acc_unit_value'] > one['water_line']:
                        carry_sum += self._calc_carry(datas['acc_unit_value'], one['water_line'], fof_info.incentive_fee_type, fof_info.incentive_fee_str) * one['share']
                    one['share'] = 0
            else:
                assert False, 'not enough shares to redeem'
            datas['carry_amount'] = carry_sum
        else:
            raise ValueError(f'invalid event_type {event_type}')

        _, share_separate = self._get_total_share(datas['manager_id'], datas['fof_id'], datas['investor_id'], exclude1=[datas['id']] if 'id' in datas else [])
        try:
            datas['share_after_trans'] = float(share_separate.at[datas['investor_id'], 'share_changed']) + datas['share_changed']
        except KeyError:
            datas['share_after_trans'] = datas['share_changed']

        datas['applied_date'] = datas['datetime']
        datas['deposited_date'] = datas['datetime']

        s = pd.Series(datas).drop(['amount', 'redemp_share'], errors='ignore')
        # TODO: 原子操作下面几步
        if 'id' in datas:
            DerivedDataApi().delete_hedge_fund_investor_pur_redemp(id_to_delete=datas['id'])
        sql_obj = HedgeFundInvestorPurAndRedemp()
        for k, v in s.to_dict().items():
            setattr(sql_obj, k, v)
        with DerivedDatabaseConnector().managed_session() as session:
            session.add(sql_obj)
            session.commit()
            the_id = sql_obj.id
        # df.to_sql(HedgeFundInvestorPurAndRedemp.__table__.name, DerivedDatabaseConnector().get_engine(), index=False, if_exists='append')
        if 'id' in datas:
            self._refresh_datas_after_updating(datas['manager_id'], datas['fof_id'], datas['investor_id'], datas['datetime'])
        return the_id

    def _calc_carry(self, nav: float, water_line: float, fee_type: str, fee_desc: str) -> float:
        profit: float = nav - water_line
        if fee_type == '1':
            return profit * float(fee_desc)
        elif fee_type == '2':
            fee_df = pd.DataFrame(json.loads(fee_desc)).sort_values(by='start', ascending=False)
            if fee_df.empty:
                assert False, f'invalid fee str {fee_desc} (fee_type){fee_type}'
            total_profit = 0
            for row in fee_df.itertuples(index=False):
                assert profit > 0, '!!!!'
                level_profit: float = row.start * water_line
                if profit > level_profit:
                    total_profit += (profit - level_profit) * row.val
                    profit = level_profit
            return total_profit
        else:
            assert False, f'invalid fee type {fee_type}, do not support to calc carry by it'

    def investor_pur_redemp_remove(self, id: int):
        '''
        申赎记录删除

        Parameters
        ----------
        id : int
            对应数据库中id

        Returns/Exceptions
        -------
        throw excepion if failed
        '''

        df = DerivedDataApi().get_hedge_fund_investor_pur_redemp_by_id(id)
        assert df is not None, f'failed to get hedge fund investor data by id {id}'
        assert df.shape[0] == 1, f'invalid id {id}'

        s = df.iloc[-1, :]
        DerivedDataApi().delete_hedge_fund_investor_pur_redemp(id_to_delete=id)
        self._refresh_datas_after_updating(s.manager_id, s.fof_id, s.investor_id, s.datetime)

    def investor_div_carry_add(self, datas: Dict[str, Any]):
        '''
        分红/业绩计提记录添加

        Parameters
        ----------
        datas : Dict[str, Any]
            数据, keys:
                fof_id : 产品ID
                datetime : 分红/计提日期
                manager_id : 管理端ID
                event_type : 交易类型(现金分红/红利再投/计提业绩报酬)
                investor_id : 投资人ID
                net_asset_value : 单位净值
                acc_unit_value : 累计净值
                total_dividend : 红利总额
                cash_dividend : 现金分红金额
                reinvest_amount : 再投资金额
                carry_amount : 业绩报酬金额
                share_changed : 份额变更
                share_after_trans : 分红/计提后份额

        Returns/Exceptions
        -------
        throw excepion if failed, or return id (an integer) if succeed
        '''

        event_type = datas['event_type']
        if event_type == FOFTradeStatus.DEDUCT_REWARD:
            # 计提业绩报酬 暂不需要额外处理
            pass
        else:
            total_share, share_separate = self._get_total_share(datas['manager_id'], datas['fof_id'], datas['investor_id'])
            share_separate = share_separate.share_changed.array[-1]
            div = datas['total_dividend'] * share_separate / total_share

            if event_type == FOFTradeStatus.DIVIDEND_CASH:
                # 现金分红
                datas['share_changed'] = 0
                datas['cash_dividend'] = div
            elif event_type == FOFTradeStatus.DIVIDEND_VOLUME:
                # 红利再投
                datas['share_changed'] = (div - (datas['carry_amount'] if not pd.isnull(datas['carry_amount']) else 0)) / datas['net_asset_value']
                datas['reinvest_amount'] = div
            else:
                raise ValueError(f'invalid event_type {event_type}')

            datas['share_after_trans'] = share_separate + datas['share_changed']

            for k in ('reinvest_amount', 'cash_dividend', 'total_dividend'):
                datas[k] = float(datas[k])

        for k in ('net_asset_value', 'acc_unit_value', 'carry_amount', 'share_changed', 'share_after_trans'):
            datas[k] = float(datas[k])

        datas['applied_date'] = datas['datetime']
        datas['deposited_date'] = datas['datetime']
        df = pd.Series(datas).to_frame().T
        # TODO: 原子操作下面几步
        if 'id' in datas:
            DerivedDataApi().delete_hedge_fund_investor_div_carry(id_to_delete=datas['id'])
        df.to_sql(HedgeFundInvestorDivAndCarry.__table__.name, DerivedDatabaseConnector().get_engine(), index=False, if_exists='append')

    def investor_div_carry_remove(self, id: int):
        '''
        分红/业绩计提记录删除

        Parameters
        ----------
        id : int
            对应数据库中id

        Returns/Exceptions
        -------
        throw excepion if failed
        '''

        DerivedDataApi().delete_hedge_fund_investor_div_carry(id_to_delete=id)

    def calc_dividend_event(self, datas: Dict[str, Any]) -> pd.DataFrame:
        '''
        计算分红事件

        Parameters
        ----------
        datas : Dict[str, Any]
            数据, keys:
                fof_id : 产品ID
                manager_id : 管理端ID
                datetime : 分红日期
                event_type : 红利发放方式(现金分红/红利再投)
                net_asset_value : 单位净值
                acc_unit_value : 累计净值
                calc_method : 计算方法(红利总额/每单位红利)
                dividend_for_calc : 红利总额/每单位红利
                do_deduct_reward: 是否计提业绩报酬

        Returns/Exceptions
        -------
        throw excepion if failed, or return a pd.DataFrame if succeed
        '''

        total_share, share_separate = self._get_total_share(datas['manager_id'], datas['fof_id'])
        share_separate = share_separate.share_changed
        weight = share_separate / total_share

        calc_method = datas['calc_method']
        if calc_method == DividendCalcMethod.BY_TOTAL_AMOUNT:
            # 红利总额
            dividend_amount = datas['dividend_for_calc']
        elif calc_method == DividendCalcMethod.BY_PER_UNIT:
            # 每单位红利
            dividend_amount = total_share * datas['dividend_for_calc']
        else:
            raise ValueError(f'invalid calc_method {calc_method}')

        s = dividend_amount * weight
        event_type = datas['event_type']
        if datas['event_type'] == FOFTradeStatus.DIVIDEND_CASH:
            # 现金分红
            df = s.to_frame('cash_dividend')
            if 'do_deduct_reward' in datas and datas['do_deduct_reward']:
                carry_df = self.calc_carry_event(datas)
                df = df.join(carry_df.set_index('investor_id').carry_amount)
                df['cash_dividend'] -= df.carry_amount
            else:
                df['carry_amount'] = np.nan
            df['share_changed'] = 0
            df['reinvest_amount'] = 0
        elif datas['event_type'] == FOFTradeStatus.DIVIDEND_VOLUME:
            # 红利再投
            df = s.to_frame('reinvest_amount')
            if 'do_deduct_reward' in datas and datas['do_deduct_reward']:
                carry_df = self.calc_carry_event(datas)
                df = df.join(carry_df.set_index('investor_id').carry_amount)
                df['reinvest_amount'] -= df.carry_amount
            else:
                df['carry_amount'] = np.nan
            df['share_changed'] = df.reinvest_amount / datas['net_asset_value']
            df['cash_dividend'] = 0
        else:
            raise ValueError(f'invalid event_type {event_type}')
        df['share_after_trans'] = share_separate + df.share_changed

        df['fof_id'] = datas['fof_id']
        df['manager_id'] = datas['manager_id']
        df['datetime'] = datas['datetime']
        df['event_type'] = datas['event_type']
        df['total_dividend'] = dividend_amount
        return df.reset_index()

    def calc_carry_event(self, datas: Dict[str, Any]) -> pd.DataFrame:
        '''
        计算业绩计提事件

        Parameters
        ----------
        datas : Dict[str, Any]
            数据, keys:
                fof_id : 产品ID
                manager_id : 管理端ID
                datetime : 计提日期
                net_asset_value : 单位净值
                acc_unit_value : 累计净值

        Returns/Exceptions
        -------
        throw excepion if failed, or return a pd.DataFrame if succeed
        '''

        fof_info = BasicDataApi().get_fof_info(datas['manager_id'], fof_id_list=[datas['fof_id']])
        assert fof_info is not None, '!!!!'
        assert fof_info.shape[0] == 1, f"invalid fof id {[datas['fof_id']]}"
        fof_info = fof_info.iloc[-1, :]

        part1 = DerivedDataApi().get_hedge_fund_investor_pur_redemp(datas['manager_id'], [datas['fof_id']])
        assert part1 is not None, '!!!!'

        carry_data = []
        for investor_id in part1.investor_id.unique():
            share_details = self._calc_share_details(fof_info, datas['manager_id'], datas['fof_id'], investor_id)
            share_before_trans = pd.DataFrame(share_details).share.sum()
            carry_amount_sum = 0
            share_changed = 0
            for one in share_details:
                if math.isclose(one['share'], 0):
                    continue
                if one['water_line'] >= datas['acc_unit_value']:
                    # 当前水位线未超过该笔份额的水位线 不需要计提业绩报酬
                    continue
                carry_amount = self._calc_carry(datas['acc_unit_value'], one['water_line'], fof_info.incentive_fee_type, fof_info.incentive_fee_str) * one['share']
                carry = carry_amount / datas['net_asset_value']
                assert one['share'] >= carry, f'!!!'
                carry_amount_sum += carry_amount
                share_changed -= carry
                one['share'] -= carry
                # 水位线变成本次计提时的水位线了
                one['water_line'] = datas['acc_unit_value']
            carry_data.append({
                'investor_id': investor_id,
                'datetime': datas['datetime'],
                'share_before_trans': share_before_trans,
                'carry_amount': carry_amount_sum,
                'share_changed': share_changed,
                'share_after_trans': share_before_trans + share_changed
            })
        df = pd.DataFrame(carry_data)
        df['fof_id'] = datas['fof_id']
        df['manager_id'] = datas['manager_id']
        df['datetime'] = datas['datetime']
        df['event_type'] = FOFTradeStatus.DEDUCT_REWARD
        return df

    def upload_custodian_data(self, manager_id: str, fof_id: str, datas: io.BytesIO) -> datetime.date:
        '''
        上传/更新私募基金托管数据

        Parameters
        ----------
        manager_id : str
            manager id
        fof_id : str
            fof id
        datas : io.BytesIO
            open 托管数据表格获得的 file object

        Returns/Exceptions
        -------
        throw excepion if failed, or return a datetime.date if succeed
        '''

        def _transform_hedge_fund_id(x: str):
            fund_id = x.split()[0].split('.')[-1]
            real_fund_id = BasicDataApi().get_hedge_fund_alias(manager_id, fund_id)
            if real_fund_id is not None and not real_fund_id.empty:
                return real_fund_id.fund_id.array[0]
            else:
                return fund_id

        to_parse_date = pd.read_excel(datas, skiprows=3, nrows=1).columns.array[0]
        the_date = re.findall(r'[0-9\-]+', to_parse_date)
        assert the_date, f'parse date failed (info){to_parse_date}'
        the_date = pd.to_datetime(the_date[0], infer_datetime_format=True).date()

        df = pd.read_excel(datas, header=4, index_col=0)
        df = df.loc[df.index.notna(), :]
        df = df.rename(columns={'Unnamed: 7': '成本.1', 'Unnamed: 11': '市值.1', 'Unnamed: 14': '估值增值.1'})
        print(df)
        equity = df.at['资产净值', '市值.1']
        total_shares = df.at['实收资本', '数量']

        mutual_funds_part1 = df.loc[(df.index > '1105.21.01') & (df.index < '1105.24'), ['科目名称', '数量', '市值.1', '行情']]
        mutual_funds_part1 = mutual_funds_part1.reset_index(drop=True)
        mutual_funds_part2 = df.loc[(df.index > '1105.24.01') & (df.index < '1108'), ['科目名称', '数量', '市值.1', '行情']]
        mutual_funds_part2 = mutual_funds_part2.reset_index(drop=True)
        mutual_funds = pd.concat([mutual_funds_part1, mutual_funds_part2], ignore_index=True).rename(columns={
            '科目名称': 'fund_id',
            '数量': 'shares',
            '市值.1': 'mv',
            '行情': 'nav',
        })
        mutual_funds['fund_id'] = mutual_funds.fund_id.map(lambda x: x + '!0')

        hedge_funds = df.loc[(df.index > '1108.02.01') & (df.index < '1203'), ['数量', '市值.1', '行情']]
        hedge_funds['fund_id'] = hedge_funds.index.map(_transform_hedge_fund_id)
        hedge_funds = hedge_funds.reset_index(drop=True).rename(columns={
            '数量': 'shares',
            '市值.1': 'mv',
            '行情': 'nav',
        })

        deposit_in_bank = df.at['1002', '市值.1']
        interest_receivable = df.at['1204', '市值.1']
        try:
            pur_amt_receivable = df.at['1207', '市值.1']
        except KeyError:
            pur_amt_receivable = np.nan
        try:
            sec_clearing_fund = df.at['3003', '市值.1']
        except KeyError:
            sec_clearing_fund = np.nan
        try:
            dividends_receivable = df.at['1203', '市值.1']
        except KeyError:
            dividends_receivable = np.nan
        other_assets = interest_receivable + deposit_in_bank
        payable_to_managers = df.at['2206', '市值.1']
        payable_to_custodian = df.at['2207', '市值.1']
        payable_to_admin_service = 0
        got_the_item = False
        for subject in ('2215', '2206.14'):
            try:
                payable_to_admin_service += df.at[subject, '市值.1']
                got_the_item = True
            except KeyError:
                pass
        if not got_the_item:
            payable_to_admin_service = np.nan

        nav = float(df.loc['今日单位净值', '科目名称'])
        pur_amt_receivable = np.nan
        sec_clearing_fund = np.nan

        total_df = pd.Series({
            'fof_id': fof_id,
            'manager_id': manager_id,
            'datetime': the_date,
            'nav': nav,
            'equity': equity,
            'total_shares': total_shares,
            'other_assets': other_assets,
            'deposit_in_bank': deposit_in_bank,
            'interest_receivable': interest_receivable,
            'pur_amt_receivable': pur_amt_receivable,
            'sec_clearing_fund': sec_clearing_fund,
            'dividends_receivable': dividends_receivable,
            'payable_to_managers': payable_to_managers,
            'payable_to_custodian': payable_to_custodian,
            'payable_to_admin_service': payable_to_admin_service,
            'mutual_funds_data': mutual_funds.to_json(orient='records'),
            'hedge_funds_data': hedge_funds.to_json(orient='records'),
        })
        total_df = total_df.to_frame().T
        total_df = total_df.infer_objects()
        now_df = DerivedDataApi().get_hedge_fund_custodian_data(manager_id=manager_id, fof_id_list=[fof_id])
        if now_df is not None:
            now_df = now_df.drop(columns=['update_time', 'create_time', 'is_deleted']).astype(total_df.dtypes.to_dict())
            # merge on all columns
            df = total_df.round(6).merge(now_df.round(6), how='left', indicator=True, validate='one_to_one')
            df = df[df._merge == 'left_only'].drop(columns=['_merge'])
        else:
            df = total_df
        if not df.empty:
            print(df)
            for row in df.itertuples(index=False):
                DerivedDataApi().delete_hedge_fund_custodian_data(row.manager_id, row.fof_id, row.datetime)
            df.to_sql(HedgeFundCustodianData.__table__.name, DerivedDatabaseConnector().get_engine(), index=False, if_exists='append')
        return the_date

    @staticmethod
    def calc_whole_adjusted_net_value(nav_acc_data: pd.DataFrame) -> pd.DataFrame:
        '''
        计算单只基金的全量复权净值

        Parameters
        ----------
        nav_acc_data : pd.DataFrame
            净值数据, index: datetime.date 净值日期
                columns:
                    net_asset_value : 单位净值(必须从1开始)
                    acc_unit_value : 累计净值(必须从1开始)

        Returns/Exceptions
        -------
        throw excepion if failed, or return a pd.DataFrame if succeed

        value returned : pd.DataFrame
            复权净值数据, index: datetime.date 净值日期
                columns:
                    adj_nav : 复权净值
                    adj_factor: 复权因子
        '''

        # 先按index(datetime.date)排序
        nav_acc_data: pd.DataFrame = nav_acc_data.sort_index()
        assert math.isclose(nav_acc_data.net_asset_value.array[0], 1) and math.isclose(nav_acc_data.acc_unit_value.array[0], 1), f'fund nav data should start with 1 (data){nav_acc_data}'

        assert nav_acc_data.acc_unit_value.round(6).ge(nav_acc_data.net_asset_value.round(6)).all(), f'acc_unit_value should always ge than net_asset_value (data){nav_acc_data}'
        days_before_dividend: pd.Series = (nav_acc_data.acc_unit_value - nav_acc_data.net_asset_value).round(6).drop_duplicates(keep='last')
        assert days_before_dividend.notna().all(), f'fund nav data should not contains NaN (data){nav_acc_data}'
        # 这里算出来每天的分红数据不应该出现负值 这样前边的 drop_duplicates 才是对的
        assert days_before_dividend.is_monotonic_increasing, f'dividend should always be monotonic increasing (data){nav_acc_data}'

        divdidend_that_day: pd.Series = days_before_dividend.sub(days_before_dividend.shift(1, fill_value=0))
        adj_factor: pd.Series = 1 + divdidend_that_day / (nav_acc_data.loc[divdidend_that_day.index, 'net_asset_value'].shift(1, fill_value=1) - divdidend_that_day)

        df: pd.DataFrame = adj_factor.reindex(nav_acc_data.index, method='bfill').to_frame('adj_factor')
        df['adj_nav'] = df.adj_factor * nav_acc_data.net_asset_value
        df = df[['adj_nav', 'adj_factor']]
        return df
