'''
Function to evaluate the impact of different pre-processing techniques and their combinations on NIR spectral data to predict Y variables

Script seperated into two parts

- First part:
    functions used to create different combinations of pre-processing techniques and applying them to data
    
- Second part: 
    function comparing pre-processing techniques using multiblock partial least squares (MBPLS)
    
'''

import numpy as np
import matplotlib.pyplot as plt
import copy
import itertools
import RG as rg # Ryan Gosselin's module containing pre-processing techniques

#%%
# ----------------- First part -----------------------------------------------------------------------------------------------------------------------------
# ---------------- Functions for creating pre-processing techniques and combinations to test and applying them ---------------------------------------
#%%

#%% Utility function to obtain all permutations of pre-processing arguments

def _get_argument_combinations(arguments):
    arg_names = sorted(arguments)
    combinations = itertools.product(*(arguments[arg] for arg in arg_names))
    combinations = [dict(zip(arg_names, arg_values)) for arg_values in combinations]
    return combinations

#%% Function to delete unwanted combination of pretreatments
# Delete combination of None pretreatments  
# Delete pipeline with more than nmax pretreatments (without autoscale)
# MSC not allowed with EMSC

def fct_delete_pipelines(pipeline, pretreatment, nmax):
    pmax = len(pretreatment) - nmax

    for i in range(len(pipeline)):
        idir = 0
        pipe = pipeline[i]
        for key in pretreatment.keys():
            if (pipe[key] == None): 
                idir += 1
        if (idir < pmax):
            pipeline[i] = None
        if (idir == len(pretreatment)):
            pipeline[i] = None
        if ('MSC' in pipe) and('EMSC' in pipe):
            if ((pipe['MSC'] != None) and (pipe['EMSC'] != None)):
                pipeline[i] = None
    
    pipeline = list(filter(None, pipeline))

    return pipeline

#%% Function to create different combinations of pretreatments and apply to data

def fct_apply_pipelines(X0, pretreatment, nmax, sg_op):
       
    # Generate combination of varying arguments for each pretreatment 
    # Ex : SG(15,1,1) / SNV + SG(15,2,1) and more
    options = {}
    for key in pretreatment.keys(): 
        options[key] = _get_argument_combinations(pretreatment[key])
        options[key].append(None)
        
        
    # Delete impossible arguments for Savitzky-Golay 
    if ('savitzky_golay') in pretreatment:   
        for i in range(len(options['savitzky_golay'])):
            if (options['savitzky_golay'][i] != None): 
                if (sg_op==0):    # degree of SG polynomial = degree of derivative                
                    if (options['savitzky_golay'][i]['deriv'] != options['savitzky_golay'][i]['order']):
                        options['savitzky_golay'][i] = 0
                else:   # all possible degrees of SG polynomial with degrees of derivative 
                    if (options['savitzky_golay'][i]['deriv'] > options['savitzky_golay'][i]['order']):
                        options['savitzky_golay'][i] = 0
        options['savitzky_golay'] = list(filter((0).__ne__, options['savitzky_golay']))

    # Create pipelines : combination of all different pretreatments to apply 
    pipeline =  _get_argument_combinations(options)

    # Delete unwanted pipelines
    pipeline = fct_delete_pipelines(pipeline, pretreatment, nmax)    
        
    # Apply pretreatments  
    datasets = []
    liste_comb = []

    for i in range(len(pipeline)):
        pipe = pipeline[i]
        two_way = False
    
        X = copy.deepcopy(X0)
        comb = ""
        # Pretreatments applied in ascending alphabetical order         
        for key in sorted(pretreatment.keys(), reverse=False):
            # Create pretreatment formula 
            if (pipe[key] != None):
                if (key == 'savitzky_golay'):
                    formula = "rg."+key+"(X, pipe[key]['window_size'], pipe[key]['order'], pipe[key]['deriv'])"
                else:
                    formula = "rg."+key+"(X)"
             
                # Execute pretreatment
                if (key == 'MSC'):
                    X, _  = eval(formula)
                else:
                    X = eval(formula)
            
                # Create list of pretreatments applied
                if (comb == ""):
                    comb = str(key) + str(pipe[key])
                else:
                    two_way = True
                    comb = comb + " / " + str(key) + str(pipe[key])
        liste_comb.append(comb)
        datasets.append(X)
     
        # Pretreatments applied in descending alphabetical order 
        if (two_way == True):
            X = copy.deepcopy(X0)
            comb = ""
            for key in sorted(pretreatment.keys(), reverse=True):
                # Create pretreatment formula 
                if (pipe[key] != None):
                    if (key == 'savitzky_golay'):
                        formula = "rg."+key+"(X, pipe[key]['window_size'], pipe[key]['order'], pipe[key]['deriv'])"
                    else:
                        formula = "rg."+key+"(X)"
                    
                    # Execute pretreatment
                    if (key == 'MSC'):
                        X, _  = eval(formula)
                    else:
                        X = eval(formula)
                
                    # Create list of pretreatments applied
                    if (comb == ""):
                        comb = str(key) + str(pipe[key])
                    else:
                        comb = comb + " / " + str(key) + str(pipe[key])
                    
            liste_comb.append(comb)
            datasets.append(X)
            
    return liste_comb, datasets

