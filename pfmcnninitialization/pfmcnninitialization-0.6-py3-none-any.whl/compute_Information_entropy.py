import numpy as np
#计算信息熵，越小越好;注意，这里加了1e-5，防止0的影响
def compute_Information_entropy(acgt):
    return -1*np.sum(np.log2(np.array(acgt)+1e-5)* (np.array(acgt)+1e-5))