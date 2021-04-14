from .displayStandards import*
#import matplotlib.pyplot as plt
from scipy import signal
from math import*

__all__ = ['Fourier','get_FFT','displayFourier','plot_fft2d',
'squareBis','unit_impulse','fftParams']
#### def : Main user interface
def Fourier(yfunc,Tf=100,dt=0.01,fopt='s',dOpt='ftc',pOpt='RIYP',
            xlims={'t':[],'f':[]},labOpts=['t','f'],
            Yth=lambda x:np.zeros((x.size)),figsize='12'):
    ''' where :
- fopt(Fourier opt)   : 's(sym) p(periodic)r(real)
- dOpt(display opt)   : 'f(freq)t(time)c(compare)d(fourierParams)s(spit Phase)
- pOpt(plot opt)      : 'R(real)I(imag)Y(abs)P(phase)
- Yth : lambda function to compare against
    '''
    symOpt,fft_func = 's' in fopt, [get_FFT,get_rFFT]['r' in fopt]

    #Signal and Fourier
    t = np.arange(0,Tf,dt) - Tf/2*symOpt
    y = yfunc(t)
    f,Y = fft_func(t,y,dt,'p' in fopt)

    #display
    df,fmax = fftParams(dt,Tf,dopt='d' in pOpt)
    if 't' in dOpt or 'f' in dOpt:
        nrows=2 if 'f' in dOpt and 't' in dOpt else 1
        ncols=2 if 's' in dOpt else 1
        fs=12;fonts=[fs]*5 #[fs,fsLeg,fsL,fsT ]
        fig,ax= create_fig(figsize=figsize,pad=0.75,rc=[nrows,ncols])
        axT,axF=ax
    if 't' in dOpt:
        displayFourier(t,y,labOpt=labOpts[0],opt=pOpt,ax=axT,xlims=xlims['t'],showOpt=0,fonts=fonts)
    if 'f' in dOpt:
        displayFourier(f,Y,labOpt=labOpts[1],opt=pOpt,ax=axF,xlims=xlims['f'],showOpt=0,fonts=fonts)
    if 'c' in dOpt:
        fig_c=compareFourier(f,Y,Yth(f),xlims=xlims['f'],showOpt=0)
        fig_c.show()
    if 't' in dOpt or 'f' in dOpt:
        fig.show()
    return t,y,f,Y

def get_FFT(t,y,dt=0,pOpt=False):
    ''' pOpt : periodic option => divide by sample size'''
    N,dt = t.size,t[1]-t[0] #shape[0]
    Y = np.fft.fftshift(np.fft.fft(y)*[dt,1./N][pOpt])
    f = np.fft.fftshift(np.fft.fftfreq(N,dt))
    #Y = np.fft.fft(y)*[dt,1./N][pOpt]
    #f = np.fft.fftfreq(N,dt)
    #f[:int(N/2)],Y[:int(N/2)]
    return f,Y

def get_iFFT(f,F,df=0,pOpt=False):
    ''' pOpt : periodic option hence divide by sample size'''
    N,df = f.size,f[1]-f[0] #shape[0]
    y = np.fft.fftshift(np.fft.ifft(F)*[df*N,1][pOpt])
    t = np.fft.fftshift(np.fft.fftfreq(N,df))
    return t,y

def get_rFFT(t,y,dt,Tf=0):
    N = t.size
    Y = 2*np.fft.rfft(y,N)/N
    f = np.fft.rfftfreq(N,dt)
    return f,Y

def fftParams(dt,Tf,dopt=1):
    ''' Tf : total length in time of the signal '''
    df,fmax   = 1./Tf, 0.5/dt
    if dopt==1:
        printParams(['Tf','dt', 'df','fmax'],[Tf,dt,df,fmax],s=4)
    if dopt==2:
        printParams(['sx','dx', 'dX','Xmax'],[Tf,dt,df,fmax],s=4)
    return df,fmax

