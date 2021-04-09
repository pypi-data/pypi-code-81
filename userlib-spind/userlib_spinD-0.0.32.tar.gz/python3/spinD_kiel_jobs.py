import numpy as np
from python3.visualizations import write_STM
from python3.shell_commands import *
import os
import time
from python3.magnetisations import SpinLattice, MultiLayer


def start_spinD(sp, calc_directory, input_directory, dt, duration):
    if not os.path.isdir(calc_directory):
        make_directory(calc_directory)
    copy_element(input_directory / "inp", calc_directory)
    copy_element(input_directory / "lattice.in", calc_directory)
    copy_element(input_directory / "efield.in", calc_directory)
    copy_element(input_directory / "dyna.in", calc_directory)
    copy_element(input_directory / "job.sh", calc_directory)
    copy_element(input_directory / "simu.in", calc_directory)
    adjust_parameter("timestep", dt, calc_directory / "dyna.in")
    adjust_parameter("duration", duration, calc_directory / "dyna.in")
    if type(sp) is MultiLayer :
        z_size = sp.number_layers
    else :
        z_size = 1
    adjust_parameter("Nsize", " " +str(sp.size) + " " + str(sp.size) + " " + str(z_size), calc_directory / "lattice.in")
    # set simulation
    adjust_parameter("i_metropolis", '.F.', calc_directory / "simu.in")
    adjust_parameter("i_paratemp", '.F.', calc_directory / "simu.in")
    adjust_parameter("i_sd", '.T.', calc_directory / "simu.in")
    adjust_parameter("i_gneb", '.F.', calc_directory / "simu.in")
    adjust_parameter("i_htst", '.F.', calc_directory / "simu.in")
    adjust_parameter("i_vt", '.F.', calc_directory / "simu.in")
    adjust_parameter("i_min", '.F.', calc_directory / "simu.in")
    with change_directory(calc_directory):
        sp.write_STM()
        print('Spin Dynamic at: ' + str(calc_directory))
        if cluster() :
            adjust_parameter('#SBATCH --job-name=', '#SBATCH --job-name=spinD', 'job.sh')
            call_sbatch("job.sh")
        else :
            call_spin()



def start_minimisation(sp, calc_directory, input_directory):
    if not os.path.isdir(calc_directory) :
        make_directory(calc_directory)
    copy_element(input_directory / "inp", calc_directory)
    copy_element(input_directory / "lattice.in", calc_directory)
    copy_element(input_directory / "efield.in", calc_directory)
    #copy_element(input_directory + "/dyna.in", calc_directory)
    copy_element(input_directory / "job.sh", calc_directory)
    copy_element(input_directory / "simu.in", calc_directory)
    copy_element(input_directory / "minimization.in", calc_directory)
    if type(sp) is MultiLayer :
        z_size = sp.number_layers
    else :
        z_size = 1
    adjust_parameter("Nsize", " " +str(sp.size) + " " + str(sp.size) + " " + str(z_size), calc_directory / "lattice.in")
    # set simulation
    adjust_parameter("i_metropolis", '.F.', calc_directory / "simu.in")
    adjust_parameter("i_paratemp", '.F.', calc_directory / "simu.in")
    adjust_parameter("i_sd", '.F.', calc_directory / "simu.in")
    adjust_parameter("i_gneb", '.F.', calc_directory / "simu.in")
    adjust_parameter("i_htst", '.F.', calc_directory / "simu.in")
    adjust_parameter("i_vt", '.F.', calc_directory / "simu.in")
    adjust_parameter("i_min", '.T.', calc_directory / "simu.in")
    with change_directory(calc_directory):
        sp.write_STM()
        print('Minimisation at: ' + calc_directory)
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
            enerden = calc_directory / 'energy_density_end.dat'
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
    adjust_parameter("CalEnergy", '.T.', input_directory / "inp")
    start_spinD(sl, calc_directory, input_directory, dt, duration)
    # extract energies
    while not os.path.isfile(calc_directory / 'tot_energy_end.dat'):
        time.sleep(0.2)
    data = np.loadtxt(calc_directory / 'tot_energy_end.dat', unpack=True)
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



def update_lattice(calc_directory, multilayer=False, number_layers=1):
    SpinSTM_end = calc_directory / 'SpinSTM_end.dat'
    while not os.path.isfile(SpinSTM_end):
        time.sleep(1)
    if multilayer :
        sp = MultiLayer(path=SpinSTM_end, number_layers=number_layers)
    else:
        sp = SpinLattice(path=SpinSTM_end)
    return sp



