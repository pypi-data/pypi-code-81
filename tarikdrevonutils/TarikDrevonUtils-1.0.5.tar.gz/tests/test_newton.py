import importlib as imp
import numpy as np
import matplotlib.pyplot as plt
from numpy import pi
import scipy.optimize as sci_opt
import utils.newtonRaphson as nwt
import utils.displayStandards as dsp
imp.reload(nwt)
imp.reload(dsp)

def test_newton_rec():
    f = lambda y,x : np.tan(pi/2*(y-x))
    df = lambda y,x : pi/2*(1+f(y,x)**2)
    cond = lambda x0,x1,y0,y1 : y1>y0

    x,y0 = np.array([0,1.6]),0.01
    y0s = nwt.newton_recursive(f,df,x,y0,cond,Ncut=3,npts=3,tol=1e-5,nMax=100)
    f0s = np.array([f(y0,x0) for y0,x0 in zip(y0s,x)])

    #plot
    y,cs = np.linspace(0,2,1000),dsp.getCs('jet',x.size)
    plts = [[y,f(y,x0),c] for x0,c in zip(x,cs)]
    plts += [[y0s[i],f0s[i],[cs[i],'s']] for i in range(x.size)]
    plts += [[[0,y.max()],[0,0],'k']]
    dsp.stddisp(plts,labs=['$y$','$f(y;x)$'],lw=2,xylims=['y',-20,20],ms=5)


def test_newton_cplx_rec():
    f  = lambda z,z0 : np.sqrt(z**2 - z0**2)
    df = lambda z,z0 : z/f(z,z0)

    z0s = np.array([1+0.2J,1.5+0.15J,2.2+0.1J,3+0J])
    z0_nwt = nwt.newton_recursive(f,df,z0s,y0=1+0J,tol=1e-5,nMax=10,v=1)

    plts = [[z0s.imag,z0_nwt.imag,'rs-','im'],
            [z0s.real,z0_nwt.real,'bs-','re']]
    dsp.stddisp(plts)

def test_newton_cplx(opts='nm'):
    f  = lambda z,z0 : np.sqrt(z**2 - z0**2)
    df = lambda z,z0 : z/f(z,z0)
    z0 = 1+0.2J

    #newton
    z0_nwt = 0.7+0.1J
    if 'n' in opts:
        methods={'N':'Newton-CG','M':'Nelder-Mead','B':'BFGS','C':'CG'}
        method = methods['N']
        z0_nwt = nwt.newton_cplx(f,df,z0=z0_nwt,args=(z0,),tol=1e-5,nMax=10)[0]
        print(z0_nwt)

    #plot
    if 'm' in opts:
        npts = 100
        x,y = np.linspace(0,2,npts),np.linspace(-1,1,npts)
        X,Y = np.meshgrid(x,y)
        Z = X+1J*Y
        fz = np.abs(f(Z,z0))**2
        dF = lambda x,y:nwt.grad_fz2(f(x+1J*y,z0),df(x+1J*y,z0))

        x0,y0=z0_nwt.real,z0.imag
        plts = [[x0],[y0],'gs','$Z_0$']
        im = None #[X,Y,np.abs(fz)]
        fig,ax=dsp.stddisp(plots=plts,im=im,
            contour=[X,Y,fz,12],quiv=dF,
            imOpt='ch',pOpt='tG',lw=3,ms=10)



######################################################################

plt.close('all')
# test_newton_cplx()
test_newton_cplx_rec()
# x = nwt.newton(F,dF,x0,args=(z0,),tol=1e-5)
# test_newton_rec()
# test_newton_cplx()
