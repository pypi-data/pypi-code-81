'''
Version 0.05

from MfP3 import putzer

from MfP3 import picard

from sympy.abc import x,y

from sympy import *

# Putzer

M = Matrix([[1,-1], [1,3]])

putzer(M)


# Picard

f = y**2

x0 = 0

y0 = 1

n = 3

picard(f,x0,y0,n)

'''

# Imports

from sympy.matrices import Matrix, eye, zeros, ones, diag

from sympy import pprint

from sympy.printing.latex import latex

from sympy.parsing.sympy_parser import parse_expr

from sympy import init_printing

from sympy import *

import sympy as sympy

from sympy.abc import x,y

# import console

from sympy import symbols

import math 

def putzer(M):
	
	result = {}

	M = Matrix(parse_expr(M, evaluate=False))

	init_printing()
	
	# Define matrix

	A = symbols('A')

	result["matrix"] = latex(Eq(S(A), M, evaluate = False))

	result["charpol"] = latex(M.charpoly().as_expr())

	eigen = M.eigenvals()

	nullstellen = [p for p in eigen.keys() for i in range(0,eigen[p])]

	result["nullstellen"] = nullstellen

	E = eye(int(math.sqrt(len(M))))

	mats = [E]

	result["p"] = [latex(Eq(S('P_0'),E, evaluate = False))]

	for i in range(0, len(nullstellen)):
		cm = (M - nullstellen[i]*E)*mats[i]
		result["p"].append(latex(Eq(S('P_' + str(i + 1)),cm, evaluate = False)))
		mats.append(cm)
	
	x = sympy.symbols('x')
	w1 = sympy.Function('w_1')
	ode = sympy.Eq(sympy.Derivative(w1(x),x),w1(x)*nullstellen[0])
	
	result["ode"] = [latex(ode)]
	
	sol = sympy.dsolve(ode,w1(x),ics={w1(0):1})
	rsol = sol.rhs


	result["ode_sol"] = [latex(sol)]

	funcs = [rsol]

	for i in range(1, len(nullstellen)):
		cf = sympy.Function('w_' + str(i + 1))
		ode = sympy.Eq(sympy.Derivative(cf(x),x),cf(x)*nullstellen[i] + funcs[i - 1])
		result["ode"].append(latex(ode))
		sol = sympy.dsolve(ode,cf(x),ics={cf(0):0})
		result["ode_sol"].append(latex(sol))
		rsol = sol.rhs
		funcs.append(rsol)
	
	erg = funcs[0]*mats[0]

	for i in range(1,len(nullstellen)):
		erg = erg + funcs[i]*mats[i]
	
	erg = simplify(erg)

	res = Eq(S('exp(xA)'), erg, evaluate = False)

	result["erg"] = latex(res)

	return result