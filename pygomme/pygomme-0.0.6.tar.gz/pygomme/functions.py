import pygomme as pg
import numpy as np  
import matplotlib.pyplot as plt

def _gaussian(x, mu, sig , n):
    f = 1/sig/np.sqrt(2*np.pi)
    f *= np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))
    return f

def _histogram_report(ax, q, n,
                      gaussian=False,
                      experimental=False,
                      *args, **kwargs):
    if experimental:
        ne,me,_ = ax.hist(q.experimental_data, bins='rice',color=q.color,*args,**kwargs)
    else:
        ne,me,_ = ax.hist(q.data(n), bins='rice',color=q.color,*args,**kwargs)
    if q.label != "":
        ax.set_xlabel(r'${la}$'.format(la=q.label))
    #if q.title is not None :
    ax.set_title(q.title)
    left, right = ax.get_xlim()
    down,up = ax.get_ylim()
    avg = q.average(n)
    std = q.deviation(n)
    ax.axvline(x=avg, color="black", linestyle="--")
    ax.axvline(x=avg+std, color="blue", linestyle="--")
    ax.axvline(x=avg-std, color="blue", linestyle="--")
    props = dict(boxstyle='square', facecolor='wheat', alpha=0.9)
    ax.text(0.05, 0.95, q.pretty_print(), 
            transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)
    props = dict(boxstyle='square', facecolor='palegreen', alpha=0.9)
    if experimental:
        n_props = len(q.experimental_data)
    else:
        n_props = n
    ax.text(0.85, 0.95, "n = {:n}".format(n_props), 
            transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)
    if gaussian :
            total = 0
            for i in range(len(ne)) :
                total += ne[i]*(me[i+1]-me[i])
            left, right = plt.xlim()
            x = np.linspace(left,right,200)
            plt.plot(x,total*_gaussian(x,avg,std,n),color="black")
            ma = total/std/np.sqrt(2*np.pi)
            if ma > up :
                up = ma
    ax.set_xlim([left,right])
    ax.set_ylim([down,up*1.1])
    return

def _histogram_compare(ax, q1, q2, n,
                      *args, **kwargs):
    la1 = "${}$ = {}".format(q1.label,q1.pretty_print()) 
    la2 = "${}$ = {}".format(q2.label,q2.pretty_print()) 
    if q1.deviation(n) != 0:
        ax.hist(q1.data(n), bins='rice',color="blue", histtype='step',
            label=la1, *args, **kwargs)
    else:
        ax.axvline(x=q1.average(), color="blue", linestyle="-",label=la1)
    if q2.deviation(n) != 0:
        ax.hist(q2.data(n), bins='rice',color="red", histtype='step',
            label=la2, *args, **kwargs)
    else:
        ax.axvline(x=q2.average(), color="red", linestyle="-",label=la2)
    ax.set_xlabel(r'${la} - {lb}$ '.format(la=q1.label,lb=q2.label))
    ax.set_title(q1.title+" -- "+q2.title)
    left, right = ax.get_xlim()
    down,up = ax.get_ylim()
    ax.set_xlim([left,right])
    ax.set_ylim([down,up*1.1])
    ax.legend(loc='upper left')
    z = "E = {:.2f}".format(q1-q2)
    props = dict(boxstyle='square', facecolor='wheat', alpha=0.9)
    ax.text(0.85, 0.9, z.replace(".",","),
            transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)
    props = dict(boxstyle='square', facecolor='palegreen', alpha=0.9)
    ax.text(0.85, 0.97, "n = {:n}".format(n), 
            transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)         
    
    return

