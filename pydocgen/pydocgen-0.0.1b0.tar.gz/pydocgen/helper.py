import csv
import xlrd
class Helper():
    @staticmethod
    def read_xlsx(filepath, sheet_name='Sheet0'):
        '''
        Function used to read data from an excel workbook.

        Parameters
        ----------
        filepath: str
            String pointing to the xlsx file that needs to be read.
        sheet_name: str
            Name of the sheet to read data from.
            Default='Sheet0'

        Returns
        -------
        data: list
            A list of rows read from the xlsx file.
        '''
        book = xlrd.open_workbook(filepath)
        sheet = book.sheet_by_name(sheet_name)
        data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
        return data

    @staticmethod
    def write_csv(row, filepath):
        '''
        Functions used to write rows into a csv file.

        Parameters
        ----------
        rows: List
            List of rows to be written into a csv file.
            
        Returns
        -------
        None
            File created successfully.
        '''
        with open(filepath, 'a+', newline='', encoding='utf-8') as csv_file:
            csv.writer(csv_file).writerow(row)