from .config import *
from openpyxl import load_workbook

def double_check_sheet(projdir):
    """
    """
    #string variables
    sheetsdir      = projdir + 'Spreadsheets/'
    xlsx           = '.xlsx'
    hes            = 'Hessian'

    for specie in species:
        if os.path.isfile(sheetsdir + specie + xlsx):
            df  = pd.read_excel(sheetsdir + specie + xlsx, index_col=0,
                               sheet_name=hes, header=6)
                               
    return