def start_GNEB(sp_init, sp_final, calc_directory, input_directory, images, iterations, use_path=None, HTST=True):
    if not os.path.isfile(calc_directory) :
        make_directory(calc_directory)
    copy_element(input_directory / "inp", calc_directory)
    copy_element(input_directory / "lattice.in", calc_directory)
    copy_element(input_directory / "efield.in", calc_directory)
    copy_element(input_directory / "job.sh", calc_directory)
    copy_element(input_directory / "GNEB.in", calc_directory)
    copy_element(input_directory / "simu.in", calc_directory)
    time.sleep(1)
    adjust_parameter("i_metropolis", '.F.', calc_directory / "simu.in")
    adjust_parameter("i_paratemp", '.F.', calc_directory / "simu.in")
    adjust_parameter("i_sd", '.F.', calc_directory / "simu.in")
    adjust_parameter("i_gneb", '.T.', calc_directory / "simu.in")
    adjust_parameter("i_vt", '.F.', calc_directory / "simu.in")
    adjust_parameter("i_min", '.F.', calc_directory / "simu.in")
    if HTST :
        copy_element(input_directory + "/htst.in", calc_directory)
        adjust_parameter("i_htst", '.T.', calc_directory / "simu.in")
    adjust_parameter("nim", images, calc_directory / "GNEB.in")
    adjust_parameter("mep_itrmax", iterations, calc_directory / "GNEB.in")
    if sp_init.size == sp_final.size :
        if type(sp_init) is MultiLayer :
            if sp_init.number_layers == sp_final.number_layers :
                z_size = sp_init.number_layers
            else :
                print('ERROR: Initial and Final configurations have different number of layers')
                quit()
        else :
            z_size = 1
        adjust_parameter("Nsize", " " +str(sp_init.size) + " " + str(sp_init.size) + " " + str(z_size), calc_directory / "lattice.in")
    else :
        print('ERROR: Initial and Final configurations have different dimensions')
        quit()
    if use_path :
        copy_all_elements(use_path, '.dat', calc_directory)
        adjust_parameter("amp_rnd_path", 0.0, calc_directory / "GNEB.in")
    with change_directory(calc_directory):
        sp_init.write_STM(name='momfile_i')
        sp_final.write_STM(name='momfile_f')
        print('GNEB at: ', calc_directory)
        if cluster() :
            adjust_parameter('#SBATCH --job-name=', '#SBATCH --job-name=GNEB', 'job.sh')
            call_sbatch("job.sh")
        else :
            call_spin()




