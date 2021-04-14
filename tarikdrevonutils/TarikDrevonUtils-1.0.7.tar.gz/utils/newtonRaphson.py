import numpy as np
import matplotlib.pyplot as plt
from .displayStandards import*
from .glob_colors import*

def y_str(v):
    if isinstance(v,complex) or isinstance(v,np.complex128):
        return '%.3f+j%.3f' %(v.real,v.imag)
    elif isinstance(v,np.ndarray):
         return '['+' '.join(map(lambda s:'%.2E' %s,v))+']'
    else:
        return '%.3f' %v
def newton_recursive(f,df,x,y0,cond=None,Ncut=5,npts=3,tol=1e-5,nMax=100,v=1):
    ''' find roots of f(y,x) with Newton for fixed values of x (works both for 1D and N-D functions F):\n
    - x : ndarray - set of values at which netwton is computed
    - y0 : initial guess
    - cond : cond(x0,x1,y0,y1) functor - condition for accepting the solution (default accepted if f0<tol)
    - Ncut,npts : max cutback level and number of intermediate pts per cutback
    - v : verbose level(1 iterations for x, 2 cutback levels)
    - tol,nMax : Newton arguments
    '''
    if isinstance(y0,complex) or isinstance(y0,np.complex128):
        is_nd = 1
        y = np.zeros(x.shape,dtype=complex)
    elif isinstance(y0,list) or isinstance(y0,np.ndarray) :
        y0 = np.array(y0)
        is_nd = 2
        y = np.zeros((x.shape[0],y0.size),dtype=float)
    else:
        is_nd = 0 # default newton1D
        y = np.zeros(x.shape,dtype=float)
    newton_p = [newtonRaphson1D,newton_cplx,newton][is_nd]
    if not cond :
        cond = lambda x0,x1,y0,y1:True
        if v>1 : print('Newton recursive defaut condition')
    #check initial guess
    y0,f0  = newton_p(f,df,y0,(x[0],),tol,nMax=10000,v=1)
    if f0<tol :
        y[0] = y0
        if v :
            print(yellow+'\tNewton Raphson %s recursion log' %(['1D','cplx','ND'][is_nd]) + black)
            print(yellow+'  i : x     y     \n'+'-'*20+black)
            print(yellow+'%3d : %s %s' %(0,y_str(x[0]),y_str(y0)) +black)
    else :
        print(red+'bad initial guess :')
        print('x0=%s,y0=%s,f0=%E' %(y_str(x[0]),y_str(y0),f0))
        print('exiting'+black);return x
    #iterate
    i,valid = 1,f0<tol
    while i<x.size and valid:
        y0,valid = _newton_rec(0,f,df,x[i-1:i+1],y0,cond,newton_p,Ncut,npts,tol,nMax,v>1)
        if v : print(yellow+'%3d : %s %s' %(i,y_str(x[i]),y_str(y0)) +black)
        y[i],i = y0,i+1
    if not valid and v :
        print(red+'convergence issue : last point (invalid)'+black)
        print('x0=%s,y0=%s,f0=%E' %(y_str(x[i]),y_str(y[i]),f0))
    return y

def _newton_rec(n,f,df,x,y0,cond,newton_p,Ncut,npts,tol,nMax,v):
    ''' Solve recursively with Newton until found
    '''
    y1,valid = y0,False
    if n<Ncut:
        i,valid = 1,True
        if n and v: print(red+'cutback level %d for x=%.2f : ' %(n,x[-1]) +black,'new range : ',x)
        while i<x.size and valid :
            x0,x1,y0 = x[i-1],x[i],y1
            if n and v : print(red+'%3d : %.6f' %(i,x1)+black)
            y1,f1  = newton_p(f,df,y0,(x1,),tol,nMax,v=1)
            valid = f1<tol and cond(x0,x1,y0,y1)
            if not valid:
                y1,valid = _newton_rec(n+1,f,df,np.linspace(x0,x1,npts),y0,cond,newton_p,Ncut,npts,tol,nMax,v)
                # valid &= cond(x0,x1,y0,y1)
            i += 1
        if n and v :print([red,green][valid]+'cutback level %d %s' %(n,['fail','success'][valid])+black)
    return y1,valid

########################################################################
# Newton algos
def newton(f,df,x0,args=(),tol=1e-5,nMax=100,v=0):
    if isinstance(df,int):
        return newtonfdf(f,x0,args,tol,nMax,v)
    else:
        return newtonf(f,df,x0,args,tol,nMax,v)


