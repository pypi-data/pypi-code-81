

import sys
from scipy import constants
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np

from python3.shell_commands import *


#======================================================================
# configure dyna.in
dt = 1.0
dur = 50000
damping = 0.
integrator = 6

# configure inp
H_z = 1.0
gra_log_freq = 500

# configure lattice.in
number_spin = 1
magn_mom = 1.0




class MagnConstants:
    #==================================================================
    #==================================================================

    def __init__(self):
        # for the gyramagnetic ratio
        self.gJ = 2.0
        self.gyro_ratio = self.gJ* constants.e/constants.m_e/2.

        # for the bohr magneton
        self.mu_B = 5.7883818012e-05






class FileConfiguration:
    #==================================================================
    #==================================================================

    def config_inp(self, H_z, gra_log_freq):
        #==============================================================
        adjust_parameter("H_ext", "0.0  0.0  "+str(H_z),"inp")
        adjust_parameter("Gra_log", ' .T. ' +str(gra_log_freq), "inp")


    def config_dyna(self, dt, dur, damp, integrator):
        #==============================================================
        adjust_parameter("timestep", str(dt), "dyna.in")
        adjust_parameter("duration", str(dur), "dyna.in")
        adjust_parameter("damping", str(damp), "dyna.in")
        adjust_parameter("integration", str(integrator), "dyna.in")


    def config_lattice(self, num_spin, magn_mom):
        #==============================================================
        # creates a quadratic lattice with size (num_spin)x(num_spin)
        adjust_parameter("Nsize", " " +str(number_spin) + " " + str(number_spin) + " 1", "lattice.in")


    def config_spiral_start(self):
        #==============================================================
        adjust_parameter("qvec", "0.0  0.0  0.0", "spiral.start")




class FitFunctions():
    #==================================================================
    #==================================================================

    def __init__(self, H_z):
        #==================================================================
        self.H_z = H_z
        # gyromagnetic ratio, with g=1
        self.gyro_ratio_alternative = 1.760859e11
        self.gyro_ratio = constants.e/constants.m_e

    def sin_fit(self, x,f):
        #==================================================================
        return np.sin(f*x)

    def cos_fit(self, x,f):
        #==================================================================
        return np.cos(f*x)

    def tanh_fit(self, x, lamb):
        #==================================================================
        return np.tanh(self.gyro_ratio* self.H_z* x* lamb)






def plot_precission(H_z, damping, dt):
    #==================================================================
    #create figure-object
    fig=plt.figure()
    fig.set_size_inches(6,5)
    plt.subplots_adjust(wspace=0.35,hspace=0.25)
    #create subplot
    ax0=fig.add_subplot(1,1,1)
    # titles
    #labels
    ax0.set_ylabel(r'abs. moment / $\mu_B$')
    ax0.set_xlabel('time /s')

    # get number of files
    number_SpinSTM_files = int(dur/gra_log_freq)-1
    # arrays for coordinats
    x, y, z, T = [], [], [], []

    for i in range(number_SpinSTM_files-1):
        data = np.loadtxt('SpinSTM_' + str(i) + '.dat')
        x.append(data[3])
        y.append(data[4])
        z.append(data[5])
        #!!!!!ATTENTION!!!!!!!!
        # T is scaled by 0.5, so 2 timesteps are 1 timestep on correct time axes
        T.append(dt*i*gra_log_freq*0.5e-15*2)

    # initiate FitFunctions
    fits = FitFunctions(H_z)
    magn = MagnConstants()

    # fit z-data, x-data, y-data, depending on damping is zero or not
    if damping != 0.0 :
        popt0,pcov0 = curve_fit(fits.tanh_fit, T, z, p0=[damping], maxfev=5000)
        ax0.plot(T, fits.tanh_fit(np.asarray(T), *popt0), 'k-')
        print('The damping is : damp=', popt0[0])
        print('And should be  : damp=', damping)
        print('relative deviation |(d_c-d)/d_c|=', abs((popt0[0]-damping)/damping))
    else :
        popt1,pcov1 = curve_fit(fits.cos_fit, T, x, p0=[magn.gyro_ratio*H_z], maxfev=5000)
        popt2,pcov2 = curve_fit(fits.sin_fit, T, y, p0=[magn.gyro_ratio*H_z], maxfev=5000)
        ax0.plot(T, fits.cos_fit(np.asarray(T), *popt1), 'g-')
        ax0.plot(T, fits.sin_fit(np.asarray(T), *popt2), 'r-')
        print('We got Lamorfrequency of : w_c=', popt1[0])
        print('And it should be :         w_c=', magn.gyro_ratio*H_z)
        print('relative deviation  |(w_c-w)/w_c|=', abs((magn.gyro_ratio*H_z - popt1[0])/magn.gyro_ratio*H_z))

    # plot data
    ax0.plot(T, z, 'b+', label=r'S$_z$')
    ax0.plot(T, x, 'g+', label=r'S$_x$')
    ax0.plot(T, y, 'r+', label=r'S$_y$')

    # finishing
    plt.legend(loc='upper right', fontsize=10)
    plt.savefig('plot_test_precission.pdf')
    plt.show()







def main(H_z, gra_log_freq, dt, dur, damp, num_spin, magn_mom, integrator):
    #==================================================================
    make_directory('test_calculation')
    copy_element('input_data/inp', 'test_calculation')
    copy_element('input_data/dyna.in', 'test_calculation')
    copy_element('input_data/lattice.in', 'test_calculation')
    copy_element('input_data/spiral.start', 'test_calculation')
    copy_element('input_data/simu.in', 'test_calculation')

    with change_directory('test_calculation'):
        # load class FileConfiguration
        config = FileConfiguration()
        # configure inputfiles in actuell calculation folder
        config.config_inp(H_z, gra_log_freq)
        config.config_dyna(dt, dur, damp, integrator)
        config.config_lattice(num_spin, magn_mom)
        config.config_spiral_start()

        # execute calculation and wait for it to finish
        call_spin()
        while not os.path.isfile("SpinSTM_end.dat") :
            time.sleep(5)

        # present results
        plot_precission(H_z, damping, dt)





if __name__ == '__main__':
    main(H_z, gra_log_freq, dt, dur, damping, number_spin, magn_mom, integrator)
