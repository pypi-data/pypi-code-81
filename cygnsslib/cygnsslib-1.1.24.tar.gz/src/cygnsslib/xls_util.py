try:
    from xlutils.copy import copy as sheet_copy
    import xlrd
except ImportError:
    pass
import numpy as np
import os

"""
NOTE: This is only left for compatibility with old versions, no update will be done to this code. 
use Pandas instead of this 
"""


def convert_data(value):
    if type(value) == np.ndarray:
        value = value.tolist()
    if type(value) in (complex, np.complex_, np.complex128, np.complex64):
        value = complex(value)
    if type(value) in (np.float_, np.float32):
        value = float(value)
    if type(value) in (np.int64, np.int32, np.int_, np.int8):
        value = int(value)
    if type(value) in (bool, np.bool_):
        value = 1 if value else 0
    return value


def write_row_existing_xls(xls_file_path, data, row_idx=-1, col_offset=0, sheet_id=0):
    """
    write a row in an existing xls file

    :param xls_file_path: xls file path
    :type xls_file_path: str
    :param data: data in an np.array or list
    :type data: list or np.array
    :param row_idx: row index, select -1 for adding a new row
    :type row_idx: int
    :param col_offset: number of column offset
    :type col_offset: int
    :param sheet_id: sheet index, default 0 (the first one)
    :type sheet_id: int
    :return: void
    """
    if not os.path.isfile(xls_file_path):
        raise FileExistsError(f'xls file not exist in path {xls_file_path}')
    rb = xlrd.open_workbook(xls_file_path, formatting_info=True)
    r_sheet = rb.sheet_by_index(sheet_id)
    row = r_sheet.nrows
    wb = sheet_copy(rb)
    sheet = wb.get_sheet(0)
    if row_idx == -1:
        row_idx = row
    write_xls_row(sheet, data, row_idx, col_offset=col_offset)
    wb.save(xls_file_path)


def write_xls_row(sheet, data, row, col_offset=0):
    """
    write a row in an xls sheet

    :param sheet: sheet object
    :type sheet: xlrd.Sheet
    :param data: data in an np.array or list
    :type data: list or np.array
    :param row: row index
    :type row: int
    :param col_offset: number of column offset
    :type col_offset: int
    :return: void
    """

    for col, col_val in enumerate(data):
        sheet.write(row, col + col_offset, convert_data(col_val))


def find_col_header(text, header):
    """

    find the col idx from the header, if multiple idx found it'll return a list, if none was found it'll return None

    :param text: header text
    :type text: str
    :param header: header list
    :type header: list
    :return: col idx
    :rtype int or None
    """

    out_idx = list()
    for idx, value in enumerate(header):
        if text == value:
            out_idx.append(idx)
    if len(out_idx) < 1:
        out_idx = None
    elif len(out_idx) < 2:
        out_idx = out_idx[0]
    return out_idx


def write_col_existing_xls(xls_file_path, data, col_idx=-1, row_offset=0, sheet_id=0):
    """
    write a row in an existing xls file

    :param xls_file_path: xls file path
    :type xls_file_path: str
    :param data: data in an np.array or list
    :type data: list or np.array
    :param col_idx: column index, select -1 for adding a new column
    :type col_idx: int
    :param row_offset: number of row offset
    :type row_offset: int
    :param sheet_id: sheet index, default 0 (the first one)
    :type sheet_id: int
    :return: void
    """
    if not os.path.isfile(xls_file_path):
        raise FileExistsError(f'xls file not exist in path {xls_file_path}')

    rb = xlrd.open_workbook(xls_file_path, formatting_info=True)
    r_sheet = rb.sheet_by_index(sheet_id)
    col = r_sheet.ncols
    wb = sheet_copy(rb)
    sheet = wb.get_sheet(0)
    if col_idx == -1:
        col_idx = col
    write_xls_col(sheet, data, col_idx, row_offset=row_offset)
    wb.save(xls_file_path)


def write_xls_col(sheet, data, col, row_offset=0):
    """
    write a column in an xls sheet

    :param sheet: sheet object
    :type sheet: xlrd.Sheet
    :param data: data in an np.array or list
    :type data: list or np.array
    :param col: column index
    :type col: int
    :param row_offset: number of row offset
    :type row_offset: int
    :return: void
    """

    for row, row_val in enumerate(data):
        sheet.write(row + row_offset, col, convert_data(row_val))
