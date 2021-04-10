"""
edata means 'easy data', is a wrapper of csv, xlrd, xlwt, pylightxl.
edata can be used to read csv, xls, xlsx format file as dict list data and write dict list data to those format file.
"""
import csv
import os

import pylightxl as xl
import xlrd
import xlwt


def read(filename, sheet_index=0, delimiter=','):
    """
    read file as dict list

    :param filename: file name
    :param sheet_index: sheet index only for Excel file
    :param delimiter: delimiter only for csv file
    :return: dict list, format：[{...}, {...}]
    """
    # parse file ext
    _, ext = os.path.splitext(filename)
    if ext == '.xls':
        return _read_xls(filename, sheet_index)
    if ext == '.xlsx' or ext == '.xlsm':
        return _read_xlsx(filename, sheet_index)
    if ext == '.csv':
        return _read_csv(filename, delimiter=delimiter)
    else:
        raise Exception('file format not supported!')


def write(filename, dict_list, delimiter=','):
    """
    write dict list to Excel file

    :param filename: Excel file name
    :param dict_list: dict list, format:[{...},{...}]
    :param delimiter: only for csv file
    :return:
    """
    if not dict_list:
        raise Exception('no data to write!')
    # parse file ext
    _, ext = os.path.splitext(filename)
    if ext == '.xls':
        return _write_xls(filename, dict_list)
    if ext == '.xlsx' or ext == '.xlsm':
        return _write_xlsx(filename, dict_list)
    if ext == '.csv':
        return _write_csv(filename, dict_list, delimiter)
    else:
        raise Exception('file format not supported!')


def get_sheet_names(filename):
    """
    get Excel sheet name list

    :param filename: Excel file name
    :return: sheet name list
    """
    _, ext = os.path.splitext(filename)
    if ext == '.xls':
        return xlrd.open_workbook(filename).sheet_names()
    if ext == '.xlsx' or ext == '.xlsm':
        return xl.readxl(fn=filename).ws_names
    else:
        raise Exception('file format not supported!')


def _get_real_value(value):
    """
    get real cell value

    :param value: cell value
    :return: real value
    """
    if type(value) is float:
        if value % 1 == 0:
            return int(value)
    return value


def _read_xls(filename, sheet_index=0):
    """
    read Excel file with suffix .xls

    :param filename: Excel file name
    :param sheet_index: Excel sheet index
    :return dict list, format：[{...}, {...}]
    """
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_by_index(sheet_index)
    header = sheet.row_values(0)
    rows = []
    for r in range(1, sheet.nrows):
        row_values = sheet.row_values(r)
        row_dict = {}
        for c in range(sheet.ncols):
            cell_value = _get_real_value(row_values[c])
            row_dict[header[c]] = cell_value
        rows.append(row_dict)
    return rows


def _read_xlsx(filename, sheet_index=0):
    """
    read Excel file with suffix .xlsx

    :param filename: Excel file name
    :param sheet_index: Excel sheet index
    :return dict list, format：[{...}, {...}]
    """
    db = xl.readxl(fn=filename)
    if sheet_index < 0 or sheet_index >= len(db.ws_names):
        raise Exception('please make sure: 0 <= sheet_index < %s' % len(db.ws_names))

    data = []
    header = None
    for i, row in enumerate(db.ws(ws=db.ws_names[sheet_index]).rows):
        if i == 0:
            header = row
            continue
        data.append(dict(zip(header, row)))

    return data


def _read_csv(filename, delimiter=','):
    """
    read csv file

    :param filename: csv file name
    :param delimiter: delimiter
    :return dict list, format：[{...}, {...}]
    """
    with open(filename, mode='r') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=delimiter)
        return list(reader)


def _write_xls(filename, dict_list):
    """
    write data to Excel file with suffix .xls

    :param filename: Excel file name
    :param dict_list: dict list，format：[{...},{...}]
    """
    if len(dict_list) > 65535:
        raise ValueError('.xls format rows limit is 65535')
    workbook = xlwt.Workbook(encoding='utf-8')
    # create sheet
    worksheet = workbook.add_sheet('Sheet1')
    # write header
    header = dict_list[0].keys()
    for col_index, field_name in enumerate(header):
        worksheet.write(0, col_index, label=field_name)
    # write data
    for row_index, row in enumerate(dict_list):
        for col_index, field_name in enumerate(header):
            worksheet.write(row_index + 1, col_index, label=row.get(field_name, ''))
    # save file
    workbook.save(filename)


def _write_xlsx(filename, dict_list):
    """
    write data to Excel file with suffix .xlsx

    :param filename: Excel file name
    :param dict_list: dict list，format：[{...},{...}]
    """
    db = xl.Database()
    db.add_ws(ws="Sheet1")
    sheet = db.ws(ws="Sheet1")
    # write header to the worksheet
    header = dict_list[0].keys()
    for column_number, column_name in enumerate(header, start=1):
        sheet.update_index(row=1, col=column_number, val=column_name)
    # add data to the worksheet
    for row_number, row_data in enumerate(dict_list, start=2):
        for column_number, column_name in enumerate(header, start=1):
            sheet.update_index(row=row_number, col=column_number, val=row_data.get(column_name))

    # write out the db
    xl.writexl(db=db, fn=filename)


def _write_csv(filename, dict_list, delimiter=','):
    """
    write data to csv file

    :param filename: csv file name
    :param delimiter: delimiter
    :param dict_list: dict list，format：[{...},{...}]
    """
    with open(filename, mode='w') as csv_file:
        fieldnames = dict_list[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(dict_list)
