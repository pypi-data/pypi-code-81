import numpy as np
import time

__all__ = ["rescale_for_vis"]

def rescale(values, relations=None, atol=1e-10,verbose=0):

    if len(values) <= 1:
        return np.array(values)

    if verbose:
        start = time.time()

    values = np.array(values).astype(float)
    values.sort()
    n = len(values)-1 #len diff, dimesion of vector space

    #the position vector (in the space of differences between levels)
    s = np.diff(values)
    minidiff = np.min(s[np.nonzero(s)])
    s /= minidiff

    #initialize the position matrix with zeros on the diagonal and above
    # and increasing values to the lower left
    M = np.zeros((n+1,n+1),dtype=float)
    for i in range(n):
        M[i+1:,:i+1] += s[i]

    #we're done with s, from now on we 
    # only care about the velocity vector.
    # And we start walking towards the origin
    v = - s
    #the velocity matrix
    A = - M.copy()

    #zeroth step of the algorithm, take care of the smallest difference
    # and differences equal to zero
    normals = np.zeros((n,n),dtype=int)

    # #imprecise alternative #TODO: decide whether or not to use this alternative
    # #zeroth step of the algorithm, take care of the smallest difference
    # # and differences equal to zero
    # normals = np.zeros((n,n),dtype=float)

    counter = 0 #counts normals
    for i in range(n):
        if v[i] in [0,-1]:
            A[i+1:,:i+1] -= v[i]
            v[i] = 0
            normals[counter,i] = 1#normal
            counter += 1
        else:
            A[i+1:,:i+1] += 1

    tri_n = n*(n+1)//2 #the n'th triangular number

    #each iteration we hit at least one boundary condition
    for iteration in range(n): 
 
        #set c (short for constant or coefficient)
        cs = np.zeros(tri_n**2, dtype=float)
        indices = np.zeros((tri_n**2,2,2),dtype=int)
        k = 0
        tril = np.tril_indices(n+1,k=-1) #tril is a tuple of indices
        for first in range(tri_n):
            for second in range(tri_n):
                i = (tril[0][first],tril[1][first])
                j = (tril[0][second],tril[1][second])
                if A[i] >= A[j] :  # TODO: maybe I should just exclude zero to be save, 
                                   #       maybe a new condition will be stepped over
                    continue
                cs[k] = - (M[i]-M[j]) / (A[i]-A[j])
                indices[k,0,:] = i#i M[i] darf nicht kleiner werden, deshalb wird A[i] geändert
                indices[k,1,:] = j 
                k += 1

        big_cs = cs[cs>0] #TODO: this line might cause trouble, 
                          #      because a new condition is stepped over because of numerical errors
        big_cs.sort()
        for c in big_cs:

            #M[i] is not allowed to get smaller than M[j]
            #these are getting small to fast
            positions = indices[cs == c,0,:]
            #these values would be too big
            qositions = indices[cs == c,1,:] # yes, this is a bad name

            new_constraints = False
            #in practice len(positions) = 1
            for (p_row, p_col),(q_row,q_col) in zip(reversed(positions),reversed(qositions)):
                
                #remember the row has always the greater index
                if relations is not None:
                    move_on = True
                    for relation in relations:
                        if [p_row,p_col] in relation and [q_row, q_col] in relation:
                            move_on = False
                            break
                    if move_on:
                        continue

                normal = np.zeros(n,dtype=int)
                # #imprecise alternative
                # normal = np.zeros(n,dtype=float)
                for i in range(n):
                    if p_col <= i <= p_row -1:
                        normal[i] += 1
                    if q_col <= i <= q_row -1:
                        normal[i] -= 1

                #modified Gram-Schmidt 
                for a in normals[:counter]:
                    normal *= a@a #avoid floating point devision
                    if normal@normal < 0:
                        raise RuntimeError("Encountered integer overflow. "
                                        + "Try a smaller list of numbers. "
                                        + "Or group the data into a list of lists.")
                    normal -= (normal@(a)) *(a)  // (a@a)
                    if normal@normal != 0:
                       normal = normal // np.gcd.reduce(normal) #avoid integer overflow

                # #imprecise alternative:
                # #modified Gram-Schmidt 
                # for a in normals[:counter]:
                #     normal -= (normal@(a)) *(a)  / (a@a)

                #if there is no new constraint, don't change v
                if normal@normal != 0:
                # #imprecise alternative:
                # #if there is no new constraint, don't change v
                # if normal@normal >= 1e-13:
                    new_constraints = True
                    normals[counter] = normal
                    counter += 1

                    #projection onto a subspace
                    #modified Gram-Schmidt process
                    unit_normal = normal / np.linalg.norm(normal)
                    v -= (v @ unit_normal) * unit_normal 

                    #update velocity matrix
                    new_A = np.zeros_like(A)
                    for i in range(n):
                        new_A[i+1:,:i+1] += v[i]

            if new_constraints:
                #this is the main step, update the position matrix
                M += c * A
                A = new_A
                break
            else:
                #probably c was small and sould have been zero,
                # try the next one
                if verbose:
                    print(f"iteration = {iteration} and c = {c} no new constraint")
        else:
            #if you weren't able to find a new constraint at all, well then you're done
            if verbose:
                print("terminated on iteration: ",iteration)
            break
        if abs(A[n,0]) < atol:
            if verbose:
                print("lower left corner of A:")
                print(A[n-2:,:2])
                print("terminated on iteration: ",iteration)
            break
        
    else:
        print("levels so far: ",M[:,0])
        raise RuntimeError("The algorithm did not converge.")

    if verbose:
        end = time.time()
        print("n:",n)
        print("time:",end-start)
        print("normals:")
        print(normals)
    return M[:,0]

