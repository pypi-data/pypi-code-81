'''Generic mathematical statistical functions for semiconductors
'''
import time
import scipy.special as spe
import numpy as np
import mpmath as mpm
from . import displayStandards as dsp
# from integrationRect import *
from . import newtonRaphson as nwt


##### def : Maxwell-Boltzmann Statistics
def MaxwellBoltz(x):
    return np.exp(-x)

##### def Fermi-Dirac statistics Th
def FermiDirac(x):
    return 1/(1+np.exp(x))
def FD_int(etas,j,dps=5):
    mpm.mp.dps = dps; mpm.mp.pretty = True;
    etas = np.array([etas]) if np.isscalar(etas) else np.array(etas)
    Li      = [mpm.polylog(j+1,-np.exp(float(eta))).real for eta in etas]
    FDint   = -spe.gamma(j+1)*np.array(Li)
    return FDint
def FermiDiracInt_Th(etas,dps=10):
    return FD_int(etas,0.5,dps)
def dFermiDiracInt_Th(etas,dps=10):
    return spe.gamma(1.5)/spe.gamma(0.5)*FD_int(etas,-0.5,dps)

def FermiDiracIntInv0(x,eta0=0,dps=5):
    f  = lambda eta: FermiDiracInt_Th(eta,dps) - x
    df = lambda eta:dFermiDiracInt_Th(eta,dps)
    eta0 = nwt.newtonRaphson1D(f,df,eta0,tol=0.0001,nMax=10)
    #eta0 = bis.bissection2(f,-2,2,tol=0.001,Nmax=100)
    #eta0 = nwt.newtonRaphson1Ddebug(f,df,eta0,np.linspace(0,3,10), tol=0.0001,nMax=10)
    eta0 = eta0[0]
    return eta0

def FermiDiracIntInv(x,eta0=0,dps=5):
    x = np.array([x]) if np.isscalar(x) else np.array(x)
    N = x.size
    etas  = np.zeros((N))
    for i in range(N):
        eta0 = FermiDiracIntInv0(x[i],eta0,dps); #printeta0
        etas[i] = eta0
    return etas



###### Fermi Dirac numerical integrations
def FermiDiracInt(eta,dx=0.001,xMax=100):
    eta = np.array([eta]) if np.isscalar(eta) else np.array(eta)
    N       = eta.size;
    FDint  = np.zeros((N))
    for i in range(N):
        X        = np.arange(0,eta[i]+xMax,dx)
        FDint[i] = sum(np.sqrt(X)*FermiDirac(X-eta[i]) )*dx
    return FDint
def dFermiDiracInt(eta,dx=0.001,xMax=100):
    eta = np.array([eta]) if np.isscalar(eta) else np.array(eta)
    N       = eta.size;
    dFDint  = np.zeros((N))
    for i in range(N):
        X = np.arange(0,eta[i]+xMax,dx)
        dFDint[i] = sum(np.sqrt(X)*np.exp(X-eta[i])*pow(FermiDirac(X-eta[i]),2))*dx
    return dFDint

def dFermiDiracIntInv(x,eta0=0,dps=5):
    return 1/dFermiDiracInt_Th(FermiDiracIntInv(x,eta0,dps))


#### def : Misc:
dummyLambda = lambda E:np.ones((E.size))
#####################################################################
##### def : display
def displayLi():
    mpm.mp.dps = 15; mpm.mp.pretty = True;
    etas = np.linspace(-2,0.8,100)
    Lim2 = np.array([mpm.polylog(-2,eta) for eta in etas])
    Lim1 = np.array([mpm.polylog(-1,eta) for eta in etas])
    Li0  = np.array([mpm.polylog( 0,eta) for eta in etas])
    Li1  = np.array([mpm.polylog( 1,eta) for eta in etas])
    Li2  = np.array([mpm.polylog( 2,eta) for eta in etas])
    xlabs = ['$\eta$','$Li$']
    plots = [[etas,Lim2,'r','$Li_{-2}(x)$'],
             [etas,Lim1,'y','$Li_{-1}(x)$'],
             [etas,Li0 ,'g','$Li_0(x)$'],
             [etas,Li1 ,'b','$Li_1(x)$'],
             [etas,Li2 ,'m','$Li_2(x)$']]
    stdDispPlt(plots,xlabs,xlims=[-2,1,-1,1])
