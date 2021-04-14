import time
from datupapi.extract.io import IO

if __name__ == '__main__':

    io = IO(config_file='./config.yml', logfile='data_io', log_path='output/logs')

    io.logger.debug('Data extraction starting...')
    df_xls = io.download_excel(q_name='Base de Datos CNCH.xlsx',
                               sheet_name='Venta 2017-2020',
                               datalake_path='dev/santiago/as-is',
                               types={'Mes': str, 'Semana': str})
    io.upload_csv(df_xls,
                  q_name='Qraw',
                  datalake_path='dev/ramiro/output/sales')
    io.logger.debug('Data extraction completed...')
    io.upload_log()