def rescale_for_vis(data,relations=None,atol=1e-10,verbose=0):
    """data (numpy array or list): eiter a list of numbers or a list of list of numbers, that should be redistributed
    atol (flaot): absolute tolerance criteria for the termination of the algorithm
    verbose (0 or 1): 1: print some information, 0: print none
    relations (list): Provide lists of index pairs, each corresponding to a difference.
                      The order of magnitudes is only preserved when differences are within the same list.
                      e.g. [  [[1,0]]  [[2,1],[2,0]]]  [4,3],[5,4],[5,3],[5,2]]  ]
                      If The difference [2,1] starts out smaller than [2,0] it will stay that way.
    return either numpy array (in case the input was a list of numbers) or list of numpy arrays (input was a list of lists)"""
    #bundle multiple lists to processed together by rescale_for_vis.
    #TODO decide whether or not the bundling and cutting of lists should 
    # be left to the user.
    if len(data) == 0:
        return np.array(data)



    list_got_wrapped = False
    if isinstance(data[0],list) or isinstance(data[0],np.ndarray):
        cuts = []
        for values in data:
            cuts.append(len(values))

        #we add three types of relation
        # - sequential
        # - inner-group alias group
        # - inter-group alias diffs_and_sizes
        if relations:
            raise ValueError("When specifing relations the data must be a flat list of numbers.")
        relations = []

        diffs_and_sizes = []
        prev_cut = 0
        for c in range(len(cuts)):
            cut = cuts[c]
            group = []
            for i in range(prev_cut+1,prev_cut+cut):
                for j in range(prev_cut,i):
                    group.append([i,j])
            relations.append(group)
            #diffs_and_sizes.append([i,prev_cut])# only sizes of groups
            prev_cut += cut

        #diff_and_sizes
        cumsum = np.cumsum([0]+cuts[:c+1])
        for i in range(1,len(cumsum)):
            for j in range(i):
                diffs_and_sizes.append([cumsum[i]-1,cumsum[j]]) #diffs
                if j > 0:
                    diffs_and_sizes.append([cumsum[i-1],cumsum[j]-1]) #diffs + sizes
        relations.append(diffs_and_sizes)

        #sequential
        sequential = []
        N = sum(cuts)
        for i in range(N-1):
                sequential.append([i+1,i])
        relations.append(sequential)

    else:
        data = np.array([data])
        list_got_wrapped = True
        cuts = []
        for values in data:
            cuts.append(len(values))

    values = np.hstack([*data])
    order = values.argsort()
    old_order = order.argsort()
    values = values[order]
    levels = rescale(values,relations, atol,verbose) #here is the action
    levels = levels[old_order]
    data_levels = []
    prev_cut = 0
    for cut in cuts:
        cut += prev_cut
        levels_slice = levels[prev_cut:cut]
        data_levels.append(levels_slice)
        prev_cut = cut
    if list_got_wrapped:
        data_levels = data_levels[0]
    return data_levels
