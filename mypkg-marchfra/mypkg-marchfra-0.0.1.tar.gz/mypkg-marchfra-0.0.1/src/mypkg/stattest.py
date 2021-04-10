def calc_chisquare(func, x, y, xerr=None, yerr=None, pars=None):
	'''
	This function calculates the chi square value for a set of data and a fit on that data.
	Args:
	- func (function) : the model function
	- x (numpy.ndarray) : the values on the x-axis
	- y (numpy.ndarray) : the values on the y-axis
	- xerr (numpy.ndarray) : the errors on the x-axis. Defaults to no error
	- yerr (numpy.ndarray) : the errors on the y-axis. Defaults to no error
	- pars (numpy.ndarray) : the parameters of the fitted function. Defaults to no parameters
	Returns:
	- chisq (float) : chi square value
	- NDF (int) : number of degrees of freedom
	- p (float) : p-value
	'''
	import numpy as np
	from scipy.misc import derivative
	from scipy.stats import chi2

	if pars is None:
		num = (y - func(x))**2
	else:
		num = (y - func(x, *pars))**2

	if xerr is None:
		if yerr is None:
			den = 1
		else:
			den = yerr**2
	else:
		if yerr is None:
			raise TypeError("You shouldn't have an error on x only")
		if pars is None:
			den = yerr**2 + (xerr * derivative(func, x, dx=0.001))**2
		else:
			den = yerr**2 + (xerr * derivative(func, x, args=pars, dx=0.001))**2

	chisq = np.sum(num / den)
	NDF = len(x) - len(pars)
	p = chi2.sf(chisq, NDF)
	return chisq, NDF, p
