import csv
from .frame import ColumnarFrame


def read_csv(filename):
    with open(filename) as f:
        csvdata = csv.reader(f, delimiter=',')

    rit = iter(csvdata)
    header = next(rit)

    data = {key: [] for key in header}
    for row in rit:
        for key, value in zip(header, row):
            data[key].append(value)

    return ColumnarFrame(data)
