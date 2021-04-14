import matplotlib.pyplot as plt

def bisect(f,a,b,args=(),rtol=1e-8, Nmax=100,v=1) : #,full_output=0):
    ''' Bisection method
    v : 1:warning if tol not met, 2:full_output with f0
    '''
    x0,N = float(a+b)/2,0
    args0 = (x0,)+args;
    f0 = abs(f(*args0))
    while f0>rtol and N<Nmax:
        x1 = (0.75*a + 0.25*b)
        x2 = (0.25*a + 0.75*b)
        args1,args2 = (x1,)+args, (x2,)+args
        f1,f2 = abs(f(*args1)),abs(f(*args2))
        if f1>f2 :
            a = x1
        else:
            if f2>f1:
                b = x2
            else:
                a = x1
                b = x2
        x0,N = (a+b)/2, N+1
        args0 = (x0,)+args
        f0 = abs(f(*args0))
    if v==1 :
        if f0>rtol:print('Warning tolerance not achieved f(x0)=%E,Nmax=%d'  %(f0,Nmax))
    if v==2 : return x0,f0
    return x0


def bissectionPos(f,a,b,tol=0.001, Nmax=100):
    x0,N = (a+b)/2,0
    while abs(f(x0))>tol and N<Nmax:
        #print abs(f(x0)),x0
        if  f(x0)>0:
            b = x0
        else:
            a = x0
        x0 = float(a+b)/2
        N+=1
    return x0,f(x0)

def bissection(f,a,b,tol=0.001, Nmax=100, plotOpt=0):
    x0 = float(a+b)/2
    N  = 0
    while f(x0)>tol and N<Nmax:
        x1 = (0.75*a + 0.25*b)
        x2 = (0.25*a + 0.75*b)
        if      f(x1)>f(x2):
            a = x1
        else:
            if f(x2)>f(x1):
                b = x2
            else:
                a = x1
                b = x2
        x0 = (a+b)/2
        N+=1
    return x0,f(x0)

def bissection2(f,a,b,tol=0.001, Nmax=100, plotOpt=0):
    x0 = float(a+b)/2
    N  = 0
    while abs(a-b)>tol and N<Nmax:
        x1 = (0.75*a + 0.25*b)
        x2 = (0.25*a + 0.75*b)
        if      f(x1)>f(x2):
            a = x1
        else:
            if f(x2)>f(x1):
                b = x2
            else:
                a = x1
                b = x2
        x0 = (a+b)/2
    return x0


def bissectionDebug(f,a,b,tol=0.001, Nmax=100, plotOpt=0):
    x0 = (a+b)/2
    N  = 0
    f0 = f(x0)
    f0s = [f0]
    while f0>tol and N<Nmax:
        x1 = (0.75*a + 0.25*b)
        x2 = (0.25*a + 0.75*b)
        if  f(x1)>f(x2):
            a = x1
        elif f(x2)>f(x1):
            b = x2
        else:
            a = x1
            b = x2
        x0 = (a+b)/2


        N  = N+1
        f0 = f(x0)
        f0s.insert(N,f0)
        #print x0

    if N==Nmax:
        print('''warning :'
                  bissection did not get to the required tolerance tol=%f
                  within the limited number of iterations Nmax=%d
              ''' %(tol,Nmax))
    if plotOpt:
        plt.plot(range(len(f0s)),f0s)
        plt.show()
    return x0,f(x0)

if __name__=='__main__':
##    f = lambda x:pow(x-1.0,2)
##    x0,f0 = bissection(f,0,1,0.001,12)
##    print('bissection result : %f with residual %f ' %(x0, f0))
##    x0,f0 = bissectionDebug(f,0,1,0.00001,100,1)

    print('Bissection compiled')