###########################################################################
#### def : display
def plot_fft2d(f,F,xy=None,kxy=None,figsize='12',pad=None):
    '''
    f : function 2D NxN ndarray
    F : fft2D(f)
    xy,kxy : extent in real and reciprocal spaces
    '''
    #fig,((axm,axM),(axp,axP))=plt.subplots(nrows=2,ncols=2)
    #plt.tight_layout()
    fig,((axm,axM),(axp,axP)) = create_fig(figsize,pad,rc='22')
    plot_ax2D(axm,np.real(f),'$|f|$',xy)
    plot_ax2D(axp,angle(F),'$\phi(F)$',kxy,'P')
    plot_ax2D(axM,np.abs(F)**2,'$|F|^2$',kxy,'F')
    plot_ax2D(axP,np.abs(F),'$|F|$',kxy,'F')
    fig.show()
    return fig
def plot_ax2D(ax,f,title='',extent=None,opt='P',cmap='jet',org='lower'):
    A=f #/f.max()#;print(A)
    vmin,vmax=A.min(),A.max()
    if opt == 'P' : vmin,vmax = 0,2*pi
    if opt == 'F' : vmin=min(A.min(),0)
    ax.imshow(A,cmap=cmap,origin=org,extent=extent)#,vmax=vmax, vmin=vmin)
    ax.set_title(title)

def displayFourier(f,Y,labs=[],labOpt='f',opt='RIYPS',ax=None,xlims=[],showOpt=1,fonts=[]):
    plts = {'R':[f,np.real(Y),'c','$Re$'], 'Y':[f,np.abs(Y)   ,'b','$||$'],
            'I':[f,np.imag(Y),'m','$Im$'], 'P':[f,np.angle(Y) ,'r','$\Phi$'],
            'S':[f,np.power(np.abs(Y),2),'g','$S$']}
    labs = {'t':['$t$','$y$'],'f':['$f$','$F_y$'],
            'x':['$x$','$y$'],'k':['$k$','$F_y$']}[labOpt]
    if isinstance(ax,np.ndarray):
        plots = [plts[p] for p in opt if p in 'RI']
        stdDispPlt(plots,labs,ax=ax[0],xlims=xlims,showOpt=0,fonts=fonts)
        plots = [plts[p] for p in opt if p in 'YPS']
        stdDispPlt(plots,labs,ax=ax[1],xlims=xlims,showOpt=showOpt,fonts=fonts)
    else :
        plots = [plts[p] for p in opt if p in 'RIYPS']
        stdDispPlt(plots,labs,ax=ax,xlims=xlims,showOpt=showOpt,fonts=fonts)

def compareFourier(f,Y,Yth,xlims=[0,5,0,1],showOpt=1):
    plots = [[f,np.abs(Y),'g'   ,'$|Y|$'     ],
             [f,Yth      ,'b--' ,'$|Y|_{th}$']]
    fig_c,ax=stdDispPlt(plots,['$f$','$Y$'],xlims=xlims,showOpt=showOpt)
    return fig_c


###########################################################################
#### def : Misc
def angle(x,ee=1e-10) :
    '''Prevents round off errors from polluting the phase'''
    return ((np.abs(x)>ee)*np.angle(x)+
            ((abs(np.real(x))<ee) & (abs(np.imag(x)>ee)))*pi/2*np.sign(np.imag(x))+
            ((abs(np.imag(x))<ee) & (abs(np.real(x)>ee)))*pi*np.sign(np.real(x))+
            2*pi) %(2*pi)
def getFourierPair(t,opt=0, f0=1.0,tau0=0.1,t0=0.0,phi0=0.0):
    fy = {'cos':lambda t:np.cos(2*pi*f0*(t-t0)+phi0),
          'sin':lambda t:np.sin(2*pi*f0*(t-t0)+phi0),
          'exp':lambda t:np.cos(2*pi*f0*(t-t0)+phi0)*np.exp(-np.power((t-t0)/(tau0/2),2)),
          'gau':lambda t:np.exp(-tau0*np.power(t,2))}
    y = fy[opt](t)
    return y
def get_extents(a,npts):
    dx=a/npts
    xy = [0,a]*2
    kxy = np.fft.fftshift(np.fft.fftfreq(npts,dx))[[0,-1]].tolist()*2
    return xy,kxy
def unit_impulse(n,i):
    y = np.zeros((n));y[i] = 1
    return y
