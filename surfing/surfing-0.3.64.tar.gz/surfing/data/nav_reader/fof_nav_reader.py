

from typing import Optional, List, Dict, Any
import os
import traceback
import time

import pandas as pd

from ...util.mail_retriever import MailAttachmentRetriever, UID_FILE_NAME
from ...util.wechat_bot import WechatBot
from ..wrapper.mysql import DerivedDatabaseConnector
from ..view.derived_models import FOFNav
from ..api.basic import BasicDataApi
from ..api.derived import DerivedDataApi


class FOFNAVReader:

    COLUMNS_DICT = {
        '基金代码': 'fof_id',
        '产品代码': 'fof_id',
        '资产代码': 'fof_id',
        '基金名称': 'fund_name',
        '产品名称': 'fund_name',
        '资产名称': 'fund_name',
        '基金份额净值': 'nav',
        '单位净值': 'nav',
        '计提前单位净值': 'nav',
        '资产份额净值(元)': 'nav',
        '基金份额累计净值': 'acc_net_value',
        '累计单位净值': 'acc_net_value',
        '累计净值': 'acc_net_value',
        '资产份额累计净值(元)': 'acc_net_value',
        '虚拟后净值': 'v_net_value',
        '虚拟净值': 'v_net_value',
        '计提后单位净值': 'v_net_value',
        '虚拟计提净值': 'v_net_value',
        '虚拟后单位净值': 'v_net_value',
        '复权累计净值': 'adjusted_nav',
        '复权净值': 'adjusted_nav',
        '净值(分红再投)': 'adjusted_nav',
        '日期': 'datetime',
        '净值日期': 'datetime',
        '业务日期': 'datetime',
        '估值日期': 'datetime',
        '计算日期': 'calc_date',
    }

    def __init__(self, info: Dict[str, Any]):
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

        email_data_base_dir = os.environ['SURFING_EMAIL_DATA_DIR']

        self._read_dir = os.path.join(email_data_base_dir, f"attachments/{info['manager_id']}_{info['fof_id']}")
        os.makedirs(self._read_dir, exist_ok=True)
        assert os.path.isdir(self._read_dir), f'arg dump_dir should be a directory (now){self._read_dir}'

        self._manager_id = info['manager_id']
        self._fof_id = info['fof_id']
        self._sp_uri = f"{info['server']}:{info['port']}"
        self._user_name = info['email']
        self._password = info['password']
        self._wechat_bot = WechatBot()

    def _read_for_Template1(self, file_path: str) -> pd.DataFrame:
        df = pd.read_excel(file_path)
        df = df.loc[:, ['估值日期', '单位净值', '累计单位净值']]
        df = df.rename(columns=FOFNAVReader.COLUMNS_DICT)
        df['fof_id'] = self._fof_id
        return df

    @staticmethod
    def _read_for_Template2(file_path: str) -> pd.DataFrame:
        df = pd.read_excel(file_path)
        df = df.loc[:, ['产品代码', '产品名称', '净值日期', '单位净值', '累计净值']]
        df = df.rename(columns=FOFNAVReader.COLUMNS_DICT)
        return df

    @staticmethod
    def _read_for_OrientSec(file_path: str) -> pd.DataFrame:
        df = pd.read_excel(file_path, header=None)
        df.iloc[:, 0] = df.iloc[:, 0].map(lambda x: x.strip().split('：')[0] if isinstance(x, str) else x)
        df = df.set_index(df.columns[0])
        date = df.index.array[2].date()
        df = df.T.loc[:, ['基金代码', '基金名称', '基金份额净值', '基金份额累计净值']]
        df = df[df.notna().any(axis=1)]
        df = df.rename(columns=FOFNAVReader.COLUMNS_DICT).assign(datetime=date)
        return df

    @staticmethod
    def _read_for_GuoTaiJunAnSec(file_path: str) -> pd.DataFrame:
        df = pd.read_excel(file_path)
        df = df.loc[:, ['产品代码', '产品名称', '净值日期', '单位净值', '累计单位净值']]
        df = df.rename(columns=FOFNAVReader.COLUMNS_DICT)
        return df

    @staticmethod
    def _read_for_HuaTaiSec(file_path: str) -> pd.DataFrame:
        df = pd.read_excel(file_path)
        df = df.loc[:, ['资产代码', '资产名称', '日期', '资产份额净值(元)', '资产份额累计净值(元)']]
        df = df.rename(columns=FOFNAVReader.COLUMNS_DICT)
        return df

    def _notify_error_event(self, err_msg: str):
        print(f'[read_navs_and_dump_to_db] {err_msg}')
        # self._wechat_bot.send_hedge_fund_nav_update_failed(err_msg)

    def read_navs_and_dump_to_db(self):
        fof_info = BasicDataApi().get_fof_info(self._manager_id, [self._fof_id])
        custodian_name = fof_info.custodian_name.array[0]
        try:
            with open(os.path.join(self._read_dir, UID_FILE_NAME), 'rb') as f:
                uid_last = f.read()
                if not uid_last:
                    uid_last = None
        except FileNotFoundError:
            uid_last = None
        except Exception as e:
            self._notify_error_event(f'read uid file failed (e){e}, use None instead(read all emails) (manager_id){self._manager_id} (fof_id){self._fof_id}')
            uid_last = None

        try:
            mar = MailAttachmentRetriever(self._read_dir, ['xls', 'xlsx', 'pdf'])
            data = mar.get_excels(self._sp_uri, self._user_name, self._password, uid_last)
        except Exception as e:
            self._notify_error_event(f'FATAL ERROR!! get new data of hedge fund nav failed (e){e} (manager_id){self._manager_id} (fof_id){self._fof_id}')
            return

        parsers = {
            '东方证券': FOFNAVReader._read_for_OrientSec,
            '国泰君安证券': FOFNAVReader._read_for_GuoTaiJunAnSec,
            '中信证券': self._read_for_Template1,
            '中国国际金融股份': FOFNAVReader._read_for_Template2,
            '华泰证券': FOFNAVReader._read_for_HuaTaiSec,
        }

        can_not_update = False
        uid_last_succeed: Optional[bytes] = None
        df_list: List[pd.DataFrame] = []
        for name, comp_date in data.items():
            uid, file_path = comp_date

            try:
                for c_name, func in parsers.items():
                    if c_name in custodian_name:
                        try:
                            df = func(file_path)
                            print(df)
                        except Exception:
                            pass
                            # can_not_update = True
                        else:
                            break
                else:
                    raise NotImplementedError(f'unknown hedge fund nav file from attachment (manager_id){self._manager_id} (fof_id){self._fof_id}')
            except Exception as e:
                if not can_not_update:
                    # 走到这里都认为是已经处理完了这条数据
                    uid_last_succeed = uid
                self._notify_error_event(f'{e} (parse) (name){name} (file_path){file_path} (manager_id){self._manager_id} (fof_id){self._fof_id}')
                continue

            if not can_not_update:
                # 走到这里都认为是已经处理完了这条数据
                uid_last_succeed = uid

            try:
                df = df[df.fof_id == self._fof_id]
                if df.empty:
                    continue
                df = df.drop(columns=['fund_name'], errors='ignore')
                df['manager_id'] = self._manager_id
                df = self._dump_to_db(df)
                if df is not None:
                    df_list.append(df)
                else:
                    print(f'[read_navs_and_dump_to_db] duplicated data, do not process it (name){name} (manager_id){self._manager_id} (fof_id){self._fof_id}')
                time.sleep(1)
            except Exception as e:
                traceback.print_exc()
                self._notify_error_event(f'{e} (dump) (name){name} (file_path){file_path} (manager_id){self._manager_id} (fof_id){self._fof_id}')
                break

        if df_list:
            try:
                whole_df = pd.concat(df_list).set_index('fof_id')
                print(whole_df)
                # self._wechat_bot.send_hedge_fund_nav_update(whole_df)
            except Exception as e:
                self._notify_error_event(f'{e} (concat) (manager_id){self._manager_id} (fof_id){self._fof_id}')
                return
            else:
                print(f'[read_navs_and_dump_to_db] done (uid_last){uid_last_succeed} (df){whole_df} (manager_id){self._manager_id} (fof_id){self._fof_id}')
        else:
            whole_df = None
            print(f'[read_navs_and_dump_to_db] no new data this time, done (uid_last){uid_last_succeed} (manager_id){self._manager_id} (fof_id){self._fof_id}')
        # 记录下成功的最后一个uid
        if uid_last_succeed is not None:
            with open(os.path.join(self._read_dir, UID_FILE_NAME), 'wb') as f:
                f.write(uid_last_succeed)
            return whole_df
        return

    def _dump_to_db(self, df: pd.DataFrame):
        def _check_after_merged(x: pd.Series, now_df: pd.DataFrame):
            try:
                now_data = now_df[(now_df.fof_id == x.fof_id) & (now_df.datetime == x.datetime)]
                if now_data[['nav', 'acc_net_value', 'adjusted_nav']].iloc[0].astype('float64').equals(x[['nav', 'acc_net_value', 'adjusted_nav']].astype('float64')):
                    return pd.Series(dtype='object')
                else:
                    return x
            except (KeyError, IndexError):
                return x

        # TODO:
        assert df.datetime.nunique() == 1, 'should have single datetime'
        now_df = DerivedDataApi().get_fof_nav(self._manager_id, [self._fof_id])
        if now_df is not None and not now_df.empty:
            # 同产品同日期的净值如果已经存在了且没有变化，就不写DB了
            now_df = now_df.drop(columns=['update_time', 'create_time', 'is_deleted', 'volume', 'mv', 'ret']).sort_values(by=['fof_id', 'datetime']).drop_duplicates(subset=['fof_id', 'datetime'], keep='last')
            now_df = now_df.astype({'nav': 'float64', 'acc_net_value': 'float64', 'adjusted_nav': 'float64'})
            df = df.reindex(columns=now_df.columns).astype(now_df.dtypes.to_dict())
            df = df.merge(now_df, how='left', on=['manager_id', 'fof_id', 'datetime', 'nav', 'acc_net_value'], indicator=True, validate='one_to_one')
            df = df[df._merge == 'left_only'].drop(columns=['_merge', 'adjusted_nav_y']).rename(columns={'adjusted_nav_x': 'adjusted_nav'})
            if df.empty:
                return
            # FIXME 没想到特别好的方法 遍历每一行再check一下
            df['datetime'] = pd.to_datetime(df.datetime, infer_datetime_format=True).dt.date
            df = df.apply(_check_after_merged, axis=1, now_df=now_df)
            if df.empty:
                return
            df = df.set_index(['fof_id', 'datetime'])
            print(df)
            df.update(now_df.set_index(['fof_id', 'datetime']), overwrite=False)
            df = df.reset_index()
            df['datetime'] = df.datetime.map(lambda x: x.date())
            print(df)
            # 先删后添
            for date_to_delete in df.datetime.unique():
                DerivedDataApi().delete_fof_nav(date_to_delete=date_to_delete, manager_id=self._manager_id, fof_id_list=[self._fof_id])
        df.to_sql(FOFNav.__table__.name, DerivedDatabaseConnector().get_engine(), index=False, if_exists='append')
        return df


if __name__ == '__main__':
    import requests

    url = 'https://fof.prism-advisor.com/api/v1/manager_mail/email_task'
    verify_token = 'jisn401f7ac837da42b97f613d789819f37bee6a'

    res = requests.post(
        url=url,
        data={
            'verify_token': verify_token,
        }
    )
    for one in res.json()['data']:
        print(one)
        fof_nav_r = FOFNAVReader(one)
        fof_nav_r.read_navs_and_dump_to_db()
