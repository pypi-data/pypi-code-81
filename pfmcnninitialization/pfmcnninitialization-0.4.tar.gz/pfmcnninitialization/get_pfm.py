#获取pfm
import numpy as np
import wget
import pandas as pd
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