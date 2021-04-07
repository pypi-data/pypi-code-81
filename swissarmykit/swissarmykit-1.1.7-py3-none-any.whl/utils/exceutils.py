import os
import pandas as pd
import numpy as np


class ExcelUtils:

    def __init__(self):
        pass

    @staticmethod
    def compareFiles(file1, file2):
        if not os.path.exists(file1) or not os.path.exists(file2):
            raise Exception('File not exist')

        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)

        print('Same data: ', df1.equals(df2))


        # comparison_values = df1.values == df2.values
        # print (comparison_values)
        #
        # rows, cols = np.where(comparison_values == False)
        # for item in zip(rows, cols):
        #     df1.iloc[item[0], item[1]] = '{} --> {}'.format(df1.iloc[item[0], item[1]], df2.iloc[item[0], item[1]])
        #
        # df1.to_excel(file1 + '.diff.xlsx', index=False, header=True)
        #
        # print('INFO: Output diff: ', file1 + '.diff.xlsx')

if __name__ == '__main__':

    # base = 'C:/Users/Will/AppData/Local/Temp/'
    base = 'C:/Users/Will/Downloads/'
    file1 = base + 'Tax Detail Report 12-2020.xls'
    file2 = base +  'Tax Detail Report 12-2020(1).xls'
    ExcelUtils.compareFiles(file1, file2)

