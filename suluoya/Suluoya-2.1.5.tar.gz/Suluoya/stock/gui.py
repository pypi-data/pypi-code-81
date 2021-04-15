class StockGui(object):

    def __init__(self):
        import PySimpleGUI as sg
        import pretty_errors
        self.sg = sg
        self.sg.theme('BlueMono')
        layout = [
            [self.sg.Button('Markovitz Portfolio')],
            [self.sg.Button('Get Good Stocks')],
            [self.sg.Button('Get Stock Data')],
            [self.sg.Button('Get Stock Capacity')],
            [self.sg.Button('Stock Industry and Constituent Stock')],
            [self.sg.Button('Financial Statement')]
        ]
        self.window = self.sg.Window('Suluoya Stock', layout)
        self.event, self.values = self.window.read()

    def MarkovitzGui(self):

        layout = [
            [self.sg.Text('Start Date'), self.sg.Input('2019-01-01')],

            [self.sg.Text(' End Date'), self.sg.Input('2020-01-01')],

            [self.sg.Text('Frequency'),
                self.sg.Radio('day', 'Frequency', default=True),
                self.sg.Radio('week', 'Frequency', default=False),
                self.sg.Radio('month', 'Frequency', default=False)],

            [self.sg.Text('Stock List')],
            [self.sg.Multiline('贵州茅台\n隆基股份\n五粮液')],

            [self.sg.Text('Holiday Mode')],
            [self.sg.Radio('open', 'Holiday Mode', default=False),
             self.sg.Radio('close', 'Holiday Mode', default=True)],

            [self.sg.Text('Holiday Name')],
            [self.sg.Combo(['国庆节', '中秋节', '春节'], default_value='春节')],

            [self.sg.Text('before')],
            [self.sg.Input('-21')],

            [self.sg.Text('after')],
            [self.sg.Input('21')],

            [self.sg.Text('risk-free interest rate (annually)')],
            [self.sg.Input('0.0185')],

            [self.sg.Text('Calculate Mode')],
            [self.sg.Radio('iteration algorithm', 'Calculate Mode', default=True),
                self.sg.Radio('generate scatters', 'Calculate Mode', default=False), ],

            [self.sg.Text('Scatter Number')],
            [self.sg.Input('500')],

            [self.sg.Button('Start working!')],
        ]

        window = self.sg.Window('Suluoya Markovitz', layout)

        event, values = window.read()
        if event == 'Cancel' or event is None:
            window.close()
            return 'Quit'
        names = values[5].split('\n')[:-1]
        start_date = values[0]
        end_date = values[1]

        if values[2]:
            frequency = 'd'
        if values[3]:
            frequency = 'w'
        if values[4]:
            frequency = 'm'

        if values[6]:
            holiday = True
        if values[7]:
            holiday = False

        holiday_name = values[8]

        before = values[9]
        after = values[10]

        no_risk_rate = float(values[11])

        if values[12]:
            accurate = True
        if values[13]:
            accurate = False

        number = int(values[14])

        window.close()

        try:
            from .Markovitz import Markovitz
        except:
            from Markovitz import Markovitz

        Markovitz = Markovitz(names=names,
                              start_date=start_date,
                              end_date=end_date,
                              frequency=frequency,
                              holiday=holiday,
                              holiday_name=holiday_name,
                              before=before, after=after,
                              no_risk_rate=no_risk_rate
                              )
        print(Markovitz.portfolio(accurate=accurate, number=number))

    def MarkovitzWork(self):
        if self.event == 'Markovitz Portfolio':
            self.window.close()
            self.MarkovitzGui()

    def StockDataGui(self):
        layout = [
            [self.sg.Text('Start Date'), self.sg.Input(
                '2019-01-01', key='start_date')],

            [self.sg.Text(' End Date'), self.sg.Input(
                '2020-01-01', key='end_date')],

            [self.sg.Text('Frequency'),
                self.sg.Radio('day', 'Frequency', default=True, key='day'),
                self.sg.Radio('week', 'Frequency', default=False, key='week'),
                self.sg.Radio('month', 'Frequency', default=False, key='month')],

            [self.sg.Text('Stock List')],
            [self.sg.Multiline('贵州茅台\n隆基股份\n五粮液', key='stock_list')],

            [self.sg.Text('Holiday Mode')],
            [self.sg.Radio('open', 'Holiday Mode', default=False, key='open'),
             self.sg.Radio('close', 'Holiday Mode', default=True, key='close')],

            [self.sg.Text('Holiday Name')],
            [self.sg.Combo(['国庆节', '中秋节', '春节'],
                           default_value='春节', key='holiday')],

            [self.sg.Text('before')],
            [self.sg.Input('-21', key='before')],

            [self.sg.Text('after')],
            [self.sg.Input('21', key='after')],

            [self.sg.FolderBrowse('choose a folder to save data', key='path')],

            [self.sg.Button('Start working!')]
        ]
        window = self.sg.Window('Suluoya Stock Data', layout)
        event, values = window.read()
        if event == 'Cancel' or event is None:
            return 'Quit'
        window.close()
        start_date = values['start_date']
        end_date = values['end_date']
        if values['day']:
            frequency = 'd'
        if values['week']:
            frequency = 'w'
        if values['month']:
            frequency = 'm'
        stock_list = values['stock_list'].rstrip().split('\n')
        path = values['path']
        if path == '':
            raise ValueError('Please choose a folder to save data!')

        if values['close']:
            try:
                from .GetData import StockData
            except:
                from GetData import StockData
            StockData = StockData(names=stock_list,
                                  start_date=start_date, end_date=end_date,
                                  frequency=frequency)
            stock_pair, stock_data = StockData.stock_data[1:]
            StockData.quit()

        if values['open']:
            try:
                from .GetData import HolidayStockData
            except:
                from GetData import HolidayStockData
            holiday = values['holiday']
            before = values['before']
            after = values['after']
            HolidayStockData = HolidayStockData(names=stock_list,
                                                start_date=start_date,
                                                end_date=end_date,
                                                frequency=frequency,
                                                holiday=holiday,
                                                before=before,
                                                after=after)
            stock_pair, stock_data = HolidayStockData.HolidayNearbyData[1:]
        try:
            from ..log.SlyLog import sprint
        except:
            from log.SlyLog import sprint
        sprint = sprint()
        sprint.cyan('\n'+str(stock_pair))
        stock_data.to_excel(f'{path}\\stock_data.xlsx',
                            index=False, encoding='utf8')

    def StockDataWork(self):
        if self.event == 'Get Stock Data':
            self.window.close()
            self.StockDataGui()

    def StockCapacityGui(self):
        layout = [
            [self.sg.Text('Stock List')],
            [self.sg.Multiline('贵州茅台\n隆基股份\n五粮液', key='stock_list')],

            [self.sg.Text('        start                 end')],
            [self.sg.Text('  year    quater    year    quater')],
            [self.sg.Combo(values=[str(i) for i in range(2007, 2021)], default_value=2018, key='start_year'),
             self.sg.Combo(values=[str(i) for i in range(
                 1, 5)], default_value=1, key='start_quater'),
             self.sg.Combo(values=[str(i) for i in range(
                 2007, 2021)], default_value=2019, key='end_year'),
             self.sg.Combo(values=[str(i) for i in range(1, 5)], default_value=4, key='end_quater')],

            [self.sg.Text('choose capacities')],
            [self.sg.Checkbox('profit', default=True, key='profit'),
             self.sg.Checkbox('operation', default=True, key='operation'),
             self.sg.Checkbox('growth', default=True, key='growth'),
             self.sg.Checkbox('balance', default=True, key='balance'),
             self.sg.Checkbox('cash flow', default=True, key='cash'),
             self.sg.Checkbox('dupont', default=True, key='dupont'), ],

            [self.sg.FolderBrowse('choose a folder to save data', key='path')],

            [self.sg.Button('Start working!')]
        ]
        window = self.sg.Window('Suluoya Stock Capacity', layout)
        event, values = window.read()
        if event == 'Cancel' or event is None:
            window.close()
            return 'Quit'
        window.close()
        stock_list = values['stock_list'].rstrip().split('\n')
        start_year = int(values['start_year'])
        end_year = int(values['end_year'])
        start_quater = int(values['start_quater'])
        end_quater = int(values['end_quater'])
        path = values['path']
        if path == '':
            raise ValueError('Please choose a folder to save data!')
        try:
            from .GetData import StockAbility
        except:
            from GetData import StockAbility
        sa = StockAbility(names=stock_list,
                          start_year=start_year, start_quater=start_quater,
                          end_year=end_year, end_quater=end_quater)
        if values['profit'] and values['operation'] and values['growth'] and values['balance'] and values['cash'] and values['dupont']:
            sa.AllAbility.to_excel(f'{path}\\stock_capacity.xlsx',
                                   index=False, encoding='utf8')
        else:
            result_list = []
            if values['profit']:
                result_list.append(sa.profit)
            if values['operation']:
                result_list.append(sa.operation)
            if values['growth']:
                result_list.append(sa.growth)
            if values['balance']:
                result_list.append(sa.balance)
            if values['cash']:
                result_list.append(sa.cash_flow)
            if values['dupont']:
                result_list.append(sa.dupont_data)
            from pandas import merge
            if len(result_list) == 2:
                df = merge(result_list[0], result_list[1], how='outer', on=[
                    'code', 'name', 'year', 'quater', 'pubDate', 'statDate'])
            elif len(result_list) == 1:
                df = result_list[0]
            else:
                df = merge(result_list[0], result_list[1], how='outer', on=[
                    'code', 'name', 'year', 'quater', 'pubDate', 'statDate'])
                for i in result_list[2:]:
                    df = merge(df, i, how='outer', on=[
                        'code', 'name', 'year', 'quater', 'pubDate', 'statDate'])
            df.to_excel(f'{path}\\stock_capacity.xlsx',
                        index=False, encoding='utf8')

    def StockCapacityWork(self):
        if self.event == 'Get Stock Capacity':
            self.window.close()
            self.StockCapacityGui()

    def StockIndustryGui(self):
        layout = [
            [self.sg.FolderBrowse('choose a folder to save data', key='path')],
            [self.sg.Button('sz50'), self.sg.Button(
                'hs300'), self.sg.Button('zz500')],

            [self.sg.Text('Stock List')],
            [self.sg.Multiline('贵州茅台\n隆基股份\n五粮液', key='stock_list')],
            [self.sg.Button('Start working!')]
        ]
        window = self.sg.Window('Suluoya Stock Industry', layout)
        try:
            from .GetData import ConstituentStock
        except:
            from GetData import ConstituentStock

        cs = ConstituentStock(save=False)
        first = True
        while 1:
            try:
                event, values = window.read(timeout=10)
                path = values['path']
                if path == '':
                    continue
                if event == 'Cancel' or event is None:
                    window.close()
                    return 'Quit'
                elif event == 'sz50':
                    if not first:
                        try:
                            from ..log.SlyLog import sprint
                        except:
                            from log.SlyLog import sprint
                        sprint = sprint()
                        sprint.hide()
                        cs.bs.login()
                        sprint.show()
                    cs.sz50.to_excel(f'{path}\\sz50.xlsx',
                                     index=False, encoding='utf8')
                    print(f'save in {path}\\sz50.xlsx')
                    first = False
                elif event == 'hs300':
                    if not first:
                        try:
                            from ..log.SlyLog import sprint
                        except:
                            from log.SlyLog import sprint
                        sprint = sprint()
                        sprint.hide()
                        cs.bs.login()
                        sprint.show()
                    cs.sz50.to_excel(f'{path}\\hs300.xlsx',
                                     index=False, encoding='utf8')
                    print(f'save in {path}\\hs300.xlsx')
                    first = False
                elif event == 'zz500':
                    if not first:
                        try:
                            from ..log.SlyLog import sprint
                        except:
                            from log.SlyLog import sprint
                        sprint = sprint()
                        sprint.hide()
                        cs.bs.login()
                        sprint.show()
                    cs.sz50.to_excel(f'{path}\\zz500.xlsx',
                                     index=False, encoding='utf8')
                    print(f'save in {path}\\zz500.xlsx')
                    first = False
                elif event == 'Start working!':
                    if not first:
                        try:
                            from ..log.SlyLog import sprint
                        except:
                            from log.SlyLog import sprint
                        sprint = sprint()
                        sprint.hide()
                        cs.bs.login()
                        sprint.show()
                    df = cs.StockIndustry(
                        names=values['stock_list'].rstrip().split('\n'))
                    print(df)
                    df.to_excel(f'{path}\\industry.xlsx',
                                index=False, encoding='utf8')
                    print(f'\nsave in {path}\\industry.xlsx')
                    first = False
            except:
                window.close()
                break

    def StockIndustryWork(self):
        if self.event == 'Stock Industry and Constituent Stock':
            self.window.close()
            self.StockIndustryGui()

    def GoodStockGui(self):
        layout = [
            [self.sg.Text('page')],
            [self.sg.Combo(list(range(1, 21)), default_value=3, key='page')],
            [self.sg.FolderBrowse('choose a folder to save data', key='path')],
            [self.sg.Button('Start working!')],
        ]
        window = self.sg.Window('Suluoya Good Stocks', layout)
        event, values = window.read()
        if event == 'Cancel' or event is None:
            window.close()
            return 'Quit'
        window.close()
        path = values['path']
        if path == '':
            raise ValueError('Please choose a folder to save data!')
        page = int(values['page'])
        try:
            from .GetGoodStock import GetGoodStock
        except:
            from GetGoodStock import GetGoodStock
        df = GetGoodStock(page=page)
        df.to_excel(f'{path}\\good_stocks.xlsx', encoding='utf8')

    def GoodStockWork(self):
        if self.event == 'Get Good Stocks':
            self.window.close()
            self.GoodStockGui()

    def FinancialStatementsGui(self):
        layout = [
            [self.sg.Text('Stock List')],
            [self.sg.Multiline('贵州茅台\n隆基股份\n五粮液', key='stock_list')],

            [self.sg.Text('        start                 end')],
            [self.sg.Text('  year    quater    year    quater')],
            [self.sg.Combo(values=[str(i) for i in range(2011, 2020)], default_value=2018, key='start_year'),
             self.sg.Combo(values=[str(i) for i in range(
                 1, 5)], default_value=1, key='start_quater'),
             self.sg.Combo(values=[str(i) for i in range(
                 2011, 2020)], default_value=2019, key='end_year'),
             self.sg.Combo(values=[str(i) for i in range(1, 5)], default_value=4, key='end_quater')],

            [self.sg.FolderBrowse('choose a folder to save data', key='path')],

            [self.sg.Button('cash flow'), self.sg.Button(
                'balance'), self.sg.Button('profit')],
        ]
        window = self.sg.Window('Suluoya Stock Capacity', layout)
        event, values = window.read()
        if event == 'Cancel' or event is None:
            window.close()
            return 'Quit'
        window.close()
        path = values['path']
        if path == '':
            raise ValueError('Please choose a folder to save data!')
        start_year = int(values['start_year'])
        end_year = int(values['end_year'])
        start_quater = int(values['start_quater'])
        end_quater = int(values['end_quater'])
        stock_list = values['stock_list'].rstrip().split('\n')
        try:
            from .FinancialStatement import FinancialStatements
        except:
            from FinancialStatement import FinancialStatements

        fc = FinancialStatements(names=stock_list,
                                 start_year=start_year, start_quater=start_quater,
                                 end_year=end_year, end_quater=end_quater)
        if event == 'cash flow':
            df = fc.statement(mode='现金流量表')
        elif event == 'balance':
            df = fc.statement(mode='资产负债表')
        elif event == 'profit':
            df = fc.statement(mode='利润表')
        df.to_excel(f'path\\{event}-{stock_list}--{start_year}.{start_quater}-{end_year}.{end_quater}.xlsx',
                    encoding='utf8', index=False)

    def FinancialStatementsWork(self):
        if self.event == 'Financial Statement':
            self.window.close()
            self.FinancialStatementsGui()


def gui():
    """stock gui
    """
    sg = StockGui()
    while 1:
        a = sg.MarkovitzWork()
        c = sg.StockCapacityWork()
        b = sg.StockDataWork()
        d = sg.StockIndustryWork()
        e = sg.GoodStockWork()
        f = sg.FinancialStatementsWork()
        if a == None and b == None and c == None and d == None and e == None and f == None:
            break


if __name__ == '__main__':
    gui()