def square(t,T,nT):
    N,nT0 = t.size,nT/2
    y = np.zeros((int(N/2)))
    t0=t+t[-1];t0=t0[t0<T*(nT0+0.5*nT%2)]
    if nT%2:
        y[t0%T>0.75*T] = 1
        y[t0%T<0.25*T] = 1
    else:
        y[t0%T>0.5*T] = 1
    if not N%2:
        y = np.concatenate((np.flipud(y),y))
    else:
        y = np.concatenate((np.flipud(y),y,np.array([0])))
    return y
def squareBis(t,T,nT,duty=0.5,applyScale=True):
    scale = [1,0.5][applyScale]
    if nT==np.Inf:
        y = scale*signal.square(2*pi*(t+0.25*T)/T,duty)+scale*applyScale
    else:
        if nT%2:
            y = scale*signal.square(2*pi*(t+0.5*duty*T)/T,duty)+scale*applyScale
        else:
            y = scale*signal.square(2*pi*(t+(duty+0.5*(1-duty))*T)/T,duty)+scale*applyScale
        y[t<-T*nT*0.5]=0;y[t>+T*nT*0.5]=0;
    return y

###########################################################################
#### def : test
###########################################################################
def testDisplayFourier():
    t = np.linspace(0,10,100)
    displayFourier(t,np.exp(2j*pi*t),opt='RIYP')
    displayFourier(t,np.exp(2j*pi*t),opt='RI')
    displayFourier(t,np.exp(2j*pi*t),opt='YP')
    displayFourier(t,np.exp(2j*pi*t),opt='Y')

def testFourier(y='gauss',params={'f0':0.0,'tau0':1.0,'t0':0,'phi0':0}):

    f0,tau0,t0,phi0 = [params.get(key) for key in ['f0','tau0','t0','phi0']]
    if y=='basic':
        yfunc,Yfunc = lambda t:np.exp(-t*t), lambda f:sqrt(pi)*np.exp(-pi**2*f*f)
        Fourier(yfunc,Tf=100,dt=0.01,fopt='s',Yfunc=Yfunc,dOpt='ft',pOpt='Y',
                xlims={'t':[-4,4,0,1],'f':[0,1,0,2]})
    if y=='gauss':
        Df  = 1.0/(pi*tau0/2);
        yfunc = lambda t:np.exp(2j*pi*f0*(t-t0)+1j*phi0)*np.exp(-np.power((t-t0)/(tau0/2),2))
        Yfunc = lambda f:sqrt(pi)*tau0/2*np.exp(-np.power((f-f0)/(Df),2))
        Fourier(yfunc,Tf=100,dt=0.01,fopt='s',Yfunc=Yfunc,dOpt='ftc',pOpt='RIY',
                xlims={'t':[-4,4,-1,1],'f':[0,4,0,1.5]})
    elif y=='cos':
        yfunc = lambda t:np.cos(2*pi*f0*(t-t0)+phi0)
        Yfunc = lambda f:unit_impulse(f.size,np.argmin(np.abs(f-f0)))
        Fourier(yfunc,Tf=100,dt=0.01,fopt='rp',Yfunc=Yfunc,dOpt='ftc',pOpt='R',
                xlims={'t':[0,5,-1,1],'f':[0,4,0,1]})
    elif y=='expi':
        yfunc = lambda t:np.exp(2j*pi*f0*(t-t0)+1j*phi0)
        Fourier(yfunc,Tf=100,dt=0.01,fopt='p',dOpt='ft',pOpt='RIY',
                xlims={'t':[0,5,-1.1,1.1],'f':[f0-0.1,f0+0.1,-0.1,1.1]})
def test_square():
    t,T = np.linspace(-10,10,1000),2
    Ns = [2,5,np.Inf]
    cs = getCs('jet',len(Ns))
    plots = [[t,squareBis(t,T,Ns[i],0.25,applyScale=False),cs[i],'$%s$' %Ns[i]] for i in range(len(Ns))]
    stdDispPlt(plots,['$t$','$y$'])

if __name__ =='__main__':
    #testDisplayFourier()
    #testFourier('basic')
    #testFourier('gauss',{'f0':0.0,'tau0':1.5,'t0':0.0,'phi0':0.0})
    #testFourier('cos'  ,{'f0':0.0,'tau0':1.5,'t0':0.0,'phi0':pi/3})
    #testFourier('expi' ,{'f0':2.0,'tau0':1.5,'t0':0.0,'phi0':pi/3})
    #test_square()
    print('FourierTest compiled');print("")
