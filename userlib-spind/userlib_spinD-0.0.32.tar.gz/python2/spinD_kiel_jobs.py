import numpy as np
from visualizations import write_STM
from shell_commands import *
import os
import time
from magnetisations import SpinLattice


def start_spinD(sp, calc_directory, input_directory, dt, duration):
    if not os.path.isdir(calc_directory) :
        make_directory(calc_directory)
    copy_element(input_directory + "/inp", calc_directory)
    copy_element(input_directory + "/lattice.in", calc_directory)
    copy_element(input_directory + "/efield.in", calc_directory)
    copy_element(input_directory + "/dyna.in", calc_directory)
    copy_element(input_directory + "/job.sh", calc_directory)
    copy_element(input_directory + "/simu.in", calc_directory)
    adjust_parameter("timestep", dt, calc_directory + "/dyna.in")
    adjust_parameter("duration", duration, calc_directory + "/dyna.in")
    adjust_parameter("Nsize", " " +str(sp.size) + " " + str(sp.size) + " 1", calc_directory + "/lattice.in")
    # set simulation
    adjust_parameter("i_metropolis", '.F.', calc_directory + "/simu.in")
    adjust_parameter("i_paratemp", '.F.', calc_directory + "/simu.in")
    adjust_parameter("i_sd", '.T.', calc_directory + "/simu.in")
    adjust_parameter("i_gneb", '.F.', calc_directory + "/simu.in")
    adjust_parameter("i_htst", '.F.', calc_directory + "/simu.in")
    adjust_parameter("i_vt", '.F.', calc_directory + "/simu.in")
    adjust_parameter("i_min", '.F.', calc_directory + "/simu.in")
    with change_directory(calc_directory):
        write_STM(sp)
        print 'Spin Dynamic at: ', calc_directory
        if cluster() :
            adjust_parameter('#SBATCH --job-name=', '#SBATCH --job-name=spinD', 'job.sh')
            call_sbatch("job.sh")
        else :
            call_spin()



def start_minimisation(sp, calc_directory, input_directory):
    if not os.path.isdir(calc_directory) :
        make_directory(calc_directory)
    copy_element(input_directory + "/inp", calc_directory)
    copy_element(input_directory + "/lattice.in", calc_directory)
    copy_element(input_directory + "/efield.in", calc_directory)
    #copy_element(input_directory + "/dyna.in", calc_directory)
    copy_element(input_directory + "/job.sh", calc_directory)
    copy_element(input_directory + "/simu.in", calc_directory)
    copy_element(input_directory + "/minimization.in", calc_directory)
    adjust_parameter("Nsize", " " +str(sp.size) + " " + str(sp.size) + " 1", calc_directory + "/lattice.in")
    # set simulation
    adjust_parameter("i_metropolis", '.F.', calc_directory + "/simu.in")
    adjust_parameter("i_paratemp", '.F.', calc_directory + "/simu.in")
    adjust_parameter("i_sd", '.F.', calc_directory + "/simu.in")
    adjust_parameter("i_gneb", '.F.', calc_directory + "/simu.in")
    adjust_parameter("i_htst", '.F.', calc_directory + "/simu.in")
    adjust_parameter("i_vt", '.F.', calc_directory + "/simu.in")
    adjust_parameter("i_min", '.T.', calc_directory + "/simu.in")
    with change_directory(calc_directory):
        write_STM(sp)
        print 'Minimisation at: ', calc_directory
        if cluster() :
            adjust_parameter('#SBATCH --job-name=', '#SBATCH --job-name=spinD', 'job.sh')
            call_sbatch("job.sh")
        else :
            call_spin()


#===============================================================================
# INPUT: spinlattice object @sl
#        directory for calculation, string: @calcdirectory
#        directory for the input files, string: @input_directory
#OUTPUT: 1d array with energy contributions from all interactions
#===============================================================================
def numeric_energy(sl, calc_directory, input_directory):
    # SUBFUNCTION: read out energy_density_end.dat
    def get_calenergy_data(calc_directory):
        EXC = []
        DMI = []
        ANI = []
        ZEE = []
        DIP = []
        BIQ = []
        FSP = []
        TOT = []
        for n in range(images) :
            exc = dmi = ani = zee = dip = biq = fsp = tot = 0.0
            enerden = calc_directory + '/energy_density_end.dat'
            with open(enerden) as file:
                for line in file:
                    data = np.asarray(line.split())
                    if data[0][0] == '#':
                        continue
                    exc += float(data[2])
                    dmi += float(data[3])
                    ani += float(data[4])
                    zee += float(data[5])
                    dip += float(data[6])
                    biq += float(data[7])
                    fsp += float(data[8])
                    tot += float(data[9])
            EXC.append(exc)
            DMI.append(dmi)
            ANI.append(ani)
            ZEE.append(zee)
            DIP.append(dip)
            BIQ.append(biq)
            FSP.append(fsp)
            TOT.append(tot)
        return EXC, DMI, ANI, ZEE, DIP, BIQ, FSP, TOT
    # start spindynamics for just 1 step with zero time evolution
    dt = 0
    duration=1
    adjust_parameter("CalEnergy", '.T.', input_directory + "/inp")
    start_spinD(sl, calc_directory, input_directory, dt, duration)
    # extract energies
    while not os.path.isfile(calc_directory + '/tot_energy_end.dat'):
        time.sleep(0.2)
    data = np.loadtxt(calc_directory + '/tot_energy_end.dat', unpack=True)
    Exc_intra = data[2]
    Exc_inter = data[3]
    Dmi = data[4]
    Ani = data[5]
    Zee = data[6]
    Dip = data[7]
    Biq = data[8]
    Sp4 = data[9]
    Sp3 = data[10]
    Abs = data[11]
    return np.asarray([Abs, Exc_intra, Zee, Ani, Dmi, Sp3, Sp4, Biq, Dip])



