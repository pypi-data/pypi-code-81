'''
First example: function compare_preprocessing used on artificial data
Two possible values for y (property to predict):
    - peak 1, absorbance values at 1100 nm
    - baseline, absorbance values at 1200 nm

'''
print('\n'*100)

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
from colorspectra_y import colorspectra_y
import NIR_preprocess as nir_pre
plt.close('all')

np.random.seed(0)

#%% Choose y value
print('0 - Peak 1')
print('1 - Baseline')
user = int(input('Choose y value: '))

if int(user)==0:
    y_user = 100
else:
    y_user = 200

#%% Create dataset
x = np.arange(-15,15,0.01)

Y = []

for i in range(60):

    r0 = 10*np.random.rand()
    r1 = np.random.rand()
    r2 = np.random.rand()
    r3 = np.random.rand()
    
    y0 = (50+r0)*st.norm.pdf(x,-2,5) 
    y1 = 10+r1*st.norm.pdf(x,-6,0.1) 
    y2 = 10+r2*st.norm.pdf(x,-4,0.1) 
    y3 = 10+r3*st.norm.pdf(x,6,0.1) 
    y = y0+y1+y2+y3

    Y.append(y)
    
Y = np.array(Y)

# Only keep 2 peaks
x = x[800:1300]
Y = Y[:,800:1300]

X0 = Y
n, k = X0.shape

# Create y variable to predict
y = Y[:,y_user]
y = y[np.newaxis].T
y = 1/y

# Add noise to data
X0 = X0 + np.random.randn(n,k)/100

#%% Show original spectra
if int(user)==0:
    c_label = 'peak 1'
else:
    c_label = 'baseline'

colorspectra_y(X0,y, y_label='Absorbance', x_label='Wavelength (nm)', colorbar_label= c_label)
plt.axvline(x=y_user, linestyle='-.', c='g')
plt.xticks(np.arange(0,k+100,100),[1000, 1100, 1200, 1300,1400,1500],fontsize=14)

#%% Compare pre-processing
combination, datasets, datasets0, R2_all, R2adj_all, RMSECV_all, VIP_all, Ef_all, Wt = nir_pre.compare_preprocessing(X0, y)
