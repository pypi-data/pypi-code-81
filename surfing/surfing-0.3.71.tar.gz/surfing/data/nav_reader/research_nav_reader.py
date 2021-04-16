

from typing import Optional, List
# import datetime
import os
import traceback
import time
import tarfile

import pandas as pd

from ...util.mail_retriever import MailAttachmentRetriever, IMAP_SPType, UID_FILE_NAME
from ...util.wechat_bot import WechatBot
from ..wrapper.mysql import RawDatabaseConnector
from ..api.raw import RawDataApi
from ..api.basic import BasicDataApi
from ..view.raw_models import HFIndexPrice, HFFundNav


class ResearchNAVReader:

    def __init__(self, read_dir: str, user_name: str, password: str):
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

        self._read_dir = read_dir
        assert os.path.isdir(self._read_dir), f'arg dump_dir should be a directory (now){self._read_dir}'

        self._user_name = user_name
        self._password = password
        self._wechat_bot = WechatBot()

    @staticmethod
    def _read_for_NAVData(file_path: str) -> pd.DataFrame:
        tar = tarfile.open(file_path, 'r:gz', encoding='gb2312')
        for one in tar:
            if not one.name.endswith('.xls') and not one.name.endswith('.xlsx'):
                continue
            if '业绩走势' in one.name:
                continue
            try:
                try:
                    print(f'[_read_for_NAVData] (name in tar){one.name}')
                except UnicodeEncodeError:
                    replace_dict = {
                        '\udc9bK': '汯',
                        '\udcacB': '珺',
                        '\udcd4Z': '訸',
                        '\udcb6G': '禛',
                    }
                    p_name = one.name
                    for k, v in replace_dict.items():
                        p_name = p_name.replace(k, v)
                    print(f'[_read_for_NAVData] (name in tar (fixed)){p_name}')
                else:
                    p_name = one.name
                p_name = p_name.split('.')[0]
                df = pd.read_excel(tar.extractfile(one), na_values=['--'])
                df = df.rename(columns={'日期': 'datetime', '净值(分红再投)': 'nav'})
                df = df[['datetime', 'nav']]
                hf_fund_info = RawDataApi().get_hf_fund_info()
                hf_fund_info = hf_fund_info[hf_fund_info.desc_name == p_name]
                fund_id = hf_fund_info.fund_id.array[0]
                df['fund_id'] = fund_id
                df['datetime'] = pd.to_datetime(df.datetime, infer_datetime_format=True).dt.date
                hf_fund_nav = RawDataApi().get_hf_fund_nav(fund_ids=[fund_id])
                if hf_fund_nav is not None:
                    df = df.astype(hf_fund_nav.dtypes.to_dict())
                    # merge on all columns
                    df = df.merge(hf_fund_nav, how='left', indicator=True, validate='one_to_one')
                    df = df[df._merge == 'left_only'].drop(columns=['_merge'])
                print(df)
                # TODO: 最好原子提交下边两步
                RawDataApi().delete_hf_fund_nav(fund_id_to_delete=fund_id, datetime_list=df.datetime.to_list())
                # 更新到db
                df.to_sql(HFFundNav.__table__.name, RawDatabaseConnector().get_engine(), index=False, if_exists='append')
            except Exception:
                traceback.print_exc()
        tar.close()

    @staticmethod
    def _read_for_IndexData(file_path: str):
        update_info = {}
        tar = tarfile.open(file_path, 'r:gz', encoding='gb2312')
        for one in tar:
            print(f'[_read_for_IndexData] (name in tar){one.name}')
            index_name = one.name.split('/')[-1].split('.')[0]
            if '朝阳永续' in one.name:
                key_name = one.name.split('朝阳永续-')[-1].split('.')[0]
                df = pd.read_excel(tar.extractfile(one), na_values=['--'], thousands=',')
                df = df.rename(columns={'时间': 'index_date', key_name: 'close'})
                df = df[['index_date', 'close']]
                df['calcu_date'] = None
            else:
                if '融智' not in one.name:
                    continue
                    # print(f'[_read_for_IndexData] got special file name {one}')
                key_name = one.name.split('融智-')[-1].split('.')[0]
                df = pd.read_excel(tar.extractfile(one), header=3, na_values=['--'])
                df = df.rename(columns={'指数日期': 'index_date', '指数计算日期': 'calcu_date', key_name: 'close'})
                df = df[['index_date', 'calcu_date', 'close']]
                df['calcu_date'] = pd.to_datetime(df.calcu_date, infer_datetime_format=True).dt.date
            df = df[df.close.notna()]
            asset_info = BasicDataApi().get_asset_info_by_type(['策略指数'])
            asset_info = asset_info[asset_info.real_name == index_name]
            if asset_info.empty:
                assert False, f'[_read_for_IndexData] can not find name of index {index_name}'
            index_id = asset_info.real_id.array[0]
            df['index_id'] = index_id
            df['index_date'] = pd.to_datetime(df.index_date, infer_datetime_format=True).dt.date
            hf_index_price = RawDataApi().get_hf_index_price(index_ids=[index_id])
            if hf_index_price is not None:
                df = df.astype(hf_index_price.dtypes.to_dict())
                # merge on all columns
                df = df.merge(hf_index_price, how='left', indicator=True, validate='one_to_one')
                df = df[df._merge == 'left_only'].drop(columns=['_merge'])
            print(df)
            # TODO: 最好原子提交下边两步
            RawDataApi().delete_hf_index_price(index_id, df.index_date.to_list())
            # 更新到db
            df.to_sql(HFIndexPrice.__table__.name, RawDatabaseConnector().get_engine(), index=False, if_exists='append')
            update_info[key_name] = df.shape[0]
        tar.close()
        return update_info

    def _notify_error_event(self, err_msg: str):
        print(f'[read_navs_and_dump_to_db] {err_msg}')
        # self._wechat_bot.send_hedge_fund_nav_update_failed(err_msg)

    def read_navs_and_dump_to_db(self):
        try:
            with open(os.path.join(self._read_dir, UID_FILE_NAME), 'rb') as f:
                uid_last = f.read()
                if not uid_last:
                    uid_last = None
        except Exception as e:
            self._notify_error_event(f'read uid file failed (e){e}, use None instead(read all emails)')
            uid_last = None

        try:
            mar = MailAttachmentRetriever(self._read_dir, ['tar.gz', ])
            data = mar.get_excels(IMAP_SPType.IMAP_QQ, self._user_name, self._password, uid_last)
        except Exception as e:
            self._notify_error_event(f'FATAL ERROR!! get new data of hedge fund nav failed (e){e}')
            return

        uid_last_succeed: Optional[bytes] = None
        for name, comp_date in data.items():
            uid, file_path = comp_date
            if not name.endswith('.tar.gz'):
                continue

            try:
                if '净值数据' in name:
                    ResearchNAVReader._read_for_NAVData(file_path)
                elif '指数数据' in name:
                    update_info = ResearchNAVReader._read_for_IndexData(file_path)
                else:
                    raise NotImplementedError('unknown research nav file from attachment')
            except Exception as e:
                traceback.print_exc()
                self._notify_error_event(f'{e} (parse) (name){name} (file_path){file_path}')
                continue

            uid_last_succeed = uid
            time.sleep(1)

        # 记录下成功的最后一个uid
        if uid_last_succeed is not None:
            with open(os.path.join(self._read_dir, UID_FILE_NAME), 'wb') as f:
                f.write(uid_last_succeed)
        return


if __name__ == '__main__':
    try:
        email_data_dir = os.environ['SURFING_EMAIL_DATA_DIR']
        user_name = os.environ['SURFING_EMAIL_USER_NAME']
        password = os.environ['SURFING_EMAIL_PASSWORD']
    except KeyError as e:
        import sys
        sys.exit(f'can not found enough params in env (e){e}')

    r_nav_r = ResearchNAVReader(email_data_dir, user_name, password)
    r_nav_r.read_navs_and_dump_to_db()
