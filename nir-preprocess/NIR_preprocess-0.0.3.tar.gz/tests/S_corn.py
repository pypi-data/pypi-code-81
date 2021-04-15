'''
Second example: function compare_preprocessing used on corn data
https://www.eigenvector.com/data/Corn/index.html
1 NIR spectrometer used: m5
2 property values studied: moisture and protein values for each of the samples 
'''

print('\n'*100)

import numpy as np
import matplotlib.pyplot as plt
from fct_loadmat import loadmat
from colorspectra_y import colorspectra_y
import NIR_preprocess as nir_pre

plt.close('all')

#%% Load data
data = loadmat('corn.mat')
m5 = data['m5spec']['data']
y = data['propvals']['data']

# Set y values
y1 = y[:,0][np.newaxis].T # moisture
y2 = y[:,2][np.newaxis].T # protein

y = np.concatenate([y1,y2], axis=1)

# Choose which spectromoter to use
X0 = m5
n, k = X0.shape

#%% Show original spectra
colorspectra_y(X0,y1,y_label='Absorbance', x_label='Wavelength (nm)', colorbar_label='moisture')
plt.text(0.01,0.85,'A', fontsize=12)
plt.xticks([0, 300,600],[1100, 1700, 2300],fontsize=14)

colorspectra_y(X0,y2,y_label='Absorbance', x_label='Wavelength (nm)', colorbar_label= 'protein')
plt.text(0.01,0.85,'B', fontsize=12)
plt.xticks([0, 300,600],[1100, 1700, 2300],fontsize=14)

#%% Compare pre-processing
combination, datasets, datasets0, R2_all, R2adj_all, RMSECV_all, VIP_all, Ef_all, Wt = nir_pre.compare_preprocessing(X0, y, nbPC=3)