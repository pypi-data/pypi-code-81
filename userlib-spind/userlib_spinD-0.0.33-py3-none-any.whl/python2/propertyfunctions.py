import numpy as np

#============================================
# function for the topological charge of a lattice, see B.Berg and M.Luescher
# works just on a lattice constructed in the way
# the class 'Lattices' does. For other constructions
# S1,S2,S3,S4 have to be assigned disfferently.
# But the calculation of the spherical area is nice in every way.
# Input : mag = [my, mx,mz]
# Output : float Q
#============================================
def topocharge(mag):
    Q = 0
    size = int(np.sqrt(len(mag[0])))
    for n in range(size-1):
        for m in range(size-1):
            index1 = n*size + m
            index2 = (n+1)*(size-1) + (m+1) +n
            index3 = (n+1)*(size-1) + (m+2) +n
            index4 = n*size + (m+1)
            S1 = np.asarray([mag[0][index1], mag[1][index1], mag[2][index1]])
            S2 = np.asarray([mag[0][index2], mag[1][index2], mag[2][index2]])
            S3 = np.asarray([mag[0][index3], mag[1][index3], mag[2][index3]])
            S4 = np.asarray([mag[0][index4], mag[1][index4], mag[2][index4]])
            area1 = get_spherical_area(S1, S2, S3)
            area2 = get_spherical_area(S1, S3, S4)
            Q += area1 + area2
    return Q/4.0/np.pi
#============================================
# function returns the spherical area created by three spins
# the sign of the area is the sign of the spat product S1*(S2xS3)
# inspired by implementation of B. Dupe
#============================================
def get_spherical_area(S1, S2, S3):
    con = 1 + np.dot(S1,S2) + np.dot(S2,S3) + np.dot(S3,S1)
    # FM CASE
    if con >= 4.-10e-8 :
        area = 0.
    else :
        mat = [S1, S2, S3]
        det_mat = np.linalg.det(mat)
        # EXCEPTIONAL CASE
        if abs(con) <= 10e-8 and abs(det_mat) <=10e-8:
            area = 0.
        # NON-EXCEPTIONAL NON-COLINEAR CASE
        else :
            area = 2.0*np.arctan2(det_mat, con)
    return area


#============================================
# funktion for calculation of the skyrmion radius.
# method adopted from S.v. Malottki
# Input: SpinLattice object
#============================================
def skyrmionradius(splat):
    from scipy.optimize import curve_fit, fmin
    #============================================
    # 2d fit function for the skyrmion profile
    #============================================
    def sk_2dprofile(R, r0x, r0y, c, w):
        r = np.sqrt((R[0]-r0x)**2 + (R[1]-r0y)**2)
        mzs = np.cos(theta(r,c,w))
        return mzs
    #============================================
    # analytic function for the azimuthal angle @theta of a skyrmion
    # and its derivation @dtheta_dr
    # @r is the distance from the centrum
    # @c, @w the fit parameters
    #============================================
    def theta(r,c,w):
        comp1 = np.arcsin(np.tanh((-abs(r) -c)*2.0/w))
        comp2 = np.arcsin(np.tanh((-abs(r) +c)*2.0/w))
        return np.pi +comp1 +comp2
    def dtheta_dr(r,c,w):
        comp1 = 2.0*np.sqrt(-np.tanh(2.0*(-c + abs(r))/w)**2 + 1)/w
        comp2 = 2.0*np.sqrt(-np.tanh(2.0*( c + abs(r))/w)**2 + 1)/w
        return -comp1 -comp2
    #============================================
    # calculates the radius determined by @c, @w using
    # lilley criteria
    #============================================
    def sk_radius(c,w):
        x0 = fmin(lambda x: dtheta_dr(x,c,w), 0,disp=False,xtol=1.0E-10)[0]
        rad = x0 - theta(x0,c,w)/dtheta_dr(x0,c,w)
        return rad
    #================================================================
    # main
    #================================================================
    # 1) Find the minimum of magnetisation, as it is nearly the sk center
    index = np.where( splat.mz == min(splat.mz))[0][0]
    # 2) make a 2d fit to mz using sk_2dprofile function
    start_para = [splat.X[index], splat.Y[index], 2.5, 3.0]
    popt, pcov = curve_fit(sk_2dprofile, [splat.X, splat.Y], splat.mz, start_para, maxfev=2000)
    popt, pcov = curve_fit(sk_2dprofile, [splat.X, splat.Y], splat.mz, popt)
    # the estimated parameters c,w determine the Radius
    radius = sk_radius(popt[2], popt[3])
    return radius, popt, np.sqrt(np.diag(pcov))

