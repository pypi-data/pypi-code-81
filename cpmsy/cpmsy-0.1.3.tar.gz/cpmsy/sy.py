import numpy as np
def Mapper(data, data1, srcMp):
    dataz = data[data[:, 2].argsort()]
    datay = data[data[:, 1].argsort()]
    datax = data[data[:, 0].argsort()]
    dataxLen = datax[10499][0] - datax[0][0]
    datayLen = datay[10499][1] - datay[0][1]
    datazLen = dataz[10499][2] - dataz[0][2]

    p = np.array(srcMp)
    print(p)
    pxlen = p[0] - datax[0][0]
    pylen = p[1] - datay[0][1]
    pzlen = p[2] - dataz[0][2]
    xpd = pxlen / dataxLen
    ypd = pylen / datayLen
    zpd = pzlen / datazLen

    data1z = data1[data1[:, 2].argsort()]
    data1y = data1[data1[:, 1].argsort()]
    data1x = data1[data1[:, 0].argsort()]
    data1xLen = data1x[10119][0] - data1x[0][0]
    data1yLen = data1y[10119][1] - data1y[0][1]
    data1zLen = data1z[10119][2] - data1z[0][2]
    rx = data1xLen * xpd + data1x[0][0]
    ry = data1yLen * ypd + data1y[0][1]
    rz = data1zLen * zpd + data1z[0][2]
    p=np.array([rx,ry,rz])
    return p


