#获取ppm
def get_ppm(pfm_ ):
    ppm = []
    for k in pfm_:
        ppm.append(k)
    for i in range(len(ppm)):
        for j in range(len(ppm[i][0])):
            a = ppm[i][0][j] / (ppm[i][0][j] + ppm[i][1][j] +
                                ppm[i][2][j] + ppm[i][3][j])
            b = ppm[i][1][j] / (ppm[i][0][j] + ppm[i][1][j] +
                                ppm[i][2][j] + ppm[i][3][j])
            c = ppm[i][2][j] / (ppm[i][0][j] + ppm[i][1][j] +
                                ppm[i][2][j] + ppm[i][3][j])
            d = ppm[i][3][j] / (ppm[i][0][j] + ppm[i][1][j] +
                                ppm[i][2][j] + ppm[i][3][j])
            
            ppm[i][0][j] = a
            ppm[i][1][j] = b
            ppm[i][2][j] = c
            ppm[i][3][j] = d
    return ppm