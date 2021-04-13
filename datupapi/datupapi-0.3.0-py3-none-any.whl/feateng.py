import pandas as pd

from datupapi.extract.io import IO
from datupapi.feateng.scale import Scale


if __name__ == '__main__':
    io = IO(config_file='./config.yml', logfile='data_feateng', log_path='output/logs')
    scl = Scale(config_file='./config.yml', logfile='data_feateng', log_path='output/logs')

    io.logger.debug('Feature engineering starting...')
    df = io.download_csv(q_name='Qprep',
                         datalake_path='dev/ramiro/output/sales'
                         )
    seasons = []
    for ix, sku in enumerate(df.iloc[:,1:].columns):
        ts = df.iloc[:, ix + 1].values
        out = scl.extract_frequency(ts=ts, duration=4)
        seasons.append(out)
    print(seasons)
    #df = pd.DataFrame(data=data, index=range(0, len(data)), columns=['Age', 'PnL', 'Temp'])
    #df_out, _ = scl.scale_dataset(df, scaler='minmax')


