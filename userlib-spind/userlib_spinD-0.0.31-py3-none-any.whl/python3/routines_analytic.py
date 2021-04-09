import numpy as np


#======================================
# Describtion: the function returns the Energie of a Spinspiral
#              with respect to the input object @para and the absolute
#              of a spinspiral vector @q in the GM-direction for @q<0
#              and in the GK-direction for @q>=0.
def energy_SS(q, para, left_rotating=False):
    # zero padding of parameter arrays, so that the total length fits to
    # calculations below
    pad = 11 - len(para.exc)
    if pad > 0:
        exc_zeros = np.asarray([0.0 for n in range(pad)])
        exc = np.concatenate((para.exc, exc_zeros), axis=None)
    pad = 11 - len(para.dmi)
    if pad > 0:
        dmi_zeros = np.asarray([0.0 for n in range(pad)])
        dmi = np.concatenate((para.dmi, dmi_zeros), axis=None)

    if left_rotating :
        dmi = -dmi

    # ==========================================================================
    # GK-direction
    # ==========================================================================
    if q >= 0.0 :
        # add up exchange interactions
        Exc = -exc[0]*2.0*(np.cos(2.0*np.pi*q) + 2.0*np.cos(np.pi*q) -3.0)
        Exc += -exc[1]*4.0*(np.cos(3.0*np.pi*q) -1.0)
        Exc += -exc[2]*2.0*(np.cos(4.0*np.pi*q) + 2.0*np.cos(2.0*np.pi*q) -3)
        Exc += -exc[3]*4.0*(np.cos(np.pi*q) + np.cos(4.0*np.pi*q) + np.cos(5.0*np.pi*q) -3)
        Exc += -exc[4]*2.0*(np.cos(6.0*np.pi*q) + 2.0*np.cos(3.0*np.pi*q) -3.0)
        Exc += -exc[5]*4.0*(np.cos(6.0*np.pi*q) -1.0)
        Exc += -exc[6]*4.0*(np.cos(2.0*np.pi*q) + np.cos(5.0*np.pi*q) + np.cos(7.0*np.pi*q) -3)
        Exc += -exc[7]*2.0*(np.cos(8.0*np.pi*q) + 2.0*np.cos(4.0*np.pi*q) -3.0)
        Exc += -exc[8]*4.0*(np.cos(np.pi*q) + np.cos(7.0*np.pi*q) + np.cos(8.0*np.pi*q) -3)
        Exc += -exc[9]*4.0*(np.cos(3.0*np.pi*q) + np.cos(6.0*np.pi*q) + np.cos(9.0*np.pi*q) -3)
        Exc += -exc[10]*2.0*(np.cos(10.0*np.pi*q) + 2.0*np.cos(5.0*np.pi*q) -3.0)
        # add dmi interactions
        Dmi = -dmi[0]*2.0*(np.sin(2.0*np.pi*q) + np.sin(np.pi*q))
        Dmi += -dmi[1]*6.0/np.sqrt(3.0)*np.sin(3.0*np.pi*q)
        Dmi += -dmi[2]*2.0*(np.sin(4.0*np.pi*q) + np.sin(2.0*np.pi*q))
        Dmi += -dmi[3]*2.0/np.sqrt(7.0)*(5.0*np.sin(5.0*np.pi*q) + 4.0*np.sin(4.0*np.pi*q) + np.sin(np.pi*q))
        Dmi += -dmi[4]*2.0*(np.sin(6.0*np.pi*q) + np.sin(3.0*np.pi*q))
        Dmi += -dmi[5]*2.0*np.sqrt(3.0)*np.sin(6.0*np.pi*q)
        #Dmi += -dmi[6]*2.0/np.sqrt(13.0)*(7.0*np.sin(7.0*np.pi*q) + 5.0*np.sin(5.0*np.pi*q))
        Dmi += -dmi[6]*2.0/np.sqrt(13.0)*(7.0*np.sin(7.0*np.pi*q) + 5.0*np.sin(5.0*np.pi*q) + 2.0*np.sin(2.0*np.pi*q))
        # add anisotropy
        if q > -np.finfo(float).eps and q < np.finfo(float).eps :
            Ani = para.ani[0]
        else :
            Ani = para.ani[0]/2.0
        # higher order interactions
        Biq = -para.biq[0]*(3.0 + 2.0*np.cos(2.0*np.pi*q) + np.cos(4.0*np.pi*q) - 6.0)
        Sp4 = 0.0
        Sp3 = -para.sp3[0]*2.0*( 4.0*np.cos(np.pi*q)*np.cos(2.0*np.pi*q) + 2.0*np.cos(np.pi*q)**2.0 -12.0)

    # ==========================================================================
    # GM-direction
    # ==========================================================================
    else :
        # add up exchange interactions
        Exc = -exc[0]*4.0*(np.cos(np.sqrt(3.0)*np.pi*q)-1.0)
        Exc += -exc[1]*2.0*(np.cos(2.0*np.sqrt(3.0)*np.pi*q) + 2.0*np.cos(np.sqrt(3.0)*np.pi*q) -3.0)
        Exc += -exc[2]*4.0*(np.cos(2.0*np.sqrt(3.0)*np.pi*q) -1.0)
        Exc += -exc[3]*4.0*(np.cos(3.0*np.sqrt(3.0)*np.pi*q) + np.cos(2.0*np.sqrt(3.0)*np.pi*q) + np.cos(np.sqrt(3.0)*np.pi*q) -3)
        Exc += -exc[4]*4.0*(np.cos(3.0*np.sqrt(3.0)*np.pi*q) -1.0)
        Exc += -exc[5]*2.0*(np.cos(4.0*np.sqrt(3.0)*np.pi*q) + 2.0*np.cos(2.0*np.sqrt(3.0)*np.pi*q) -3.0)
        Exc += -exc[6]*4.0*(np.cos(4.0*np.sqrt(3.0)*np.pi*q) + np.cos(3.0*np.sqrt(3.0)*np.pi*q) + np.cos(np.sqrt(3.0)*np.pi*q) -3)
        Exc += -exc[7]*4.0*(np.cos(4.0*np.sqrt(3.0)*np.pi*q)-1.0)
        Exc += -exc[8]*4.0*(np.cos(5.0*np.sqrt(3.0)*np.pi*q) + np.cos(3.0*np.sqrt(3.0)*np.pi*q) + np.cos(2.0*np.sqrt(3.0)*np.pi*q) -3)
        Exc += -exc[9]*4.0*(np.cos(5.0*np.sqrt(3.0)*np.pi*q) + np.cos(4.0*np.sqrt(3.0)*np.pi*q) + np.cos(np.sqrt(3.0)*np.pi*q) -3)
        Exc += -exc[10]*4.0*(np.cos(5.0*np.sqrt(3.0)*np.pi*q)-1.0)
        # add dmi interaction
        Dmi = dmi[0]*2.0*np.sqrt(3.0)*np.sin(np.sqrt(3.0)*np.pi*q)
        Dmi += dmi[1]*2.0*(np.sin(2.0*np.sqrt(3.0)*np.pi*q) + np.sin(np.sqrt(3.0)*np.pi*q))
        Dmi += dmi[2]*2.0*np.sqrt(3.0)*np.sin(2.0*np.sqrt(3.0)*np.pi*q)
        #Dmi += dmi[3]*2.0/np.sqrt(3.0/7.0)*(2.0*np.sin(2.0*np.sqrt(3.0)*np.pi*q) + 3.0*np.sin(3.0*np.sqrt(3.0)*np.pi*q) + np.sin(np.sqrt(3.0)*np.pi*q))
        Dmi += dmi[3]*2.0*np.sqrt(3.0/7.0)*(3.0*np.sin(3.0*np.sqrt(3.0)*np.pi*q) + 2.0*np.sin(2.0*np.sqrt(3.0)*np.pi*q) + np.sin(np.sqrt(3.0)*np.pi*q))
        Dmi += dmi[4]*2.0*np.sqrt(3.0)*np.sin(3.0*np.sqrt(3.0)*np.pi*q)
        Dmi += dmi[5]*2.0*(np.sin(4.0*np.sqrt(3.0)*np.pi*q) + np.sin(2.0*np.sqrt(3.0)*np.pi*q))
        #Dmi += dmi[6]*2.0*np.sqrt(3.0/13.0)*(4.0*np.sin(4.0*np.sqrt(3.0)*np.pi*q) + 3.0*np.sin(3.0*np.sqrt(3.0)*np.pi*q))
        Dmi += dmi[6]*2.0*np.sqrt(3.0/13.0)*(4.0*np.sin(4.0*np.sqrt(3.0)*np.pi*q) + 3.0*np.sin(3.0*np.sqrt(3.0)*np.pi*q) + np.sin(np.sqrt(3.0)*np.pi*q))
        # add anisotropy
        Ani = para.ani[0]/2.0
        # higher order interactions
        Biq = -para.biq[0]*(3.0 + 2.0*np.cos(2.0*np.pi*np.sqrt(3.0)*q) -5.0)
        Sp4 = 0.0
        Sp3 = -para.sp3[0]*2.0*( 4.0*np.cos(np.pi*np.sqrt(3.0)*q) + 2.0*np.cos(np.pi*np.sqrt(3.0)*q)**2.0 -12.0)

    Zee, Dip = 0.0, 0.0
    Abs = Exc +Dmi +Ani +Biq +Sp4 +Sp3
    return [Abs, Exc, Zee, Ani, Dmi, Sp3, Sp4, Biq, Dip]
