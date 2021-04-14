from FourierUtils import*
from displayStandards import*
from scipy import signal


#__all__=['base_test']
def base_test():
    ''' Show the Fourier transform of a square in  '''
    Tf,dt = 10, 0.01
    T,nT,duty = 1,1,1

    yfunc = lambda t:np.array(squareBis(t,T,nT,duty),dtype=complex)
    t,y,f,Y = Fourier(yfunc,Tf=Tf,dt=dt,
                      fopt='',dOpt='fts',pOpt='RIYP',
                      labOpts=['x','k'],
                      xlims={'t':[-10,10,-0.1,1.1],'f':[]})

def test_showCase():
    Tf,dt = 10000, 0.1
    T,nT,duty = 10,20,0.2

    t = np.arange(0,Tf+dt,dt) - Tf/2
    fig,ax = plt.subplots(2,1)

    y = squareBis(t,10,50,duty=0.2)
    y0 = squareBis(t,1000,1,duty=0.5)
    yF = squareBis(t,10,100,duty=0.2)
    Ts  = np.arange(0,Tf+dt,T) - Tf/2; nTs = Ts.size;Ts = np.array([Ts,Ts])
    #ax[0].plot(Ts,[0,1],'g--',label=''      ,alpha=0.25,linewidth=0.5)
    ax[0].plot(t,yF,'b'  ,label='periodic'  ,alpha=0.15,linewidth=0.75)
    ax[0].plot(t,y,'b'   ,label='$f(x)$'    ,alpha=1.0,linewidth=0.75)
    ax[0].plot(t,y0,'r',label='$y_0$'       ,alpha=0.5,linewidth=2.0)

    standardDisplay(ax[0],['$x$','$f$'],opt='q',axPos=22,xylims=[-500,500,0,1.2]) #,xyTickLabs=[[''],['']])

    f,Y = get_FFT(t,y,dt)
    f0,Y0 = get_FFT(t,y0,dt)

    Y = abs(Y)**2;          Ym=Y.max()
    Y0 = abs(Y0)**2;        Y0*=Ym/Y0.max()

    x0  = np.arange(-5,5.1,0.1)
    FF = np.sinc(2*f)**2*Ym
    FF0 = np.sinc(2*x0)**2*Ym
    ax[1].plot(f,FF    ,'b--' ,label='$sinc^2$',alpha=0.4,linewidth=3.0)
    ax[1].plot(x0,FF0  ,'bo'  ,label=''        ,alpha=0.4,markersize=15)
    ax[1].plot(f,abs(Y),'b'   ,label='$F(f)$'  ,alpha=1.0,linewidth=2.0)
    ax[1].plot(f0,Y0   ,'r'   ,label='$Y_0$'   ,alpha=1.0,linewidth=1.0)

    standardDisplay(ax[1],['$X$','$|F|^2$'],opt='q',axPos=21,xylims=[-1,1,0,1.1*10000])
    ax[0].xaxis.set_ticklabels([])
    ax[0].yaxis.set_ticklabels([])
    ax[1].xaxis.set_ticklabels([])
    ax[1].yaxis.set_ticklabels([])
    plt.show()

if __name__=="__main__":
    base_test()
    #test_showCase()
