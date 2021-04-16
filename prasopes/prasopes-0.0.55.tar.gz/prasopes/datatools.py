from PyQt5 import QtWidgets
from PyQt5 import QtCore
import numpy as np
import os.path


def argsubselect(array, minimum, maximum):
    """finds arguments which fits into boundary conditions,
    if there is no fit, return nearest argument"""
    bounds = sorted([minimum, maximum])
    args = np.where((array >= bounds[0]) & (array <= bounds[1]))[0]
    if len(args) == 0:
        aver = (minimum+maximum)/2
        args = np.array([(np.abs(array - aver)).argmin()])
    return args


def argsubselect_2d(array1, min1, max1, array2, min2, max2):
    """finds arguments which fits into boundary conditions,
    if there is no fit, return nearest argument"""
    bounds1 = sorted([min1, max1])
    bounds2 = sorted([min2, max2])
    args = np.where((array1 >= bounds1[0]) & (array1 <= bounds1[1]) &
                    (array2 >= bounds2[0]) & (array2 <= bounds2[1]))[0]
    if len(args) == 0:
        # aver = (min1+max1)/2
        # args = np.array([(np.abs(array - aver)).argmin()])
        # TODO: FIXME!! THIS IS REALLY BAD!!
        args = [0]
    return args


def specttostr(augCanvas, delim=" ", names=["mass", "ion_count"],
               units=["m/z", ""], description=""):
    """converts spectrum to string"""
    lines = augCanvas.get_lines()
    formnames = delim.join([delim.join(names) for i in range(len(lines))])
    formunits = (delim).join([delim.join(units) for i in range(len(lines))])
    header = "\n".join([formnames, formunits, description])+"\n"

    strdata = []
    for i in range(np.max([len(line.get_xdata()) for line in lines])):
        pairs = [("{}"+delim+"{}").format(
                 line.get_xdata()[i], line.get_ydata()[i]) if
                 i < len(line.get_xdata()) else "--"+delim+"--"
                 for line in lines]
        strline = delim.join(pairs)+"\n"
        strdata.append(strline)
    strdata = "".join(strdata)
    return "{}{}".format(header, strdata)


def clip_spectstr(augCanvas):
    """clip converted spectrum to string"""
    description = ("{}_{:.4}-{:.4}_minutes_of_the_aquisition".format(
                   os.path.basename(augCanvas.ds.filename),
                   augCanvas.ds.mintime, augCanvas.ds.maxtime))
    string = specttostr(augCanvas.spectplot, delim="\t",
                        description=description)
    QtWidgets.QApplication.clipboard().clear()
    [QtWidgets.QApplication.clipboard().setText(string, i) for i in range(2)]


def clip_tablestr(augCanvas):
    """clip values from table"""
    pairs = [" ".join((augCanvas.paramstable.item(row, 1).text(),
                       augCanvas.paramstable.item(row, 2).text()))
             for row in range(augCanvas.paramstable.rowCount())
             if augCanvas.paramstable.cellWidget(row, 0).checkState()]
    text = ", ".join(pairs)
    QtWidgets.QApplication.clipboard().clear()
    [QtWidgets.QApplication.clipboard().setText(text, i) for i in range(2)]


def table(labels, minsizex=600, minsizey=0):
    """creates a reasonable table"""
    table = QtWidgets.QTableWidget(columnCount=len(labels))
    table.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                        QtWidgets.QSizePolicy.Expanding)
    table.setHorizontalHeaderLabels(labels)
    table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

    for n in range(table.columnCount()):
        table.horizontalHeader().setSectionResizeMode(
            n, QtWidgets.QHeaderView.Stretch)
    table.setMinimumSize(minsizex, minsizey)
    return table