def start_MF_interface(SL, modes, calc_directory, input_directory, output_frequency=200, type=None):
    # PRIVATE METHOD FOR FINDING THE HIGHEST MF-IMAGE IN A GIVEN DIRECTORY
    def find_highest_image(directory, stepsize):
        number_tmp = 1
        while True :
            number_tmp += stepsize
            filename_tmp = directory / 'spin_'+str(number_tmp).zfill(4)+'.dat'
            if os.path.isfile(filename_tmp):
                number = number_tmp
            else :
                break
        return number
    # PRIVATE METHOD FOR STARTING A SINGLE MF CALCULATION
    def start_MF(SL, mode, steps, calc_directory, input_directory, vector_init=True, jobname='vt'):
        if not os.path.isfile(calc_directory) :
            make_directory(calc_directory)
        copy_element(input_directory / "inp", calc_directory)
        copy_element(input_directory / "lattice.in", calc_directory)
        copy_element(input_directory / "job.sh", calc_directory)
        copy_element(input_directory / "vt.in", calc_directory)
        copy_element(input_directory / "simu.in", calc_directory)
        # adjust input
        adjust_parameter("i_metropolis", '.F.', calc_directory / "simu.in")
        adjust_parameter("i_paratemp", '.F.', calc_directory / "simu.in")
        adjust_parameter("i_sd", '.F.', calc_directory / "simu.in")
        adjust_parameter("i_gneb", '.F.', calc_directory / "simu.in")
        adjust_parameter("i_htst", '.F.', calc_directory / "simu.in")
        adjust_parameter("i_vt", '.T.', calc_directory / "simu.in")
        adjust_parameter("i_min", '.F.', calc_directory / "simu.in")
        adjust_parameter("vec_init_index", mode, calc_directory / "vt.in")
        adjust_parameter("translation_steps", steps, calc_directory / "vt.in")
        if vector_init :
            adjust_parameter("i_vector_init", " .T. \'vector_init.dat\'", calc_directory / "vt.in")
        else :
            adjust_parameter("i_vector_init", " .F. \'vector_init.dat\'", calc_directory / "vt.in")
        # DO ACTUAL CALL TO MF ROUTINE
        with change_directory(calc_directory):
            SL.write_STM()
            print('VecTrans at: ', calc_directory)
            if cluster() :
                set_jobname(jobname, 'job.sh')
                call_sbatch("job.sh")
            else :
                call_spin()

    # EXCECUTION PART OF FUNCTION
    # ADJUST OUTPUT FREQUENCY
    adjust_parameter("Gra_log", ' .T. '+str(output_frequency) , input_directory / "inp")
    # ERROR CHECK
    if type == None:
        print('ERROR: set @type= \'fresh\' or \'further\' ' )
        exit()
    # STARTS A NEW VECTORTRANSLATION SERIES
    elif type == 'fresh':
        for mode in modes :
            tmp_calc_directory = calc_directory / ('MF_mode_'+str(mode))
            make_directory(tmp_calc_directory)
            # MAKE A FIRST RUN OF ONLY 1 STEP TO GET THE VECOR FOR THE MODE
            fs_directory = tmp_calc_directory / 'first_shoot'
            make_directory(fs_directory)
            start_MF(SL, mode, 1, fs_directory, input_directory, vector_init=False, jobname='vt')
            while not os.path.isfile(fs_directory / 'vt_0001.dat'):
                time.sleep(0.2)
            SL_vec = SpinLattice(path=fs_directory / 'vt_0001.dat')

            # START TRANSLATION IN POSITIVE DIRECTION (fwd)
            fwd_directory = tmp_calc_directory / 'fwd_iteration_1'
            make_directory(fwd_directory)
            write_STM(SL_vec, name=fwd_directory / 'vector_init.dat')
            start_MF(SL, mode, 10000, fwd_directory, input_directory, vector_init=True, jobname='MF'+str(mode)+'_fwd')

            # START TRANSLATION IN NEGATIVE DIRECTION (bck)
            SL_vec.mx, SL_vec.my, SL_vec.mz = -SL_vec.mx, -SL_vec.my, -SL_vec.mz
            bck_directory = tmp_calc_directory / 'bck_iteration_1'
            make_directory(bck_directory)
            write_STM(SL_vec, name=bck_directory / 'vector_init.dat')
            start_MF(SL, mode, 10000, bck_directory, input_directory, vector_init=True, jobname='MF'+str(mode)+'_bck')

    # CREATES A NEW ITERATION OF PREVIOUS MF-SERIES. INPUT @SL WILL BE IGNORED
    elif type == 'further':
        for mode in modes :
            tmp_calc_directory = calc_directory / 'MF_mode_'+str(mode)
            if not os.path.isdir(tmp_calc_directory):
                print('ERROR: Directory, in which the previous MF calculation is supposed to be, does not exist: ', str(tmp_calc_directory))
            # CHECK FOR HIGHEST ITERATION
            n = 1
            check_directory = tmp_calc_directory / 'fwd_iteration_'+str(n)
            while os.path.isdir(check_directory):
                n +=1
                check_directory = tmp_calc_directory / 'fwd_iteration_'+str(n)
            # RESTART fwd: GET SpinLattice AND VECTOR FROM LATEST CALCULATION
            old_fwd_directory = tmp_calc_directory / 'fwd_iteration_'+str(n-1)
            print('highest iteration folder found: ', old_fwd_directory)
            old_image_number = find_highest_image(old_fwd_directory, output_frequency)
            old_image_path =  old_fwd_directory / 'spin_'+str(old_image_number).zfill(4)+'.dat'
            old_image_vect =  old_fwd_directory / 'vt_'+str(old_image_number).zfill(4)+'.dat'
            SL_ini = SpinLattice(path=old_image_path)
            SL_vec = SpinLattice(path=old_image_vect)
            # START CALCULATION IN A NEW DIRECTORY
            fwd_directory = tmp_calc_directory / 'fwd_iteration_'+str(n)
            make_directory(fwd_directory)
            write_STM(SL_vec, name=fwd_directory / 'vector_init.dat')
            start_MF(SL_ini, mode, 10000, fwd_directory, old_fwd_directory, jobname='MF'+str(mode)+'_fwd')
            # RESTART bck: GET SpinLattice AND VECTOR FROM LATEST CALCULATION
            old_bck_directory = tmp_calc_directory / 'bck_iteration_'+str(n-1)
            old_image_number = find_highest_image(old_bck_directory, output_frequency)
            old_image_path =  old_bck_directory / 'spin_'+str(old_image_number).zfill(4)+'.dat'
            old_image_vect =  old_bck_directory / 'vt_'+str(old_image_number).zfill(4)+'.dat'
            SL_ini = SpinLattice(path=old_image_path)
            SL_vec = SpinLattice(path=old_image_vect)
            # START CALCULATION IN A NEW DIRECTORY
            bck_directory = tmp_calc_directory / 'bck_iteration_'+str(n)
            make_directory(bck_directory)
            write_STM(SL_vec, name=bck_directory / 'vector_init.dat')
            start_MF(SL_ini, mode, 10000, bck_directory, old_bck_directory, jobname='MF'+str(mode)+'_fwd')