def newtonfdf(fdf,x0,args=(),tol=1e-5,nMax=100,v=0):
    x,i = x0,0
    fx,dfx = fdf(x,*args)
    fxN = np.linalg.norm(fx)
    while fxN>=tol and i<nMax:
        fx,dfx = fdf(x,*args)
        # print(x,fxN,fx,dfx)
        dx = np.linalg.solve(dfx,fx)
        x -= dx
        fxN = np.linalg.norm(fx)
        i = i+1
    return [x,fxN,i][:v+1]

def newtonf(f,df,x0,args=(),tol=1e-5,nMax=100,v=0):
    x,i = x0,0
    fx,dfx = f(x,*args)
    fxN = np.linalg.norm(fx)
    while fxN>=tol and i<nMax:
        fx,dfx = f(x,*args),df(x,*args)
        # print(x,fxN,fx,dfx)
        dx = np.linalg.solve(dfx,fx)
        x -= dx
        fxN = np.linalg.norm(fx)
        i = i+1
    return [x,fxN,i][:v+1]

def newton_cplx(f,df,z0,args=(),tol=1e-7,nMax=100,v=0):
    ''' Newton for a complex valued function f(z)
    - f,df : functor f(z), df(z) - complex valued function and its derivative
    - z0 : complex - initial guess
    '''
    F  = lambda z:np.abs(f(z[0]+1J*z[1],*args))**2
    dF = lambda z:grad_fz2(f(z[0]+1J*z[1],*args), df(z[0]+1J*z[1],*args))

    z,i     = [z0.real,z0.imag],0
    fz      = F(z)
    while fz>=tol and i<nMax :
        dfz = dF(z)
        # print(z[0]+1J*z[1],fz,dfz)
        z -= dfz*fz/np.linalg.norm(dfz)**2
        fz = F(z)
        i = i+1
    out = [z[0]+1J*z[1],fz,i]
    return out[:v+1]
def grad_fz2(fz,dfz):
    u,v = fz.real,fz.imag
    ux,vx = dfz.real,dfz.imag
    return np.stack([2*u*ux + 2*v*vx,-2*u*vx+2*v*ux])


def newtonRaphson1D(f,df,x0,args=(),tol=0.01,nMax=10,v=0):
    x,i     = x0,0
    #argsx   = (x,)+args
    fx      = f(x,*args)
    while abs(fx)>=tol and i<nMax :
        print(x,fx,df(x,*args))
        x = x - fx/df(x,*args)
        #argsx = (x,)+args
        fx = f(x,*args)
        i = i+1
    X = [x,abs(fx),i]
    return X[:v+1]

############################################################
#### def : Efficient
def newtonRaphsonEff(fdf,x0,tol=0.01,nMax=10):
    x,i = x0,0
    fx,dfx = fdf(x)
    fxN = np.linalg.norm(fx)
    while fxN>=tol and i<nMax:
        fx,dfx = fdf(x)
        dx = np.linalg.solve(dfx,fx)
        x = np.subtract(x,dx)
        fxN = np.linalg.norm(fx)
        i = i+1
    return x

def newtonRaphson1DEff(fdf,x0,tol=0.01,nMax=10):
    x,i  = x0,0
    fx,dfx = fdf(x)
    while abs(fx)>=tol and i<nMax:
        x = x - fx/dfx
        i = i+1
        fx,dfx = fdf(x)
    return x

############################################################
#### def : Debug
def newtonRaphson_dbg(f,df,x0,args=(),tol=0.01,nMax=10,v=0):
    x,i,xi = x0,0,[]
    argsx = (x,)+args
    fx = np.linalg.norm(f(*argsx))
    while fx>=tol and i<nMax:
        xi += [np.array(x)]; print(xi)
        dfx = df(*argsx)
        dfinv = np.linalg.inv(dfx)
        dx = dfinv.dot(f(*argsx))#np.linalg.solve(df(*argsx),f(*argsx))
        print(red,x,black);print(dfx);print(dfinv);print(f(*argsx));print(dx);print(fx)
        x -= dx # np.subtract(x,dx)
        argsx = (x,)+args
        fx = np.linalg.norm(f(*argsx))
        i = i+1
    xi+=[np.array(x)]
    #X = [x,fx,i]
    return np.array(xi) #X[:v+1]