def display_FermiInt():
    eta = np.linspace(-2,2,100)

    t0 = time.clock()
    FDint = FermiDiracInt(eta,dx=0.001,xMax=50)
    print('My computation %f ' %(time.clock()-t0));t0 = time.clock();
    FDint_th1 = FermiDiracInt_Th(eta,dps=4)
    print('Th computation %f ' %(time.clock()-t0));t0 = time.clock();

    plots = [[eta,FDint,'b','$num$'],
             [eta,FDint_th1 ,'r','$th_1$' ],]
    xlabs = ['$\eta$','$F_{1/2}(\eta)}$']
    stdDispPlt(plots,xlabs)

def display_dFermiInt(opt=0,timeOpt=0):
    eta = np.linspace(-2,2,100)
    FDint_Th    = lambda x:FermiDiracInt_Th(x)
    dFDint_Th   = lambda x:dFermiDiracInt_Th(x)
    FDint_Num   = lambda x:FermiDiracInt(x)
    dFDint_Num  = lambda x:dFermiDiracInt(x)
    if opt:
        if timeOpt:
            t0 = time.clock()
            FDint_num = FermiDiracInt(eta,dx=0.01,xMax=50)
            print('My computation %f ' %(time.clock()-t0));t0 = time.clock();
            FDint_th = FermiDiracInt_Th(eta,dps=10)
            print('Th computation %f ' %(time.clock()-t0));t0 = time.clock();
        else :
            FDint_num = dFDint_Num(eta)
            FDint_th  = dFDint_Th(eta)
        plots = [[eta, FDint_num  ,'b','$num$'],
                 [eta, FDint_th,'r','$th$' ],]
        xlabs = ['$\eta$','$\partial_{\eta}F_{1/2}(\eta)}$']
        stdDispPlt(plots,xlabs)
    else :
        displayDerivative(eta,FDint_Th  ,dFDint_Th ,['\eta','F_{-1/2}^{ana} '],showOpt=0)
        #displayDerivative(eta,FDint_Num,dFDint_Num,['\eta','F_{-1/2}^{int}'],showOpt=0)
        plt.show()


#####################################################################
##### def : display
# inversions
def testFermiInversion():
    x,eta0 = 0,0
    eta0 = FermiDiracIntInv0(x,eta0);

    f  = lambda eta:FermiDiracInt_Th(eta) - x
    df = lambda eta:dFermiDiracInt_Th(eta)
    etas = np.linspace(-2,2,50)
    plots = [[etas,f(etas) , 'b-+' ,'$f_x(\eta)$'],
             [eta0,f(eta0) ,'bs'   ,'$\eta_0$'],]
             #[etas,df(etas), 'r--' ,'$\partial_{\eta} f_x(\eta)$'],
    stdDispPlt(plots,['$\eta $','$f_x(\eta)$'],axPos=[0.15,0.12,0.8,0.8])

def testFermiInversions():
    #x = np.concatenate((np.linspace(0,0.5,50),np.linspace(0.5,1,10)) )
    x = np.linspace(0.1,1,100)
    eta0   = 0
    etas   = FermiDiracIntInv(x,eta0);
    x0     = FermiDiracInt_Th(etas)
    plots  = [[x,etas   , 'r-+' ,'$F^{-1}(x)$'],
              [etas,x   , 'm-+' ,'$F(\eta)$'],
              [x,x0     , 'k-+' ,'$F(F^{-1}(x))=x$'],]
    stdDispPlt(plots,['$x $','$F_{1/2}^{-1}(x)$'])

def testdFermiIntInv():
    x = np.concatenate((np.linspace(0.1,0.5,50),np.linspace(0.5,1,10)) )
    eta0 = 0
    FDintInv  = lambda x:FermiDiracIntInv(x,eta0)
    dFDintInv = lambda x:dFermiDiracIntInv(x,eta0)
    displayDerivative(x,FDintInv,dFDintInv,['\eta','F_{-1/2}(x)'])


if __name__=='__main__':
    #displayLi()
    #display_FermiInt()
    #display_dFermiInt()
    #testFermiInversion()
    #testFermiInversions()
    testdFermiIntInv()
    print("Statistics compiled")
