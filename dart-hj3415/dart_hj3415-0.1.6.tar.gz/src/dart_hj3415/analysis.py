import os
import time
import requests
import pickle
import re
import datetime
import pandas as pd
from . import subjects, dart
from krx_hj3415 import krx
from noti_hj3415 import telegram
from telegram.error import TimedOut

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.ERROR)


class Pickle:
    FILENAME = 'rno_anal_noti.pickle'
    FULL_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), FILENAME)

    @staticmethod
    def save(obj: dict):
        p = re.compile('^20[0-9][0-9][0,1][0-9][0-3][0-9]$')
        if p.match(obj['date']) is None:
            print(f"Invalid date - {obj['date']}(YYYYMMDD)")
            raise Exception
        logger.info(f'Save to pickle : {obj}')
        with open(Pickle.FULL_PATH, "wb") as fw:
            pickle.dump(obj, fw)

    @staticmethod
    def init(date: str):
        p = re.compile('^20[0-9][0-9][0,1][0-9][0-3][0-9]$')
        if p.match(date) is None:
            print(f'Invalid date - {date}(YYYYMMDD)')
            raise Exception
        logger.info(f'init {Pickle.FULL_PATH}')
        with open(Pickle.FULL_PATH, "wb") as fw:
            pickle.dump({'date': date, 'notified': [], 'analysed': []}, fw)

    @staticmethod
    def load() -> dict:
        try:
            with open(Pickle.FULL_PATH, "rb") as fr:
                obj = pickle.load(fr)
                logger.info(f'Load from pickle : {obj}')
                return obj
        except (EOFError, FileNotFoundError) as e:
            logger.error(e)
            Pickle.init(datetime.datetime.today().strftime('%Y%m%d'))
            with open(Pickle.FULL_PATH, "rb") as fr:
                obj = pickle.load(fr)
                logger.info(f'Load from pickle : {obj}')
                return obj


pretested_subject = ('주식분할결정', '주식병합결정', '주식등의대량보유상황보고서', '자기주식처분결정', '공개매수신고서',
                     '전환사채권발행결정', '신주인수권부사채권발행결정', '교환사채권발행결정', '만기전사채취득',
                     '신주인수권행사', '소송등의', '주식배당결정', '주주총회소집결의', '회사합병결정', '회사분할결정',
                     '자산재평가실시결정')
available_subject = ('특정증권등소유상황보고서', '주식등의대량보유상황보고서', '유상증자결정',
                     '현물배당결정', '매출액또는손익구조',  '주식소각결정')
enabled_subject = ('공급계약체결', '무상증자결정', '자기주식취득결정')


