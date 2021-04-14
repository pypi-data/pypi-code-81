
import math
import numpy as np

############################# units #######################################
#m,s,kg
km      = 1e3
#m       = 1.0
cm      = 1e-2
mm      = 1e-3
mum     = 1e-6
nm      = 1e-9
A       = 1e-10
pm      = 1e-12
fm      = 1e-15
cm2     = cm**2
cm3     = cm**3
mm2     = 1e-6
mm3     = 1e-9
mum2    = mum**2
mum3    = mum**3
mum2cm2 = 1e-8
#s       = 1.0
kHz     = 1e3
MHz     = 1e6
GHz     = 1e9
THz     = 1e12
PHz     = 1e15
ns      = 1e-9
ps      = 1e-12
fs      = 1e-15
#kg      = 1.0
g       = 1e-3
##energy
#J       = 1.0
eV      = 1.60217662*pow(10.,-19)
keV     = eV*1e3
meV     = eV*1e6
meV     = eV*1e-3
kV      = 1e3
muW      = 1e-6
mW      = 1e-3
kW      = 1e3
MJ      = 1e6
mA      = 1e-3
Na      = 6.02214076e23
## weird units
grain   = 6.47989e-5
lbs     = 0.453592
kmh     = km/3600

########################### physics constants ############################
q       = eV                        #C
kB      = 1.38064852*pow(10,-23)    #J/K
eps0    = 8.854187817*pow(10,-12)   #S.I.
mu0     = 4*math.pi*pow(10.,-7)          #H.m
hbar    = 1.0545718*pow(10,-34)     #J.s
h       = 2*math.pi*hbar;                #J.s
hplanck = 2*math.pi*hbar;                #J.s
m0      = 9.1093856*pow(10,-31)     #kg
emass   = 510.99906                 #keV
c       = 299792458                 #m/s


# alias
Angstrum = pow(10.,-10)
c0       = 299792458

############### physics values ################################
alpha_cst = 1/137
a0 = hbar/(m0*c*alpha_cst)/A
mc2 = 510.99906 # keV
hbsm = pow(hbar/nm,2)/(2*m0)/eV # eV (k=1nm^-1)

mph2kmh = lambda mph:1.609344*mph


#####################################################################
#unit conversions
eV2Hz   = lambda E:E*eV/hplanck
eV2mum  = lambda E:c/eV2Hz(E)/mum
keV2A   = lambda E:c/eV2Hz(E*1000)/A
meV2THz = lambda E:E*meV/hplanck/1e12
THz2meV = lambda nu: hplanck*nu*THz/meV
lam2eV  = lambda lam: hplanck*c0/(lam*nm)/eV
lam2omega = lambda lam: 2*math.pi*c0/(lam*nm)
T2meV = lambda T:kB*T/meV
kT = lambda T:kB*T/meV
omega2meV = lambda omega: hbar*omega/meV

keV2v     = lambda KE:math.sqrt(1 - 1/(1+np.array(KE)/mc2)**2)
keV2lam   = lambda KE:h*c0/(np.sqrt(KE*(2*emass+KE))*keV)/A
lam2keV   = lambda lam:emass*(-1+np.sqrt(1+((h*c0/keV)/(lam*A*emass))**2))
keV2sigma = lambda KE:2*np.pi*m0*(1+KE/mc2)*keV2lam(KE)*A*eV/h**2*kV*A #rad/(m*V)

Vg2Ug = lambda Vg,k0:Vg*2*m0*(1+lam2keV(1/k0)/mc2)*q/h**2*A**2
#####################################################################
#functions
def E2lam(E) :
    '''E(eV),lam(mum)'''
    return eV2mum(E)