def update_lattice(calc_directory):
    SpinSTM_end = calc_directory + '/SpinSTM_end.dat'
    while not os.path.isfile(SpinSTM_end):
        time.sleep(1)
    sp = SpinLattice(path=SpinSTM_end)
    return sp



def start_GNEB(sp_init, sp_final, calc_directory, input_directory, images, iterations, use_path=None, HTST=True):
    if not os.path.isfile(calc_directory) :
        make_directory(calc_directory)
    copy_element(input_directory + "/inp", calc_directory)
    copy_element(input_directory + "/lattice.in", calc_directory)
    copy_element(input_directory + "/efield.in", calc_directory)
    copy_element(input_directory + "/job.sh", calc_directory)
    copy_element(input_directory + "/GNEB.in", calc_directory)
    copy_element(input_directory + "/simu.in", calc_directory)
    adjust_parameter("i_metropolis", '.F.', calc_directory + "/simu.in")
    adjust_parameter("i_paratemp", '.F.', calc_directory + "/simu.in")
    adjust_parameter("i_sd", '.F.', calc_directory + "/simu.in")
    adjust_parameter("i_gneb", '.T.', calc_directory + "/simu.in")
    adjust_parameter("i_vt", '.F.', calc_directory + "/simu.in")
    adjust_parameter("i_min", '.F.', calc_directory + "/simu.in")
    if HTST :
        copy_element(input_directory + "/htst.in", calc_directory)
        adjust_parameter("i_htst", '.T.', calc_directory + "/simu.in")
    adjust_parameter("nim", images, calc_directory + "/GNEB.in")
    adjust_parameter("mep_itrmax", iterations, calc_directory + "/GNEB.in")
    if sp_init.size == sp_final.size :
        adjust_parameter("Nsize", " " +str(sp_init.size) + " " + str(sp_init.size) + " 1", calc_directory + "/lattice.in")
    else :
        print 'ERROR: Initial and Final configurations have different dimensions'
        quit()
    if use_path :
        copy_all_elements(use_path, '.dat', calc_directory)
        adjust_parameter("amp_rnd_path", 0.0, calc_directory + "/GNEB.in")
    with change_directory(calc_directory):
        write_STM(sp_init, name='momfile_i')
        write_STM(sp_final, name='momfile_f')
        print 'GNEB at: ', calc_directory
        if cluster() :
            adjust_parameter('#SBATCH --job-name=', '#SBATCH --job-name=GNEB', 'job.sh')
            call_sbatch("job.sh")
        else :
            call_spin()





def start_VecTrans(SL, mode, steps, calc_directory, input_directory, jobname='vt'):
    if not os.path.isfile(calc_directory) :
        make_directory(calc_directory)
    copy_element(input_directory + "/inp", calc_directory)
    copy_element(input_directory + "/lattice.in", calc_directory)
    copy_element(input_directory + "/job.sh", calc_directory)
    copy_element(input_directory + "/vt.in", calc_directory)
    copy_element(input_directory + "/simu.in", calc_directory)
    # adjust input
    adjust_parameter("i_metropolis", '.F.', calc_directory + "/simu.in")
    adjust_parameter("i_paratemp", '.F.', calc_directory + "/simu.in")
    adjust_parameter("i_sd", '.F.', calc_directory + "/simu.in")
    adjust_parameter("i_gneb", '.F.', calc_directory + "/simu.in")
    adjust_parameter("i_htst", '.F.', calc_directory + "/simu.in")
    adjust_parameter("i_vt", '.T.', calc_directory + "/simu.in")
    adjust_parameter("i_min", '.F.', calc_directory + "/simu.in")
    adjust_parameter("vec_init_index", mode, calc_directory + "/vt.in")
    adjust_parameter("translation_steps", steps, calc_directory + "/vt.in")

    with change_directory(calc_directory):
        write_STM(SL, name='SpinSTMi.dat')

        print 'VecTrans at: ', calc_directory
        if cluster() :
            set_jobname(jobname, 'job.sh')
            call_sbatch("job.sh")
        else :
            call_spin()
