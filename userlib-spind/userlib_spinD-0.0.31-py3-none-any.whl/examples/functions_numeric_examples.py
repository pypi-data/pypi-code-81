import numpy as np
from python3.magnetisations import SpinLattice, MultiLayer
from python3.visualizations import *
from python3.shell_commands import *
from python3.spinD_kiel_jobs import *





def run_example_multilayer_GNEB():
    # SET UP MULTILAYER WITH 2 LAYERS CONTAINING SKYRMIONS AS INIT STATE
    c, w = 2., 3.
    helicity, vorticity = 0., 1.
    size, key, magmom1 = 50, 'hex', 1.
    # center is the same for both Skyrmions
    center = [size//2, 0]
    a1_0=2.0/3.0
    a2_0=1.0/3.0
    magmom2= 2.0
    SL0_init = SpinLattice(size=size, key=key, path=None, magmom=magmom1)
    SL0_init.addSkyrmion(center, vorticity, helicity, c, w)
    SL1_init = SpinLattice(size=size, key=key, path=None, magmom=magmom2, a1_0=a1_0, a2_0=a2_0)
    SL1_init.addSkyrmion(center, vorticity, helicity, c, w)
    ML_init =  MultiLayer(number_layers=2)
    ML_init.add_layer(SL0_init, index_layer=0, zpos_uc=0.)
    ML_init.add_layer(SL1_init, index_layer=1, zpos_uc=3.8302600704)

    # SET UP MULTILAYER WITH 2 FM LAYERS AS FINAL STATE
    SL0_final = SpinLattice(size=size, key=key, path=None, magmom=magmom1)
    SL1_final = SpinLattice(size=size, key=key, path=None, magmom=magmom2, a1_0=a1_0, a2_0=a2_0)
    ML_final =  MultiLayer(number_layers=2)
    ML_final.add_layer(SL0_final, index_layer=0, zpos_uc=0.)
    ML_final.add_layer(SL1_final, index_layer=1, zpos_uc=3.8302600704)

    # CREATE DIRECTORY FOR TEST CALCULATION AND DEFINE DIRECTORY CONTAINING INPUTS
    images = 20
    iterations = 1
    input_directory = 'input_data'
    calc_directory = 'calculation_multilayer_GNEB'
    make_directory(calc_directory)

    # START CALCULATION FOR MAGNETIC FIELD B=0
    Bfield = 0.
    adjust_parameter("H_ext", "0.0  0.0  "+str(Bfield), input_directory + "/inp")
    start_GNEB(ML_init, ML_final, calc_directory, input_directory, images, iterations, use_path=None)
