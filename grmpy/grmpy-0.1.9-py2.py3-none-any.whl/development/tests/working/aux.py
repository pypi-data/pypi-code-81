from scipy import stats
import numpy as np
#Studnt, n=999, p<0.05, 2-tail
#equivalent to Excel TINV(0.05,999)

x = 0.0458

se = 0.0147

print(x/se)