#============================================
# function to find the width of a domainwall using curve_fit
#============================================
def dwwidth(splat):
    from scipy.optimize import curve_fit, fmin
    X, Y, mx, my, mz = np.asarray(splat.X), np.asarray(splat.Y), np.asarray(splat.mx), np.asarray(splat.my), np.asarray(splat.mz)
    #============================================
    # 2d fit function for the domainwall profile and a straight line
    #============================================
    def dw_2dprofile(R, r0, phi, w):
        theta = 2.0*np.arctan(np.exp( (R[0]*np.cos(phi) + R[1]*np.sin(phi) -r0)/w))
        return np.cos(theta)
    def dw_2dprofile_reduzed(R, w):
        theta = 2.0*np.arctan(np.exp( (R[0]*np.cos(init_phi) + R[1]*np.sin(init_phi)-init_r0)/w))
        return np.cos(theta)
    def gerade(x, y0, m):
        return y0 + x*m
    #============================================
    # the functions returns the initial values for @phi, the angle between @direction
    # and the x-axis, and also @r0, the distance to the wall on this line
    #============================================
    def get_init_values():
        # find points inside the DW and fit them with a straight line
        index = np.where( abs(mz) < 0.1 )
        popt, pcov = curve_fit(gerade, X[index[0]], Y[index[0]])
        # calculate the initial guess for the angle between @direction and x-axis
        # by using the slope of the fitted straight line
        phi = np.pi/2.0 - np.arctan(abs(popt[1]))
        # to find @r0 set arg=(r-r0)n=0 => r0=rx*cos(phi) + ry*sin(phi)
        # which corresponds to a position on the domainwall
        r0 = splat.X[index[0][0]]*np.cos(phi) + splat.Y[index[0][0]]*np.sin(phi)
        return r0, phi
    #============================================
    # main
    #============================================
    # determine situation: down->up, up->down
    dir = np.sign(splat.mz[0])
    # get initial values for @r0 and @phi and fit DW with them to get @init_w
    init_r0, init_phi = get_init_values()
    popt, pcov = curve_fit(dw_2dprofile_reduzed, [splat.X, splat.Y], np.asarray(splat.mz)*dir, [1.0])
    init_w = popt[0]
    start_para = [init_r0, init_phi, init_w]
    # fit the DW profile to the data using reasonable start parameters
    popt, pcov = curve_fit(dw_2dprofile, [splat.X, splat.Y], np.asarray(splat.mz)*dir, start_para)
    return popt[0], popt[1], popt[2]








#==============================================
# INPUT: initial and final images @init and @final. optionaly the number of images
#        to generate
# OUTPUT: the methods writes the sequence of images to the folder @'geodasic_path'
# DESCRIPTION: This method calculates @steps images on the geodasic
#              path between the initial image @init and the final image
#              @final.
# CONVENTION: the initial image is @image_0 and the final @image_(steps)
#==============================================
def geodasic_path(init, final, steps=10, make_pov=False):
    import os
    from magnetisations import rotate_to_axis, rotation_matrix, rotate_spins, SpinLattice
    from visualizations import write_STM, spinpov
    from shell_commands import make_directory, change_directory

    assert init.size == final.size
    if not os.path.isdir('geodasic_path'):
        make_directory('geodasic_path')

    with change_directory('geodasic_path'):
        # write the inital and final STM files
        write_STM(init, name='image_0.dat')
        write_STM(final, name='image_'+str(steps)+'.dat')
        if make_pov :
            spinpov(init, 'image_0')
            spinpov(final, 'image_'+str(steps))

        # for each image on the geodasic path, calculate the spin configuration
        for n in range(1,steps):
            sl = SpinLattice(size=init.size, key='hex', magmom=init.magmom[0])
            for m in range(len(init.mx)):
                axis, ang = rotate_to_axis([final.mx[m], final.my[m], final.mz[m]], [init.mx[m], init.my[m], init.mz[m]])
                mat = rotation_matrix(axis, ang*float(n)/float(steps))
                tempx, tempy, tempz = rotate_spins([init.mx[m]], [init.my[m]], [init.mz[m]], mat)
                sl.mx[m], sl.my[m], sl.mz[m] = tempx[0], tempy[0], tempz[0]
            tag = 'image_'+str(n)
            write_STM(sl, name=tag+'.dat')
            if make_pov :
                spinpov(sl, tag)
