from sympy import exp,log,symbols,oo,integrate
x=symbols('x')

def test():
    I=integrate(x**2*exp(-x),(x,0,oo))
    print(I)

if '__main__'==__name__:
    test()
