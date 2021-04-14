import pandas as pd

from datupapi.extract.io import IO
from datupapi.transform.ranking import Ranking


if __name__ == '__main__':
    io = IO(config_file='./config.yml', logfile='data_ranking', log_path='output/logs')
    rnkg = Ranking(config_file='./config.yml', logfile='data_ranking', log_path='output/logs')

    io.logger.debug('Items transform starting...')
    df = io.download_csv(q_name='Qprep',
                         datalake_path='dev/ramiro/output/sales'
                         ).set_index('Fecha')

    df_abc = rnkg.rank_abc(df, sku_col='Codigo Material', rank_col='Venta Neta Cop', threshold=[.8, .95])
    df_fsn = rnkg.rank_fsn(df, sku_col='Codigo Material', rank_col='Venta Neta Kilos', threshold=[.8, .5])
    df_xyz = rnkg.rank_xyz(df, sku_col='Codigo Material', rank_col='Venta Neta Kilos', threshold=[.25, .75])
    df_afx = rnkg.concat_ranking(df_abc, df_fsn, df_xyz, sku_col='Codigo Material')
    print(df_abc['ABC'].value_counts())
    print(df_fsn['FSN'].value_counts())
    print(df_xyz['XYZ'].value_counts())
    print(df_afx['Ranking'].value_counts())
    io.upload_csv(df_afx, q_name='Qrank', datalake_path='dev/ramiro/output/sales')


