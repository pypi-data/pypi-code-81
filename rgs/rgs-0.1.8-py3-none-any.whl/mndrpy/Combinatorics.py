'''
Created on Aug 14, 2020

@author: vladislavkargin
'''
import rgs.mndrpy.Meander as Meander
import rgs.mndrpy.Utility as ut
#import rgs.mndrpy.Pairing as pg
import rgs.mndrpy.DyckPaths as dp


import numpy as np
import itertools 
import matplotlib.pyplot as plt
#from progress.bar import Bar


def cyclesOfPerm(perm):
    ''' calculates all cycles in the permutation perm. 
    For, example if the permutation is 102534, then return a list of 
    [01][2][354]. Currently, the order of cycles and the order inside cycles are NOT
    normalized to the standard order defined in Ennumerative Combinatorics by Stanley.
    '''
    cycles = []
    elements = list(range(len(perm)))
    while len(elements) > 0:
        cycle = []
        i = elements[0]
        elements.remove(i)
        cycle.append(i)
        j = perm[i]
        while j != i:
            elements.remove(j)
            cycle.append(j)
            j = perm[j]
        cycles.append(cycle)
    return cycles
        
def cycleLengths(perm):
    '''caclullates cycle lengths for a permutation. returns them in 
    decreasing order (as a partition of the length of the permutation'''
    cycles = cyclesOfPerm(perm)
    y = np.sort(list(map(len, cycles)))
    y = y[::-1]
    return y     

def enumPropMeanders(n):
    ''' enumerates proper Meanders on [2n]. (Obviously, n cannot be too large.)
    '''
    meanders = set([])
    for uPrng in ut.genPairings(n):
        for dPrng in ut.genPairings(n):
            mndr = Meander.Meander(uPrng, dPrng)
            if mndr.isProper():
                meanders.add(mndr)
    return meanders       

def enumIrrMeanders(n):
    ''' enumerates irreducible Meanders on [2n]. (Obviously, n cannot be too large.)
    NB. The definition that I use is different from the definition used by Zvonkin-Lando,
    in their paper about meanders,  
    so this is more of exploratory character.
    '''
    meanders = set([])
    for uPrng in ut.genPairings(n):
        for dPrng in ut.genPairings(n):
            mndr = Meander.Meander(uPrng, dPrng)
            if mndr.isIrreducible():
                meanders.add(mndr)
    return meanders     

def rotationNumber(cycle):
    '''calculate the rotation number for a cycle
    The input is a permuted list of numbers from 0 to 2n - 1 that starts with 0.
    It represents a cycle in the plane (a meander with self-intersections allowed)
    For example (0 2 1 3) represents a cycle formed by arcs (0 2) and (1 3) in 
    the upper-halfplane and arcs (2 1) (3 0) in the lower half-plane
    The function returns the rotation number for this cycle. For example, for this
    cycle the rotation number is 2. For non-crossing meanders the rotation number
    is always 0. '''
    if len(cycle)%2 != 0:
        print("Rotation Number says: The length of the cycle must be even!")
        return
    n = int(len(cycle)/2)
    #print(n)
    rn = 0
    for i in range(2*n):
        if cycle[(i + 1)%(2*n)] > cycle[i]:
            rn = rn + (-1)**(i%2)
        else:
            rn = rn - (-1)**(i%2)
    return int(rn/2) 
    

def random231perm(n):
    ''' generates a random 231 permutation of n objects, like 3 0 2 1 for n = 4'''
    path = dp.randomDyckPath(n)
    p = dp.pathTo231perm(path)
    return p   

    
    

    
'''
For testing methods
'''
def main():
    #n = 7
    n = 4
    meanders = enumPropMeanders(n)
    print(len(meanders))
    #print(list(map(str,meanders)))
    
    meanders = enumIrrMeanders(n)
    print(len(meanders))
    #print(list(map(str,meanders)))
    
    print(list(itertools.permutations(range(1,n))))
    cycle = [0, 1, 5, 2, 4, 3]
    mndr = ut.makeMeanderFromCycle(cycle)
    print(mndr)
    mndr.draw()
    rn = rotationNumber(cycle)
    print("Rotation number = ", rn) 
    
    cycle = [0, 5, 1, 4, 2, 3]
    mndr = ut.makeMeanderFromCycle(cycle)
    print(mndr)
    mndr.draw()
    rn = rotationNumber(cycle)
    print("Rotation number = ", rn) 
    
    
    #a random 231 permutation 
    n = 100
    p = random231perm(n)
    print(p)
    plt.figure()
    plt.plot(p,'*')
    plt.grid()

    cycles = cyclesOfPerm(p)
    print(cycles)
    print(cycleLengths(p))    
    
    

    
    plt.show()

if __name__ == '__main__':
    main()