def run_all_subject(edate: str):
    """
    edate 날짜에 해당하는 dataframe을 얻어서 enabled_subject에 해당하는 타이틀을 분석하여\n
    기준을 넘으면 yield_rno_anal_noti_for_one_subject() 함수에서 텔레그램으로 노티하고\n
    yield된 형식 딕셔너리를 통해 피클에 저장한다.
    :param edate: %Y%m%d형식의 문자열
    """
    def islive_opendart() -> bool:
        url = 'https://opendart.fss.or.kr/api/list.json'
        key = '?crtfc_key=f803f1263b3513026231f4eff69312165e6eda90'
        first_url = url + key
        try:
            r = requests.get(first_url, timeout=3).json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            logger.error(e)
            return False
        return True

    def convert_df_to_intro_dicts_list(df: pd.DataFrame) -> list:
        """
        데이터프레임을 intro 딕셔너리를 포함하는 리스트로 변환한다.
        :param df: 온라인또는 이미저장된 데이터베이스에서 얻는 데이터프레임
        :return: df를 변환하여 얻은 intro 딕셔너리를 포함하는 리스트
        """
        logger.info('<<<  convert_dart_df_to_intro_dicts_lists() start >>>')
        intro_dicts = []
        for i, namedtuple in enumerate(df.itertuples()):
            intro_dicts.append(subjects.make_intro(namedtuple))
        logger.info(intro_dicts)
        return intro_dicts

    def yield_rno_anal_noti_for_one_subject(subject: str, intros: list):
        """
        intros 리스트에서 각각의 intro 딕셔너리를 분석하여 (with subject.run_one_subject())\n
        분석 결과를 통해 텔레그램으로 고지할지를 결정하고 return 딕셔너리를 yield하여 상위 함수에서 피클로 저장할수 있다록 한다.\n
        <<dict.keys>>\n
        from namedtuple - 'code', 'name', 'rtitle', 'rno', 'rdt', 'url'\n
        from c101 - 'price', 'per', 'pbr', 'high_52w', 'low_52w'\n
        :param subject: subjects.py에서 구현된 각각의 클래스 제목에 해당하는 문자열
        :param intros: df를 변환하여 얻은 intro 딕셔너리를 포함하는 리스트
        :return: yield 형식 {'rno': 리포트번호, 'is_analysed': bool, 'is_notified': bool}
        """
        logger.info('<<<  analyse_and_yield_one_subject() start >>>')
        total_items = len(intros)
        krx_all = krx.get_codes()

        for i, intro_dict in enumerate(intros):
            print(f"{i + 1}/{total_items}. code: {intro_dict['code']}\tname: {intro_dict['name']}")
            if intro_dict['code'] not in krx_all:
                # 아직 코드가 krx에 없는 경우는 넘어간다.
                print(f"\t{intro_dict['code']} {intro_dict['name']}is not registered in corp db yet..")
                time.sleep(.5)
                yield {'rno': intro_dict['rno'], 'is_analysed': True, 'is_notified': False}
            elif intro_dict['rno'] in pickle_data['analysed']:
                # 이전에 이미 분석된 경우는 넘어감
                print(f"\t<{intro_dict['rno']}> already analysed")
                time.sleep(.5)
                continue
            else:
                subject_cls = subjects.run_one_subject(subject=subject, intro=intro_dict)
                return_dict = {'rno': intro_dict['rno'], 'is_analysed': True, 'is_notified': False}
                # print(subject_cls)
                if subject_cls.point >= subjects.DartSubject.NOTI_POINT:
                    if intro_dict['rno'] in pickle_data['notified']:
                        print(f"We caught the important report but already notified..{intro_dict['rno']}")
                    else:
                        print(f"We caught the important report..{intro_dict['rno']}")
                        try:
                            telegram.dart_bot(str(subject_cls))
                        except TimedOut:
                            time.sleep(3)
                            print(f'Telegram does not respond, retrying...')
                            telegram.dart_bot(str(subject_cls))
                        finally:
                            return_dict['is_notified'] = True
                yield return_dict

    logger.info('<<< run_all_titles() >>>')
    if not islive_opendart():
        print("Connection Error on opendart.fss.or.kr..")
        telegram.dart_bot("Connection Error on opendart.fss.or.kr..")
        return

    p = re.compile('^20[0-9][0-9][0,1][0-9][0-3][0-9]$')
    if p.match(edate) is None:
        print(f"Invalid date - {edate}(YYYYMMDD)")
        raise Exception

    pickle_data = Pickle.load()  # {'date': '20201010', 'notified': [rno..], 'analysed': [rno..]}
    if pickle_data['date'] != edate:
        Pickle.init(edate)
        pickle_data = Pickle.load()

    print(f'Titles - {enabled_subject}')

    print('*' * 40, 'Dart analysis all titles', '*' * 40)
    for subject in enabled_subject:
        df = dart.get_df_from_online(edate=edate, title=subject)
        for rno_anal_noti in yield_rno_anal_noti_for_one_subject(subject=subject,
                                                                 intros=convert_df_to_intro_dicts_list(df)):
            if rno_anal_noti['is_analysed']:
                pickle_data['analysed'].append(rno_anal_noti['rno'])
            if rno_anal_noti['is_notified']:
                pickle_data['notified'].append(rno_anal_noti['rno'])
        Pickle.save(pickle_data)  # 한 타이틀이 끝나면 저장한다.
        time.sleep(1)

