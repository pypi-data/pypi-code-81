from hbshare.asset_allocation.marco import TradingCRNCalculator


def update_job():
    # today = datetime.datetime.today().strftime('%Y%m%d')
    today = '20210415'
    # 更新数据
    TradingCRNCalculator(today, today).get_construct_result()


if __name__ == '__main__':
    update_job()
