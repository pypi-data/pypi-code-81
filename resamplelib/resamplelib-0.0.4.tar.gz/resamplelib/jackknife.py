import numpy as np
from numba import jit

#@jit(nopython=True)
def jack_knife_1d(x,function):
    x_sum=np.full(len(x),np.sum(x))
    #leave-one-out averages
    jk_aver_x=np.subtract(x_sum,x)/np.float64(len(x)-1)
    #computing the function for each average
    obs_func=function(x)
    jk_func=function(jk_aver_x)
    #average of all samples
    obs_func_aver=np.sum(obs_func)/np.float64(len(obs_func))
    jk_func_aver=np.sum(jk_func)/np.float64(len(jk_func))
    #error for the observable
    err=np.sqrt((np.float64(len(x)-1))*np.sum((jk_func-jk_func_aver)**2.)/np.float64(len(jk_func)))
    #bias
    bias=np.float64(len(obs_func)-1)*(jk_func_aver-obs_func_aver)
    #unbiased obserable
    observable_unbiased=obs_func_aver-bias
    return jk_func,err,observable_unbiased,bias

#@jit(nopython=True)
def jack_knife_2d(x,y,function):
  try:
    x=np.array(x)
    y=np.array(y)
  except:
    print('From 2d jackknife: can not convert x and y to numpy array')
    quit()
  # Exit program if x and y do not have same lengths
  if np.size(x)!=np.size(y):
    print('From 2d jackknife: x and y must have same size')
    quit()
  x_sum=np.full(len(x),np.sum(x))
  y_sum=np.full(len(y),np.sum(y))
  #leave-one-out averages
  jk_aver_x=np.subtract(x_sum,x)/np.float64(len(x)-1)
  jk_aver_y=np.subtract(y_sum,y)/np.float64(len(x)-1)
  #leave-one-out averages
  #computing the function for each average
  obs_func=function(x,y)
  jk_func=function(jk_aver_x,jk_aver_y)
  #average of all samples
  obs_func_aver=np.sum(obs_func)/np.float64(len(obs_func))
  jk_func_aver=np.sum(jk_func)/np.float64(len(jk_func))
  #error for the observable
  err=np.sqrt((np.float64(len(x)-1))*np.sum((jk_func-jk_func_aver)**2.)/np.float64(len(jk_func)))
  #bias
  bias=np.float64(len(obs_func)-1)*(jk_func_aver-obs_func_aver)
  #unbiased obserable
  observable_unbiased=obs_func_aver-bias
  return jk_func,err,observable_unbiased,bias