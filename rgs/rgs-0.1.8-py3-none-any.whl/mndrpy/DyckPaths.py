'''
Created on Mar 12, 2021

@author: vladislavkargin

A collection of functions for Dyck paths.
A Dyck path is an array of +1 and -1, such that the total sum is zero and 
the partial sums are always non-negative. 
'''
import numpy as np
import matplotlib.pyplot as plt


def randomDyckPath(n, seed = None):
    '''
     * Generates a random Dyck path with 2n steps
     * 
     * @param n half-size of path
     * @return a sequence of -1 and 1 steps.
    '''
    
    if seed != None:
        np.random.seed(seed)
    path = [1] * n + [-1] * (n + 1)   
    #shuffle randomly
    np.random.shuffle(path)
    
    #do a cyclic shift. 
    #Find the first occurrence of the minimum
    S = np.cumsum(np.array([0] + path))
    '''
    fig1, ax1 = plt.subplots(nrows=1, ncols=1)
    ax1.plot(S)
    ax1.grid(True)
    '''
    m = np.min(S)
    positions = np.where(S == m)[0]
    pos = positions[0]
    #print(pos)
    path1 = path[pos:] + path[:pos]
    del path1[-1]
    return path1

def plotDyckPath(path, ax = None, method = "upperLatticePath"):
    ''' plots a Dyck path. Path is either list of 1, -1 or numpy array
    of 1, - 1'''
    if isinstance(path, list):
        n = int(len(path)/2)
    else:
        n = int(path.shape[0]/2)
    X, Y = buildPlanePath(path, method = method)
    if ax == None:
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
    major_ticks = np.arange(0, n + 1, 1)
    #minor_ticks = np.arange(0, 101, 5)
    ax.set_xticks(major_ticks)
    #ax.set_xticks(minor_ticks, minor=True)
    ax.set_yticks(major_ticks)
    #ax.set_yticks(minor_ticks, minor=True)
    # And a corresponding grid
    ax.grid(which='both')
    ax.plot(X, Y)
    Z = range(n + 1)
    ax.plot(Z)
    return ax  


def areaDyckPath(path):
    ''' calculate the area of the given Dyck path, defined as the number
    of unit squares under the path but above the line y = x'''
    if isinstance(path, list):
        n = int(len(path)/2)
    else:
        n = int(path.shape[0]/2)
    x = 0
    y = 0
    S = [(x, y)]
    for i in range(2 * n):
        if path[i] == 1:
            y += 1
        else:
            x += 1
        S.append((x,y))
    area = 0
    y_prev = 0
    for p in S: #every time as y increases, we add y - x - 1 to the area
        if p[1] > y_prev:
            area += p[1] - p[0]- 1
            y_prev = p[1]
    return area

def nvalleysDyckPath(path):
    '''counts the number of valleys of the given Dyck path '''
    if isinstance(path, list):
        n = len(path)//2 
    else:
        n = path.shape[0]//2
    nvalleys = 0
    for i in range(2 * n - 1):
        if path[i] == - 1 and path[i + 1] == 1:
            nvalleys += 1
    return nvalleys


def buildPlanePath(path, method = 'upperLatticePath'):
    ''' creates the path in the plane '''
    if isinstance(path, list):
        n = int(len(path)/2)
    else:
        n = int(path.shape[0]/2)
    x = 0
    y = 0
    S = [(x, y)]
    if method == "upperLatticePath":
        for i in range(2 * n):
            if path[i] == 1:
                y += 1
            else:
                x += 1
            S.append((x,y))
    else:         
        for i in range(2 * n):
            if path[i] == 1:
                x += 1
            else:
                y += 1
            S.append((x,y))
    #print(S)
    X, Y = list(zip(*S)) 

    return X, Y

def pathTo231perm(path):
    '''converts a Dyck path to 231 avoiding permutation
    I am using the description of the bijection from Peterson's "Eulerian paths"
    '''
    #TODO
    #first build the reflected path 
    X, Y = buildPlanePath(path, method = 'lowerLatticePath')
    n = (len(X) - 1)//2
    #One-by-one, for every column from right to left,
    #Find the lowest unoccupied row
    perm = [0] * n 
    used_rows = []
    for x in reversed(range(1, n + 1)):
        y = Y[X.index(x)] # this is the bound from below that the path gives us
        while y in used_rows:
            y += 1
        used_rows.append(y)
        perm[x - 1] = y
    return perm
    

'''
For testing methods
'''
def main():
    
    n = 5
    seed = 3
    path = randomDyckPath(n, seed = seed)
    plotDyckPath(path, method = 'upperLatticePath')
    perm = pathTo231perm(path)
    print(perm)
    
    plt.show()
    
    pass

if __name__ == '__main__':
    main()