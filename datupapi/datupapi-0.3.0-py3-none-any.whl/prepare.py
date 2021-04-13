from datupapi.extract.io import IO
from datupapi.prepare.cleanse import Cleanse
from datupapi.prepare.format import Format

import time

if __name__ == '__main__':
    io = IO(config_file='./config.yml', logfile='data_prepare', log_path='output/logs')
    clns = Cleanse(config_file='./config.yml', logfile='data_prepare', log_path='output/logs')
    fmt = Format(config_file='./config.yml', logfile='data_prepare', log_path='output/logs')

    io.logger.debug('Data preparation starting...')
    df = io.download_csv(q_name='Qraw',
                         datalake_path='dev/ramiro/output/sales',
                         types={'Mes': str, 'Semana': str})
    df = clns.clean_metadata(df)
    df = fmt.parse_week_to_date(df,
                                week_col='Semana',
                                date_col='Fecha',
                                drop_cols=['Mes'])
    df = fmt.pivot_dates_vs_sku(df,
                                date_col='Fecha',
                                sku_col='Codigo Material',
                                qty_col='Venta Neta Kilos')
    df = df.applymap(lambda x: 0 if x < 0 else x) # Replace negative values by 0
    df = df.reset_index(drop=False)
    #io.upload_dynamodb(df, table_name='Qprep-sample', tenant_id='cnch', sort_col='Fecha')
    #items = io.download_dynamodb(table_name='Qprep-sample', tenant_id='cnch')
    io.upload_csv(df, q_name='Qprep', datalake_path='dev/ramiro/output/sales')
    #io.logger.debug('Data preparation completed...')
    #io.upload_log()