#%%
# ------------------- Second part -------------------------------------------------------------------------------
# ------------------- Function to compare pre-processing techniques and combinations -------------------------------------------------------------------------------
#%%

def compare_preprocessing(X0, y ,nbPC=2, nb_comb=2, auto_x=1, auto_y=1, nb=60, CVnb=20, only_sg=0, svg_order=[1,2], svg_deriv = [1,2], svg_window = [13,15,17], sg_op=0):
    '''
    compare_preprocessing: method based on mbPLS to evaluate pre-processing techniques and their combinations
    [datasets, datasets0, R2_adj, R2_all, RMSECV_all, VIP_all, combination] = compare_preprocessing(X0, y ,nbPC=2, nb_comb=2, auto_x=1, auto_y=1, nb=1, CVnb=20, only_sg=0, svg_order=[1,2], svg_deriv = [1,2], svg_window = [13,15,17], sg_op=0)
    
    INPUT
    X0 [n x k] <numpy.ndarray>
        X0 data to test pre-processing techniques on
        n samples
        k variables
    y [n x m] <numpy.ndarray>
        y data to predict
        n samples
        m variables
        
    OPTIONAL INPUT    
    nbPC <int>
        number of principal components for PLS in the mbPLS decomposition (default value=2)
    nb_comb <int>
        maximum number of pre-processing techniques applied on same data (default value=2)      
    auto_x <int>
        autoscale data after applying pre-processing technique if auto_x=1, if not data centered (default value=1)
    auto_y <int>
        autoscale variables to predict if auto_y=1, if not centered (default value=1)
    nb <int>
        number of random picks for cross validation
    CVnb <int>
        number of samples predicted in each cross validation
    only_sg <int>
        only test Savitzky-Golay if only_sg=1 (default value=0)
    svg_order <list>
        Savitzky-Golay polynomials orders to test
    svg_deriv <list>
        Savitzky-Golay derivatives orders to test
    svg_window <list>
        Savitzky-Golay window sizes to test
    sg_op <int>
        test only Savitzky-Golay pretreatments with the same order of polynomial and derivative if sg_op=0 (default value=0)
        
    OUTPUT
    combination <list>
        Pre-processing techniques tested
    datasets0 <list>
        data X0 after each pre-processing technique  
    datasets <list>
        data X0 after each pre-processing technique and autoscaled or centered   
    R2_all <list>   
        R2 values for each y variable predicted for each pre-processing technique tested (block)
    R2adj_all <list>   
        R2 adjusted values for each y variable predicted for each pre-processing technique tested (block)
    RMSECV_all <list>   
        Root mean square error by cross validation for each y variable predicted for each pre-processing technique tested (block)
    VIP_all <list>   
        PLS variable importance in projection for each y variable predicted for each pre-processing technique tested (block) 
    
    '''
    
    #%% Save dimensions of data
    
    n, k = X0.shape
    
        
    #%% Define different pre-processing techniques to test
    
    if (only_sg==1):  
        pretreatment ={'savitzky_golay':{'window_size':svg_window,'order':svg_order,'deriv':svg_deriv}}
    else:
        pretreatment ={'SNV':{},'MSC':{},'EMSC':{}, 'detrend':{}, 'baseline':{}, \
                        'savitzky_golay':{'window_size':svg_window,'order':svg_order,'deriv':svg_deriv}}
        
    
    #%% Generate differents pretreatments and apply to dataset
    combination, datasets  = fct_apply_pipelines(X0, pretreatment, nb_comb, sg_op)
    
    nb_pt = len((datasets)) # Save number of pretreatments
    
    #%% Add data 
    
    # Matrix without pretreatment 
    datasets.append(X0)    
    
    # False signals
    for i in range(20): 
        faux_signal = np.random.randn(n,k)
        faux_signal = faux_signal/100
        datasets.append(faux_signal)
    
    # Save data before autoscale
    datasets0 = copy.deepcopy(datasets)
    y0 = copy.deepcopy(y)
    
    #%% Autoscale or center data    
             
    for i in range(len(datasets)):
        if (auto_x==0): 
            datasets[i], _ = rg.center(datasets[i]) # Center data 
        else:
            datasets[i], _, _ = rg.autoscale(datasets[i]) # Autoscale data 
    
    if (auto_y==0): 
        y, _ = rg.center(y) # Center data 
    else:
        y, _, _ = rg.autoscale(y) # Autoscale data 
    
    #%% mbPLS 
    
    Tt, T_all, Wt, Wi_all, SSX, SSY, SSXi = rg.mbPLS(nbPC, y,*datasets)
    
    
    #%% Group pretreatments
    
    # According to use of SG
    sg1 = []
    sg2 = []
    sg3 = []
    sg4 = []
    
    scat = []
    
    for i in range(nb_pt):
        if ('savitzky_golay{\'deriv\': 4, \'order\': 4' in combination[i]):
            sg4.append(i)
        elif (('savitzky_golay{\'deriv\': 3, \'order\': 3' in combination[i]) or ('savitzky_golay{\'deriv\': 3, \'order\': 4' in combination[i])):
            sg3.append(i)
        elif (('savitzky_golay{\'deriv\': 2, \'order\': 2' in combination[i]) or ('savitzky_golay{\'deriv\': 2, \'order\': 3' in combination[i]) or \
              ('savitzky_golay{\'deriv\': 2, \'order\': 4' in combination[i])):
            sg2.append(i)
        elif ('savitzky_golay' in combination[i]):
            sg1.append(i)
        else: 
            scat.append(i)
            
    plt.figure()
    plt.scatter(Wt[scat,0], Wt[scat,1],16, marker='o', c='b', label='No SG')
    if 1 in svg_deriv:
        plt.scatter(Wt[sg1,0], Wt[sg1,1],16, marker='o', c='salmon', label='SG1')
    if 2 in svg_deriv:
        plt.scatter(Wt[sg2,0], Wt[sg2,1],16, marker='o', c='orange', label='SG2')
    if 3 in svg_deriv:
        plt.scatter(Wt[sg3,0], Wt[sg3,1],16, marker='o', c='saddlebrown', label='SG3')
    if 4 in svg_deriv:
        plt.scatter(Wt[sg4,0], Wt[sg4,1],16, marker='o', c='g', label='SG4')
    plt.scatter(Wt[nb_pt,0], Wt[nb_pt,1],16, marker='o', c='k', label='Original')
    plt.scatter(Wt[nb_pt+1:,0], Wt[nb_pt+1:,1],16, marker='o', c='lightgrey', label='False signals')
    plt.xlabel('$w_1$')
    plt.ylabel('$w_2$')
    plt.legend()
    
    # According to use of EMSC, MSC or SNV
    group_sc = []
    no_sc = []
    
    for i in range(nb_pt):
        if (('MSC' in combination[i]) or ('SNV' in combination[i]) or ('EMSC' in combination[i])):
            group_sc.append(i)
        else:
            no_sc.append(i)
    
    test1 = []
    for i in list(group_sc):
        test1.append(combination[i])
    
    test2 = []
    for i in list(no_sc):
        test2.append(combination[i])
    
    plt.figure()
    plt.scatter(Wt[:,0], Wt[:,1],16, marker='o', c='lightgrey')
    plt.scatter(Wt[group_sc,0], Wt[group_sc,1],16, marker='o', c='forestgreen', label='Use of EMSC, MSC or SNV')
    plt.scatter(Wt[no_sc,0], Wt[no_sc,1],16, marker='o', c='darkgoldenrod', label='Not')
    plt.scatter(Wt[nb_pt,0], Wt[nb_pt,1],16, marker='o', c='k', label='Original')
    plt.scatter(Wt[nb_pt+1:,0], Wt[nb_pt+1:,1],16, marker='o', c='lightgrey', label='False signals')
    plt.xlabel('$w_1$')
    plt.ylabel('$w_2$')
    plt.legend()
    
    #%% Cross validation for best pretreatments
    
    RMSECV_all = []
    R2_all = []
    R2adj_all = []
    VIP_all = []
    
    for iy in range(len(y[0])):
        yi = y0[:,iy][np.newaxis].T
            
        RMSECV_y = []
        R2_y = []
        VIP_y = []
        
        for i in range(len(datasets)):
            E = []
            R2i = []
            VIPi = []
        
            for CV in range(nb):
                Xi = datasets0[i]
                r = np.random.choice(Xi.shape[0], CVnb, replace=False)
                
                
                Xc = np.delete(Xi,r,axis=0)
                yc = np.delete(yi,r,axis=0)
                
                Xv = Xi[r,:]
                yv = yi[r]
                
                # Autoscale or center data
                if (auto_x==0): 
                    Xc, mx = rg.center(Xc) 
                    Xv = Xv - mx
                else:
                    Xc, mx, stdx = rg.autoscale(Xc) 
                    Xv = (Xv - mx)/stdx
                    
                if (auto_y==0): 
                    yc, my = rg.center(yc) 
                    yv = yv - my
                else:
                    yc, my, stdy = rg.autoscale(yc)
                    yv = (yv - my)/stdy
                
                
                T, U, P, W, Q, B, Yhat, SSX, SSY = rg.PLS(Xc, yc, nbPC)
                Wstar = W@np.linalg.inv(P.T@W)
                beta = Wstar@B@Q.T
                
                Yhat = Xv@beta
                
                e = yv - Yhat
                E.append(e)
                
                R2 = rg.R2(yv, Yhat)
                R2i.append(R2)
                
                VIP = rg.VIP(datasets[i],W,SSY)
                VIP = np.squeeze(VIP)
                VIPi.append(VIP)
                
            E = np.array(E)
            RMSECV = np.sqrt(np.mean(E**2))    
            RMSECV_y.append(RMSECV)
                
            R2i = np.array(R2i)
            R2i = np.mean(R2i)    
            R2_y.append(R2i)
            
            VIPi = np.array(VIPi)
            VIPi = np.mean(VIPi, axis=0)
            VIP_y.append(VIPi)
        
        RMSECV_y = np.array(RMSECV_y)
        
        R2_y = np.array(R2_y)
        R2adj_y = 1 -((1-R2_y)*(n-1))/(n-nbPC-1)
        
        VIP_y = np.array(VIP_y)
        
        # Superloading plot with color code: RMSECV
        fig, ax = plt.subplots()
        plt.plot(Wt[:,0],Wt[:,1],'.k')
        cs = plt.scatter(Wt[:nb_pt+1,0],Wt[:nb_pt+1,1], c=RMSECV_y[:nb_pt+1], s=100)
        cbar = fig.colorbar(cs, format='%.0e')
        cbar.set_label('RMSECV', rotation=270, labelpad=10)
        for  i in range(nb_pt+1):
            plt.text(Wt[i,0], Wt[i,1],i,fontsize=12).set_color('black')
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.xlabel('$w_{1}$',fontsize=12)
        plt.ylabel('$w_{2}$',fontsize=12)
        plt.title('y[:,'+str(iy)+']',fontsize=12)
        plt.tight_layout()
        plt.show()
        
        # Superloading plot with color code: R2
        fig, ax = plt.subplots()
        plt.plot(Wt[:,0],Wt[:,1],'.k')
        cs = plt.scatter(Wt[:nb_pt+1,0],Wt[:nb_pt+1,1], c=R2adj_y[:nb_pt+1], s=100)
        cbar = fig.colorbar(cs)
        cbar.set_label('Adjusted R$^2$', rotation=270, labelpad=10)
        for  i in range(nb_pt+1):
            plt.text(Wt[i,0], Wt[i,1],i,fontsize=12).set_color('black')
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.xlabel('$w_{1}$',fontsize=12)
        plt.ylabel('$w_{2}$',fontsize=12)
        plt.title('y[:,'+str(iy)+']',fontsize=12)
        plt.tight_layout()
        plt.show()
        
        R2_all.append(R2_y)
        R2adj_all.append(R2adj_y)
        RMSECV_all.append(RMSECV_y)
        VIP_all.append(VIP_y)
        
        #%% Effective rank
        
        Ef_all = []   
        for i in range(len(datasets)):
            # ---------- Effective rank -----------------
            A = datasets[i].T@datasets[i]
            [P,D,PT] = np.linalg.svd(A)  
            D = np.diag(D)
            # Lambda : eigenvalues 
            lada = np.diag(D) / np.sum(np.diag(D))
            # Shannon entropy
            Shannon = -np.sum(lada*np.log(lada)) # natural logarithm (log base e) 
            Effective_rank = np.exp(Shannon)
            Ef_all.append(Effective_rank)
            
        # Loading plot with color code: effective rank
        fig, ax = plt.subplots(figsize=(5,4))
        plt.plot(Wt[:,0],Wt[:,1],'.k')
        cs = plt.scatter(Wt[:nb_pt+1,0],Wt[:nb_pt+1,1], c=Ef_all[:nb_pt+1], s=100)
        cbar = fig.colorbar(cs)
        cbar.set_label('Effective rank', rotation=270, labelpad=10)
        for  i in range(nb_pt+1):
            plt.text(Wt[i,0], Wt[i,1],i,fontsize=12).set_color('black')
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.xlabel('$w_{1}$',fontsize=12)
        plt.ylabel('$w_{2}$',fontsize=12)
        plt.title(' y[:,'+str(iy)+']',fontsize=12)
        plt.tight_layout()
        plt.show()

    return combination, datasets, datasets0, R2_all, R2adj_all, RMSECV_all, VIP_all, Ef_all, Wt


