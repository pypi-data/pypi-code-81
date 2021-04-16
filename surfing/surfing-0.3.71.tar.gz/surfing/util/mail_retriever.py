
import imaplib
import email
import traceback
import enum
import os
import re
from email.header import decode_header, make_header

from typing import Dict, Optional, Tuple, Union
import pandas as pd


UID_FILE_NAME = 'mail_uid_recorder'


class IMAP_SPType(enum.IntEnum):
    IMAP_QQ = 1  # 企业微信邮箱


class MailAttachmentRetriever:

    _IMAP_SERVER_INFO = {
        IMAP_SPType.IMAP_QQ: ('imap.exmail.qq.com', 993)
    }

    def __init__(self, dump_dir: str, file_suffixes: Tuple[str]):
        self._dump_dir = dump_dir
        assert os.path.isdir(self._dump_dir), f'arg dump_dir should be a directory (now){self._dump_dir}'

        self._file_suffixes = []
        for one in file_suffixes:
            if not one.startswith('.'):
                self._file_suffixes.append('.' + one)
            else:
                self._file_suffixes.append(one)
        print(f'(file suffixes){self._file_suffixes}')

    def get_excels(self, sp_type_or_uri: Union[IMAP_SPType, str], user: str, pw: str, last_uid: bytes = None) -> Optional[Dict[str, Tuple[bytes, os.PathLike]]]:
        if isinstance(sp_type_or_uri, IMAP_SPType):
            try:
                host, port = self._IMAP_SERVER_INFO[sp_type_or_uri]
            except KeyError:
                print(f'invalid SP type {sp_type_or_uri}, do not support it')
                return
        else:
            try:
                host, port = sp_type_or_uri.split(':')
            except Exception:
                print(f'invalid sp uri {sp_type_or_uri}, the format should be url:port')
                return
        try:
            df_list: Dict[str, pd.DataFrame] = {}
            with imaplib.IMAP4_SSL(host=host, port=port) as M:
                M.login(user, pw)
                M.select(mailbox='Inbox', readonly=True)
                if last_uid is None:
                    criterion = 'ALL'
                else:
                    last_uid = int(last_uid)
                    criterion = f'(TO "fof@puyuan.tech" UID {last_uid}:*)'
                    print(criterion)
                typ, data = M.uid('search', None, criterion)
                for uid in data[0].split():
                    # 上边的criterion不太好用 这里还是需要再过滤一下
                    if last_uid is not None and int(uid) <= last_uid:
                        continue
                    # 邮件应该是按顺序过来的
                    # 遍历每一封邮件
                    is_done = False
                    typ, data = M.uid('fetch', uid, '(RFC822)')
                    raw_email = data[0][1]
                    email_message = email.message_from_bytes(raw_email)
                    for part in email_message.walk():
                        # excel类型的附件这里的content maintype其实都是application
                        if part.get_content_maintype() != 'multipart':
                            # 这个条件是判断附件的关键
                            if part.get('Content-Disposition') is not None:
                                filename = part.get_filename()
                                if filename is not None:
                                    real_name = email.header.decode_header(filename)[0][0]
                                    if isinstance(real_name, bytes):
                                        real_name = real_name.decode(email.header.decode_header(filename)[0][1])
                                    for one in self._file_suffixes:
                                        if real_name.endswith(one):
                                            # pandas可以直接读，但pd.read_excel()里传的参数可能是不一样的，所以这里还是先将内容写到文件里
                                            # TODO: need to remove this
                                            if real_name == '产品净值情况.xlsx':
                                                real_name = f'产品净值情况_{uid}.xlsx'
                                            file_path = os.path.join(self._dump_dir, real_name)
                                            with open(file_path, 'wb') as f:
                                                f.write(part.get_payload(decode=True))
                                            df_list[real_name] = (uid, os.path.abspath(file_path))
                                            print(f'file {real_name} on {df_list[real_name]} done (uid){uid}')
                                            is_done = True
                                            break
                    if not is_done:
                        for part in email_message.walk():
                            if part.get_content_maintype() != 'multipart':
                                if part.get('Content-Disposition') is None:
                                    # 尝试解析正文
                                    body = part.get_payload(decode=True)
                                    pos_start = body.find(b'<table')
                                    if pos_start != -1:
                                        end_tag = b'</table'
                                        pos_end = body.find(end_tag)
                                        try:
                                            df = pd.read_html(body[pos_start:pos_end+len(end_tag)], encoding='gbk')
                                        except Exception as e:
                                            print(f'got exception when read html (exception){e}')
                                        else:
                                            if df:
                                                df = df[0]
                                                subject = str(make_header(decode_header(email_message['Subject'])))
                                                fund_id = re.findall(r'S[A-Z0-9]{5}', subject, flags=re.ASCII)
                                                if fund_id and '产品代码' not in df.columns.array:
                                                    df['产品代码'] = fund_id[0]
                                                real_name = f"{subject}.xlsx"
                                                file_path = os.path.join(self._dump_dir, real_name)
                                                try:
                                                    df.to_excel(file_path, index=False)
                                                    df_list[real_name] = (uid, os.path.abspath(file_path))
                                                    print(f'content {real_name} on {df_list[real_name]} done (uid){uid}')
                                                except Exception as e:
                                                    pass
                M.close()
            return df_list
        except Exception as e:
            print(e)
            traceback.print_exc()


if __name__ == '__main__':
    try:
        email_data_dir = os.environ['SURFING_EMAIL_DATA_DIR']
        user_name = os.environ['SURFING_EMAIL_USER_NAME']
        password = os.environ['SURFING_EMAIL_PASSWORD']
    except KeyError as e:
        import sys
        sys.exit(f'can not found enough params in env (e){e}')

    mar = MailAttachmentRetriever(email_data_dir)
    print(mar.get_excels(IMAP_SPType.IMAP_QQ, user_name, password, 496))