def newtonRaphsonDebug(f,df,x0,tol=0.01,nMax=10):
    x = x0
    fx = np.linalg.norm(f(x))
    print(fx);plt.plot(x,'o-');
    i = 0
    while fx>=tol and i<nMax:
        dx = np.linalg.solve(df(x),f(x))
        x = np.subtract(x,dx)
        fx = np.linalg.norm(f(x))
        i = i+1
        print(fx);plt.plot(x,'o-',color=(1-fx/tol,0,0));
    return x,fx,i
def newtonRaphson1Ddebug(f,df,x0,X,tol=0.01,nMax=10,logOpt=0):
    fX      = np.log10(abs(f(X))) if logOpt else f(X)
    plots   = [[X ,fX ,'b-','$f(x)  $']]

    dispIntermediateSol(plots,x0,f,'r',tol,logOpt)
    x,i = x0,0
    while abs(f(x))>=tol and i<nMax:
        x = x - f(x)/df(x)
        i = i+1
        dispIntermediateSol(plots,x,f,'b',tol,logOpt)
    dispIntermediateSol(plots,x,f,'g',tol,logOpt)

    stdDispPlt(plots,['x','fx'],xlims=['y',-100.,100.])
    return x,f(x),i


############################################################
#### def : Misc
def dispIntermediateSol(plots,x,f,c,tol,logOpt=0):
    fx = f(x)
    if logOpt:
        logTol  = abs(np.log10(tol))
        logFx   = logTol if fx<=tol else abs(np.log10(abs(fx)))
        #c       = abs(pow(logFx/logTol,0.3))
        fx      = abs(logFx)
    print(x, fx)
    plots.append([x,fx,c+'o',''])
    return plots

def f_cplx(f,z,z0):
    z = z[0]+1J*z[1]
    fz = f(z,z0)
    return np.array([fz.real,fz.imag])

def j_cplx(df,z,z0):
    z = z[0]+1J*z[1]
    df_z,dfz_ = df(z,z0),df(np.conj(z),z0)
    jac = [ [df_z+dfz_      ,  1J*(df_z+dfz_)],
            [-1J*(df_z-dfz_),       df_z-dfz_], ]
    jac = 0.5*np.array(jac)
    print('real :\n' ,jac.real)
    print('imag :\n' ,jac.imag)
    return jac #.real

############################################################
##### def : Tests
def _newtonExample(debugOpt=0):
    print('\t')                         ;print('Newton Raphson ' )
    f  = lambda x:[pow(x[0],2)-1,x[1]]  ;print("f(x)  = [x(0)^2-1,x(1)] ")
    df = lambda x:[[2*x[0]  ,0],
                   [0       ,1]]        ;print("df(x) = [[2*x(0)^2,0] \n"
                                           "         [0       ,1]]")
    x0 = [2,2]                          ;print("x0 = [2,2]")
    x = newtonRaphson(f,df, x0)         ;print("x  = " + valsToStr(x[0]))
    if debugOpt:
        X = np.meshgrid(np.linspace(0,2,10),np.linspace(0,2,10))
        fX = f0(X)
        plt.plot();plt.show()
def _newtonExample1D(debugOpt=0,logOpt=0):
    x0 = [-2.,2.5]
    print('\t')                     ;print('Newton Raphson 1D ' )
    f  = lambda x:pow(x,2)-1        ;print('f  = x^2-1')
    df = lambda x:2*x               ;print('df = 2*x')
    x  = newtonRaphson1D(f,df,x0[0]);print('x0=%-3.2f => x =%.2f'  %(x0[0],x[0]))
    x  = newtonRaphson1D(f,df,x0[1]);print('x0=%-3.2f => x =%.2f'  %(x0[1],x[0]))

    if debugOpt:
        X = np.linspace(-3,3,1002)
        newtonRaphson1Ddebug(f,df,x0[1],X,tol=pow(10.,-12),nMax=10,logOpt=logOpt)

def _newtonExample1DdebugQuick():
    f  = lambda x:pow(x,3)-1
    df = lambda x:3*pow(x,2)
    X  = np.linspace(-3,3,1000)
    x  = newtonRaphson1Ddebug(f,df,-10.,X,tol=pow(10.,-5),nMax=20,logOpt=0);
    print(x)

######################################################################
if __name__=='__main__':
    import numpy as np
    #newtonExample(0)
    #newtonExample1D(debugOpt=1,logOpt=0)
    #newtonExample1DdebugQuick()
    print('succesful compilation')
