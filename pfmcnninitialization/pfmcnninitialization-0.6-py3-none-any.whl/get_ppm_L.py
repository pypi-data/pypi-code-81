import numpy as np

import pandas as pd
#获得一组定长的ppm
def get_ppm_L(ppm,L_ = 8):
    ppm_L = []
    num_drop = 0
    num_L = 0
    f = lambda x: compute_Information_entropy(x)
    for i in ppm:
        #如果长度小于指定值
        if len(i[0])<L_:
            num_drop+=1
        #恰好等于全部的保留
        elif  len(i[0])==L_:
            ppm_L.append(i)
            num_L+=1
        #大于的情况，保留信息熵最大的L-mer
        else:
            min_Information_entropy = 2 
            final_number = 0
            for j in range(0,len(i)-L_):
                if  np.sum([f(a) for a in i.T[j:j+L_]])<min_Information_entropy:
                    min_Information_entropy = np.sum([f(a) for a in i.T[j:j+L_]])
                    final_number = j
                else:
                    pass
            ppm_L.append(i[:,final_number:final_number+L_])
    print(str(num_drop)+ ' PFMs with lengths less than the specified length have been screened out.')
    print( 'All '+str(num_L) + ' PFMs of length exactly equal to the specified length are retained.')
    print('For PFMs with lengths greater than the specified length, the segment with the highest information entropy is intercepted.')
    return ppm_L