import numpy as np

def finiteGrad(func, x0, step):
    """This function returns the jacobian of function 'func', at the location specified by 'x0', using the forward step method
    
    ATTRIBUTES:
    func (function): Function to perform complex differentiation
    x0 (float list/array): Location to calculate gradient of function 'func'
    step (float): Step-size
    
    EXAMPLE:
    finiteGrad(lambda x : x**2, [1], 10**-7)
    """
    x0 = np.array(x0)
    xLength = len(x0)
    fVal = np.array(func(x0))
    h = step
    hMatrix = np.eye(xLength)*h
    return np.array([(func(x0+np.squeeze(hMatrix[n,:]))-fVal)/h for n in range(xLength)]).T

def complexGrad(func, x0):
    """This function returns the jacobian of function 'func', at the location specified by 'x0', using the complex step method
    
    ATTRIBUTES:
    func (function): Function to perform complex differentiation
    x0 (float list/array): Location to calculate gradient of function 'func'
    
    EXAMPLE:
    complexGrad(lambda x : x**2, [1])
    
    IMPORTANT:
    Make sure that the function 'func' has been properly modified for the complex-step differentiation method.
    """
    xLength = len(x0)
    h = 10**-30 #step size (arbitrarily small, no need to modify)
    hMatrix = np.eye(xLength)*h
    return np.array([np.imag(func(x0+1j*np.squeeze(hMatrix[n,:])))/h for n in range(xLength)]).T

def nDimNewton(func, x0, fprime, tol=10**-6, maxiter=50, xlim=None, heh=True, hehcon=None):
    """This is the root finding Newton Method for n-dimensions
    
    ATTRIBUTES:
    func (function): n-dim function to find root for, where n > 1
    x0 (float list/array): Initial estimate
    fprime (function): Function returning the Jacobian matrix
    tol (float): Tolerance for the zero value (default to 10**-6)
    maxiter (float): Maximum number of interations (default to 50)
    xlim (array): Inclusive limits to raise an exception for x, in the form of np.array([[x[0]_lower, x[0]_upper], [x[1]_lower, x[1]_upper], ...]) (default to None)
    heh (boolean): Heuristic error handling (default to True)
    hehcon (function): Constraint for heuristic error handling, namely assuring that hehcon(x)<=0 during iterations. This is used to keep func inside a valid domain during interations, not to constrain the solution (default to None)
    """
    #Initialize values
    k = 1 #Iteration count
    x = x0
    xOld = None
    f = func(x)
    
    if heh and hehcon is not None and any(np.asarray(hehcon(x)) > 0):
        raise RuntimeError("Initial estimate, x0, does not satisfy hehcon(x0)<=0. Try a different x0.")
    
    while np.linalg.norm(f) > tol:
        Df = fprime(x)
        
        if heh:
            #Check if gradient is full rank and try to correct if not
            while np.linalg.matrix_rank(Df) < len(Df):
                if xOld is not None:
                    xNew = (x+xOld)/2 #Bisection backtracking
                    x = xNew
                    Df = fprime(x)
                else:
                    raise RuntimeError("Intial estimate, x0, does not produce a full rank Jacobian. Try a different x0.")
        xOld = x
        
        g = func(x)
        
        v = -np.linalg.solve(Df,g)
        
        if xlim is not None:
            #Check if result is out of the user-defined limits
            runaways = [['x['+str(i)+']' for i in range(len(x)) if x[i]<=xlim[i,0] and v[i]<0], ['x['+str(i)+']' for i in range(len(x)) if x[i]>=xlim[i,1] and v[i]>0]]
            if any(runaways):
                message = 'No solution found. Iteration stopped because the following variables were found to be outside the user-defined limits:\n'
                if runaways[0]:
                    message += ', '.join(runaways[0]) + ' <= lower bound/n'
                if runaways[1]:
                    message += ', '.join(runaways[1]) + ' >= upper bound/n'
                raise RuntimeError(message)
        
        x = x + v
        
        if heh and xlim is not None:
            #Force constraints
            for i in range(len(x)):
                if x[i] < xlim[i,0]:
                    x[i] = xlim[i,0]
                elif x[i] > xlim[i,1]:
                    x[i] = xlim[i,1]
            
        #Exit loop if maximum allowed iterations is reached
        if k == maxiter:
            raise RuntimeError('Solution did not converge after the maximum number of iterations.')
        else:
            k += 1
        
        f = func(x) #Evaluate function at new point
        
        if heh and hehcon is not None:
            while any(np.asarray(hehcon(x)) > 0):
                xNew = (x+xOld)/2 #Bisection bactracking
                x = xNew
                f = func(x)
        
    return x