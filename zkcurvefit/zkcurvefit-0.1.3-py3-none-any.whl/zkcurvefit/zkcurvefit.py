def curvefit(ftoread,ftowrite,ts=1000,density_coeff=5,plot="off",sigma=1,extend=10,isComplex=True):
    """
    takes parameters file to read, file to write to, max timestep,density 
    coeff and plot ="on" will display plot for given values. 
    assumes first column is timesteps starting from 1 and first row is titles(can be empty)
    dilutes to number of timesteps by density_coeff.
    curvefits with respect to timesteps and normalize max value to 1.
    applied to all columns.
    writes files "real" ,"curvefit", "toff (off-rates),residence times"
    """
    
    from scipy.optimize import curve_fit as cvf
    import numpy as np
    import csv
    import matplotlib.pyplot as plt
    
    csvName = ftoread
    
    csv_file = open(csvName,"r")
    csv_input = csv.reader(csv_file)
    dens_coef = density_coeff
    
    #create an array from csv file until the given timestep
    arr = []
    cof = 0
    ts = ts + 50
    for row in csv_input:
        cof +=1
        if cof<=ts:
            arr.append(row)
    
    
    arr = np.array(arr)
    
    nrow,ncol = arr.shape
    
    exp = int(nrow/dens_coef)
    init_btf = float(arr[1,1])
    
    time = np.zeros(exp)
    value = np.zeros(exp)

    
    tm = np.linspace(0,ts-dens_coef,exp)
    so_many_timePoints = np.linspace(0,ts*extend,num=500000)
    
    e = np.e
    tau = init_btf/e
    
    for i in range(exp):
        time[i] = arr[i*dens_coef+1,0]
    #tm will be used as first columnt reference time list to fit to.
    w = tm.reshape(exp,1)
    
    resTime = np.ones(ncol)
    resTime_simple = np.ones(ncol)
    
    #Every column is curvefit according to time step values.
    
    for tt,j in enumerate(range(ncol)):
    
        for i in range(1,exp):
            value[i-1] = arr[i*dens_coef,j]
        if isComplex:
            #curvefit complex function   
            def func(x, a, b,c ,d):
                return a - b*np.log(x+d)+c*x**0.25
            popt,pcov = cvf(func,time,value, p0 = [0,-30,30,+30] ,maxfev = 1000000)
  
        def func1(x, a, b,c ,d):
            return a - b*np.log(x)+c+d
            
        #parameter optimaztion with initial parameters
        
        popt1,pcov1 = cvf(func1,time,value, p0 = [0,-30,30,+30] ,maxfev = 1000000)
        
        
        #residence times are initiated
        resTime[tt]=-2/sigma
        #values are fitted to given time points
        if isComplex:
            value_fit = func(tm,*popt)
            big_val = func(so_many_timePoints,*popt)
            for ii,remTF in enumerate(big_val):
                if abs(remTF-tau)<0.1:
                    resTime[tt] = so_many_timePoints[ii]
                    break
        else:
            value_fit = func1(tm,*popt1)
        
        #for loop to go through values of the multiple timepoints

        """
        Residence time with the simplistic equation 
        """
        resTime_simple[tt] = -2/sigma
        a,b,c,d = popt1
        resTime_simple[tt] = np.e**((a+c+d-(i/e))/b)
                
        
        value_fit[0] = init_btf
        value_fit = value_fit/init_btf
        
        #fitted values is turned into column
        value_fit =value_fit.reshape(exp,1)
        
        #fixing values if they are out of boundaries
        for index,fraction in enumerate(value_fit):
            
            if fraction > 1:
                value_fit[index]=1
            elif fraction < 0:
                value_fit[index]=0
    
    
        if j == 0:
            pass
        else:
            #all the values will be appended
            w = np.append(w,value_fit,axis=1)
    
        if plot == "on":
            plt.plot(time,value/init_btf,"b.", label= "real")
            plt.plot(tm,value_fit, "r-", label = "fit")
            plt.show()
        else:
            pass
    
    
    arr3 = []
    zero = -1
    delim = int(ts/(dens_coef*10)-1)*dens_coef
    for k in arr:
        zero +=1
        if zero == 1:
            k[0]=0
            arr3.append(k)
        elif zero%delim == 0:
            arr3.append(k)
    csv_file.close()
    curvefit_arr = []
    
    i =0
    while(w[i][0]<=ts-50 and i<len(w)):
        curvefit_arr.append(w[i])
        i+=1
    
    resTime = resTime*sigma+1
    
    if isComplex:
        #toff file
        toff = 1/resTime
        toff = toff.reshape([1,ncol])
        ff = "off" + ftowrite
        np.savetxt(ff,toff,fmt= "%s",delimiter=",")
        print("done " + ff)
        
        #residence time file
        resTime = resTime.reshape([1,ncol])
        mm = "residence" + ftowrite
        np.savetxt(mm, resTime,fmt= "%s",delimiter=",")
        print("done " + mm)
        
    #curvefit values file
    curvefit_arr = np.array(curvefit_arr)
    kurve_fit = "cf" + ftowrite
    np.savetxt(kurve_fit,curvefit_arr,fmt= "%s",delimiter=",")
    print("done " + kurve_fit)
    
    arr3 = np.array(arr3)
    nr, nc = arr3.shape
    real_arr = np.zeros([nr-1,nc])
    for h in range(nc):
        for p in range(1,nr):
            real_arr[p-1][h] = float(arr3[p][h])/init_btf
            real_arr[p-1][0] = float(arr3[p][0])
    
    #real values file
    pp = "real"+ftowrite
    np.savetxt(pp,real_arr,fmt= "%s",delimiter=",")
    print("done " +  pp)
    
    #restime simple
    resTime_simple = resTime_simple*sigma*1
    resTime_simple = resTime_simple.reshape([1,ncol])
    rr = "residence_simple"+ftowrite
    np.savetxt(rr,resTime_simple,fmt= "%s",delimiter=",")
    print("done " +  rr)
    
    #toff_simple
    toff_simple = 1/resTime_simple
    toff_simple = toff_simple.reshape([1,ncol])
    ii = "off_simple" + ftowrite
    np.savetxt(ii,toff_simple,fmt= "%s",delimiter=",")
    print("done " + ii)
    
    return

if __name__ == '__main__':
    curvefit("9-5kT.csv","95.csv",plot="on",extend=10,sigma=1000,isComplex = True)
  