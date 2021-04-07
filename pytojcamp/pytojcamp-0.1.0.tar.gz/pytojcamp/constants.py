# -*- coding: utf-8 -*-
"""Some constant parts of JCAMP files"""

HEADER = """##TITLE={title}
##JCAMP-DX=4.24
##DATA TYPE={dataType}
##ORIGIN={origin}
##OWNER={owner}
##XUNITS={xUnits}
##YUNITS={yUnits}
##FIRSTX={firstX}
##LASTX={lastX}
##FIRSTY={firstY}
##LASTY={lastY}
##NPOINTS={points}\n"""

NTUPLE_HEADER = """##TITLE={title}
##JCAMP-DX=6.00
##DATA TYPE={dataType}
##ORIGIN={origin}
##OWNER={owner}\n"""

NTUPLE_PAGE_HEADER = """##VAR_NAME=  {varName}
##SYMBOL=    {symbol}
##VAR_TYPE=  {varType}
##VAR_DIM=   {varDim}
##UNITS=     {units}
"""

SYMBOL_LIST_NTUPLE = "##DATA TABLE= ({symbols}..{symbols}), PEAKS\n"


ADDITIONAL_META = "##${key}={value}\n"

END_STRING = "##END"
