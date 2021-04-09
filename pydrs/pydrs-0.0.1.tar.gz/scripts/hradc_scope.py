#import sys
#sys.path.insert(0, '../../')
#from pyELP import *

import pydrs
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import time
import sys


# Inicializa conexoes
com_port = input("\n Porta serial: ")
baud_rate = int(input("\n Baud-rate: "))
com_add = int(input("\n Endereco serial: "))
fs = float(input("\n Frequencia de amostragem: "))
num_curves = int(input("\n Numero de curvas: "))
id_curve = int(input("\n Indice da curva: "))
id_netsignal = int(input("\n Indice do netsignal: "))
id_analog_var_max = int(input("\n Indice do parametro Analog_Var_Max: "))

size_buf = 4096
n = int(size_buf/num_curves)
rangeFFT = range(int(n/2))
k = np.arange(n)
T = n/fs
frq = k/T 
frq = frq[rangeFFT] # one side frequency range

drs = pydrs.SerialDRS()
drs.Connect(com_port, baud_rate)
drs.SetSlaveAdd(com_add)

# Inicializa plot
fig = plt.figure()
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)

drs.set_param('Analog_Var_Max', id_analog_var_max, id_netsignal)

def animate(i):
    try:
        drs.disable_buf_samples()
        time.sleep(4)
        buffer = np.array(drs.read_buf_samples_ctom())
        drs.enable_buf_samples()
        
        buffer = buffer[id_curve:size_buf:num_curves]
        
        bufferMean = buffer.mean()
        std = buffer.std()
        buffer_max = buffer.max()
        buffer_min = buffer.min()
        buffer_pkpk = buffer_max - buffer_min
        
        Y = np.fft.fft(buffer-bufferMean)/n # fft computing and normalization
        try:
            Y = 20*np.log10(abs(Y[rangeFFT]))
            freq_pk = float(frq[np.where(Y == max(Y))])
        except:
            Y = frq*0
            freq_pk = 0
        
        
        print('\nMean: ' + str(bufferMean))
        print('Std: ' + str(std))
        print('Max: ' + str(buffer_max))
        print('Min: ' + str(buffer_min))
        print('Pk-Pk: ' + str(buffer_pkpk))      
        print('Peak Freq: ' + str(freq_pk))
               
        ax1.clear()
        ax2.clear()

        ax1.ticklabel_format(useOffset = False)
        #ax1.set_ylabel('iMeas [A]')
        ax1.plot(buffer)
        ax1.grid()   
        
        ax2.plot(frq,Y) # plotting the spectrum
        #ax2.set_xlim([0, 600])
        #ax2.set_ylim([0, 0.003])
        ax2.set_xlabel('Freq (Hz)')
        ax2.set_ylabel('|Y(freq)|')
        ax2.grid()

    except Exception as e:
        print(str(e))
        

ani = anim.FuncAnimation(fig, animate, interval = 200)
plt.show()

drs.Disconnect()

