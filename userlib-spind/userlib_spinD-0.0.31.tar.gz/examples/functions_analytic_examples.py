import numpy as np
import sys
sys.path.append('../python3')
from python3.magnetisations import *
from python3.visualizations import *






def run_example_setup_skyrmion_get_radius():
    # GENERAL SETTINGS
    size, key, magmom = 20, 'hex', 1.
    # DEFINE RADIAL THETA-PROFILE PARAMETER
    c, w = 2., 3.
    # DEFINE SKYRMION PARAMETER
    helicity, vorticity = 0, 1.
    center = [size//2, 0]
    # SETUP LATTICE
    SL = SpinLattice(size=size, key=key, path=None, magmom=magmom)
    SL.addSkyrmion(center, vorticity, helicity , c, w)
    SL.getSkradius()
    print('radius   R_sk =', SL.sk_radius)
    write_STM(SL)
    show_lattice(SL, details='Sk')
    display_plots()


def run_example_charge_and_chargedensity():
    # GENERAL SETTINGS
    size, key, magmom = 30, 'hex', 1.
    # DEFINE VORTICITIES m1,m2. TOPOLOGICAL CHARGE IS -Q=m1+m2
    m1, m2 = -1, 1
    center_skyrmion1, center_skyrmion2 = [size//2 , size//4], [ size//2 , -(size//4)]
    # ADD TWO NEEL SKYRMIONS WITH VORTICITIES m1= -6 AND m2=5
    SL = SpinLattice(size=size , key=key , path=None, magmom=magmom)
    SL.addSkyrmion(center_skyrmion1 , m1, np. pi , 3. , 3)
    SL.addSkyrmion(center_skyrmion2 , m2, np. pi , 3. , 3)
    # GET TOPOLOGICAL CHARGE AND PRINT OUT
    SL.getTopocharge()
    print('Tolologic charge: Q =', SL.topo_charge)
    # SHOW LATTICE AND TOPOLOGICAL DENSITY
    show_lattice(SL, details=None)
    show_topodensity(SL)
    display_plots()




def run_example_setup_cycloidal_1qstates():
    # GENERAL SETTINGS
    size, key, magmom = 30, 'hex', 1.
    # INTERNAL COORDINATE SYSTEM
    #
    #           ----------
    #          /         /  \
    #         / (1,0,0)/     \
    #        /       /        \
    #        \       \       /
    #         \(0,1,0) \    /
    #          \         \ /
    #           ---------
    #
    # @Rq and @Iq span the plane, the spins rotate in. given in internal coordinates
    Rq = [0.0, 0.0, 1.0]
    Iq = [1.0, 1.0, 0.0]
    q = 0.05
    Q = np.asarray([ 1.0, 1.0, 0.0])*q
    # CREATE LATTICE OBJECT AND ADD 1q STATE
    sl = SpinLattice(size=size, key=key, path=None, magmom=magmom)
    sl.add1qstate(Rq, Iq, Q)
    # SHOW LATTICE INCLUDING DETAILS FOR SPINSPIRALS
    show_lattice(sl, details='SS')
    display_plots()



def run_example_setup_domainwall_get_width():
    # GENERAL SETTINGS
    size, key, magmom = 40, 'hex', 1.
    # DW settings
    sigma = 2.5
    r0 = size//3
    direction = np.array([0.5, np.sqrt(3.)/6.])
    # create a right rotating neel wall
    SL = SpinLattice(size=size, key=key, path=None, magmom=magmom)
    SL.addDomainwall( r0, direction, sigma, heli=np.pi/2.)
    # GET THE WIDTH FROM FITTING
    SL.getDWwidth()
    print('fitted width:  w =', SL.dw_width)
    show_lattice(SL, details='DW')
    display_plots()



def run_example_setup_double_domainwall():
    # GENERAL SETTINGS
    size, key, magmom = 40, 'hex', 1.
    # DW settings
    direction = np.array([0.5, np.sqrt(3.)/6.])
    sigma = 1.5
    r0_1 = size//5
    r0_2 = 2*size//3
    # create a right rotating neel wall
    SL = SpinLattice(size=size, key=key, path=None, magmom=magmom)
    SL.addDomainwall(r0_1, -direction, sigma, heli=np.pi/2)
    SL.addDomainwall(r0_2, direction, sigma, heli=np.pi)
    show_lattice(SL, details=None)
    display_plots()




def run_example_setup_multilayer_hex():
    c, w = 2., 3.
    helicity, vorticity = 0., 1.
    size, key, magmom1 = 70, 'hex', 1.
    # center is the same for both Skyrmions
    center = [size//2, 0]
    a1_0=2.0/3.0
    a2_0=1.0/3.0
    magmom2= 2.0
    ML =  MultiLayer(number_layers=2)
    # No offset for this layer
    SL0 = SpinLattice(size=size, key=key, path=None, magmom=magmom1)
    SL0.addSkyrmion(center, vorticity, helicity, c, w)
    # Offset for this layer
    SL1 = SpinLattice(size=size, key=key, path=None, magmom=magmom2, a1_0=a1_0, a2_0=a2_0)
    SL1.addSkyrmion(center, vorticity, helicity, c, w)
    ML.add_layer(SL0, index_layer=0, zpos_uc=0.)
    ML.add_layer(SL1, index_layer=1, zpos_uc=3.8302600704)
    # WRITE SpinSTM FOR MULTILAYER
    ML.write_STM(name='ML_hex_SpinSTMi.dat')



def run_example_setup_multilayer_quad():
    c, w = 2., 3.
    helicity, vorticity = 0., 1.
    size, key, magmom1 = 50, 'quad', 1.
    # center is the same for both Skyrmions
    center = [size//2, size//2]
    a1_0=0.5
    a2_0=0.5
    magmom2= 2.0
    ML =  MultiLayer(number_layers=2)
    # No offset for this layer
    SL0 = SpinLattice(size=size, key=key, path=None, magmom=magmom1)
    SL0.addSkyrmion(center, vorticity, helicity, c, w)
    # Offset for this layer
    SL1 = SpinLattice(size=size, key=key, path=None, magmom=magmom2, a1_0=a1_0, a2_0=a2_0)
    SL1.addSkyrmion(center, vorticity, helicity, c, w)
    ML.add_layer(SL0, index_layer=0, zpos_uc=0.)
    ML.add_layer(SL1, index_layer=1, zpos_uc=3.8302600704)
    # WRITE SpinSTM FOR MULTILAYER
    ML.write_STM(name='ML_quad_SpinSTMi.dat')



def run_example_setup_bimeron():
    a1, a2 = 1.0, 1.0
    R = 4
    size, key, magmom1 = 50, 'hex', 1.
    # center is the same for both Skyrmions
    center = [size//2, 0]
    ML =  MultiLayer(number_layers=1)
    SL = SpinLattice(size=size, key=key, path=None, magmom=magmom1)
    SL.add_bimeron(center, 4, 1, 0.1)
    ML.add_layer(SL, index_layer=0, zpos_uc=0.)
    ML.write_STM(name='Bimeron_SpinSTMi.dat')
    show_lattice(SL, details=None)



def run_example_setup_nanoskyrmionlattice():
    # CREATE LATTICE
    size, key, magmom = 27, 'hex', 1.0
    sl = SpinLattice(size=size, key=key, path=None, magmom=magmom)
    # DEFINE RECIPROKE VECTORS FOR PLANES OF ROTATION IN CARTESIAN COORDINATES
    Rq = np.array([0.0, 0.0, 1.0])
    Iq1 = np.array([1., 0., 0.])
    Iq2 = np.array([np.cos((2./3.)*np.pi), -np.sin((2./3.)*np.pi),0])
    Iq3 = np.array([np.cos((2./3.)*np.pi),np.sin((2./3.)*np.pi),0])
    # DEFINE LENGTH OF RECIPROCAL VECTOR @q = 2pi/lambda
    q = 2.*np.pi/4.5
    # CHANGE EVERY SPIN VECTOR BY HAND TO RECIEVE NANOSKYRMION LATTICE
    for n in range(size**2):
        rr = np.array([sl.X[n], sl.Y[n], sl.Z[n]]) + [0, 1./np.sqrt(3.), 0]
        ss1 = 2.*( Rq*np.cos(np.dot(-q*Iq1, rr)) - Iq1*np.sin(np.dot(-q*Iq1, rr)))
        ss2 = 2.*( Rq*np.cos(np.dot(-q*Iq2, rr)) - Iq2*np.sin(np.dot(-q*Iq2, rr)))
        ss3 = 2.*( Rq*np.cos(np.dot(-q*Iq3, rr)) - Iq3*np.sin(np.dot(-q*Iq3, rr)))
        spin = ss1 +ss2 +ss3
        norm = np.sqrt(spin[0]**2. +spin[1]**2. +spin[2]**2.)
        sl.mx[n], sl.my[n], sl.mz[n] = spin[0]/norm, spin[1]/norm, spin[2]/norm
    show_lattice(sl)



def run_example_uudd_by_superposition():
    # SPECIFY SPINSPIRALS
    Rq = [0.0, 0.0, 1.0]
    Iq = [1.0, 0.5, 0.0]
    q = 0.25
    Q =  np.asarray([ 1.0, 0.0, 0.0])
    # SPECIFY LATTICE
    size, key, magmom = 30, 'hex', 1.
    # CREATE STATES WITH LEFT AND RIGHT ROTATING SPINSPIRALS + PHASE SHIFT
    sl1 = SpinLattice(size=size, key=key, path=None, magmom=magmom)
    sl1.add1qstate(Rq, Iq, Q*q, phase=-np.pi/4.)
    sl2 = SpinLattice(size=size, key=key, path=None, magmom=magmom)
    sl2.add1qstate(Rq, Iq, -Q*q, phase=0)
    # CREATE SUPERPOSITION OF BOTH STATES
    sl3 = SpinLattice(size=size, key=key, path=None, magmom=magmom)
    sl3.add_superposition(sl1, sl2)
    # SHOW RESULTING LATTICE
    show_lattice(sl3, filename='uudd.png')



def run_example_setup_AFM_skyrmion():
    #SPECIFY LATTICE
    size, key, magmom = 30, 'quad', 1.
    sl = SpinLattice(size=size, key=key, path=None, magmom=magmom, AFM=True)
    # DEFINE RADIAL THETA-PROFILE PARAMETER
    c, w = 6., 5.
    # DEFINE SKYRMION PARAMETER
    helicity, vorticity = 0, -3.
    center = [size//2, size//2]
    sl.addSkyrmion(center, vorticity, helicity , c, w, AFM=True)
    # DEVIDE LATTICE INTO SUBLATTICES
    sublat1, sublat2 = afm_sublattices(sl)
    # CHECK TOPOLOGICAL CHARGES
    sl.getTopocharge()
    sublat1.getTopocharge()
    sublat2.getTopocharge()
    print('topological charges of lattices and sublattices:')
    print('0) AFM lattice  : ', sl.topo_charge)
    print('1) sub lattice 1: ', sublat1.topo_charge)
    print('2) sub lattice 2: ', sublat2.topo_charge)
    # SHOW RESULTING LATTICE
    show_lattice(sl, filename='afm_skyrmion.png')
    show_lattice(sublat1)
    show_lattice(sublat2)



def run_example_setup_chimera_state():
    #SPECIFY LATTICE
    size, key, magmom = 30, 'hex', 1.
    sl = SpinLattice(size=size, key=key, path=None, magmom=magmom, AFM=False)
    # SPECIFY SKYRMION PROPERTIES
    # SKYRMION SETTINGS
    vorticity = 1.
    helicity = np.pi/2.
    c, w = 3.1, 5.0
    ursprung = [size/2., 0.]
    # WRITE CHIMERA STATE
    sl.add_chimera(ursprung, vorticity, helicity , c, w, sym_chimera=False, angl_chimera=np.pi/2.)
    show_lattice(sl, filename='chimera_state.png', zoom=[sl.size/2, 0, 10])
