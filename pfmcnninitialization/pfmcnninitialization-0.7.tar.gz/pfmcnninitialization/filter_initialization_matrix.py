import numpy as np
import wget
import pandas as pd
from random import randint, sample

#获取pfm
def get_pfm(taxonomic_groups=str('plants'),data_local = None):
    if data_local == None:
        if taxonomic_groups=='plants':
            DATA_URL = 'http://jaspar.genereg.net/download/CORE/JASPAR2020_CORE_plants_non-redundant_pfms_jaspar.txt'
            out_fname='./plants.txt'
            wget.download(DATA_URL, out=out_fname)
            pre_pfm = pd.read_csv('./plants.txt',
                          sep='\t',
                          header=None)
            
        elif taxonomic_groups=='fungi':
            DATA_URL = 'http://jaspar.genereg.net/download/CORE/JASPAR2020_CORE_fungi_non-redundant_pfms_jaspar.txt'
            out_fname='./plants.txt'
            wget.download(DATA_URL, out=out_fname)
            pre_pfm = pd.read_csv('./plants.txt',
                          sep='\t',
                          header=None)
        
        elif taxonomic_groups=='vertebrates':
            DATA_URL = 'http://jaspar.genereg.net/download/CORE/JASPAR2020_CORE_vertebrates_non-redundant_pfms_jaspar.txt'
            out_fname='./plants.txt'
            wget.download(DATA_URL, out=out_fname)
            pre_pfm = pd.read_csv('./plants.txt',
                          sep='\t',
                          header=None)
        
        elif taxonomic_groups=='insects':
            DATA_URL = 'http://jaspar.genereg.net/download/CORE/JASPAR2020_CORE_insects_non-redundant_pfms_jaspar.txt'
            out_fname='./plants.txt'
            wget.download(DATA_URL, out=out_fname)
            pre_pfm = pd.read_csv('./plants.txt',
                          sep='\t',
                          header=None)
            
            
    else:
        #接收从JASPAR下载的文件作为输入
        pre_pfm = pd.read_csv(str(data_local),
                          sep='\t',
                          header=None)
    pfm = []
    for i in range(0,len(pre_pfm),5):
        pfm_sample = []
        for j in range(i+1,i+5):
            str_pfm = pre_pfm.iloc[j,0][4:-1].strip().split()
            int_pfm = [int(k) for k in str_pfm]
            pfm_sample.append(np.array(int_pfm))
        pfm.append(np.array(pfm_sample).astype('float32'))
    #返回记录有多个pfm数组的列表，每个pfm数组的shape均为4*L(L为长度)
    print('There are '+str(len(pfm))+ ' PFMs '+str('!'))
    print('You need to consider whether the number of CNN filters you use is suitable for this initialization method.')
    return pfm


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

#计算信息熵，越小越好;注意，这里加了1e-5，防止0的影响
def compute_Information_entropy(acgt):
    return -1*np.sum(np.log2(np.array(acgt)+1e-5)* (np.array(acgt)+1e-5))

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

#获得一组定长的ppm，每个值-0.5，均值近0
def get_ppm_rp25_L(ppm,L_ = 8):
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
            ppm_L.append(i-0.25)
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
            ppm_L.append(i[:,final_number:final_number+L_]-0.25)
    print(str(num_drop)+ ' PFMs with lengths less than the specified length have been screened out.')
    print( 'All '+str(num_L) + ' PFMs of length exactly equal to the specified length are retained.')
    print('For PFMs with lengths greater than the specified length, the segment with the highest information entropy is intercepted.')
    return ppm_L
def get_pwm(ppm_L,background_acgt = [0.25,0.25,0.25,0.25]):
    pwm_L = []
    for i in range(len(ppm_L)):
        pwm_L_sample = []
        for j in range(4):
            #这里加1e-3是防止结果中出现0
            #这里的问题在于，正向最多到2，而负向可以到-inf（很大的负数）
            #考虑如何改，或者直接用ppm？
            #这会有一些问题哦——————
            pwm_L_sample.append(list(np.log2((ppm_L[i][j]+1e-2)/background_acgt[j])))
        pwm_L.append(np.array(pwm_L_sample))
    return np.array(pwm_L) 


def filter_initialization_matrix(taxonomic_groups='plants',data_local = None,
                                 filters=64,
                                 L_=8,
                                 pattern='ppm_rp25',
                                 background_acgt=[0.25, 0.25, 0.25, 0.25]):
    print('Note that the base order in the return result matrix is ACGT')
    #只有pwm模式，需要background_acgt
    if pattern == 'ppm_rp25':
        print(
            'You will get the PPM_R25 matrix((the value of each position of the PPM matrix is subtracted by 0.25)) with the specified number and length.'
        )
        pfm = get_pfm(taxonomic_groups,data_local )
        ppm = get_ppm(pfm)
        ppm_L = get_ppm_rp25_L(ppm, L_)
        sample_number = [randint(0, len(ppm_L) - 1) for _ in range(filters)]
        ppm_r25_filters = []
        for i in sample_number:
            ppm_r25_filters.append(ppm_L[i])
        print('You will get the numpy array with shape ',
              str(np.array(ppm_r25_filters).shape))
        print(
            "You can use numpy's swaaxes function to make the dimension transformation suitable for initializing your parameters"
        )
        return np.array(ppm_r25_filters)
    elif pattern == 'ppm':
        print(
            'You will get the PPM matrix with the specified number and length.'
        )
        pfm = get_pfm(taxonomic_groups,data_local )
        ppm = get_ppm(pfm)
        ppm_L = get_ppm_L(ppm, L_)
        sample_number = [randint(0, len(ppm_L)-1) for _ in range(filters)]
        ppm_filters = []
        for i in sample_number:
            ppm_filters.append(ppm_L[i])
        print('You will get the numpy array with shape ',
              str(np.array(ppm_filters).shape))
        print(
            "You can use numpy's swaaxes function to make the dimension transformation suitable for initializing your parameters"
        )
        return np.array(ppm_filters)
    elif pattern == 'pwm':
        print(
            'You will get the PWM matrix of the specified length and the specified number calculated with '
            + str(background_acgt) + ' as the background.',
            'To prevent negative infinity, the value of 1e-2 is added to all positions.'
        )
        pfm = get_pfm(taxonomic_groups,data_local )
        ppm = get_ppm(pfm)
        ppm_L = get_ppm_L(ppm, L_)
        pwm = get_pwm(ppm_L, background_acgt)
        sample_number = [randint(0, len(pwm)-1) for _ in range(filters)]
        pwm_filters = []
        for i in sample_number:
            pwm_filters.append(pwm[i])
        print('You will get the numpy array with shape ',
              str(np.array(pwm_filters).shape))
        print(
            "You can use numpy's swaaxes function to make the dimension transformation suitable for initializing your parameters"
        )
        return np.array(pwm_filters)