import numpy as np
import os

#============================================
# function to show all created plots
#============================================
def display_plots():
    import matplotlib.pyplot as plt
    plt.show()
#============================================
# write spin configuration
# default name is 'SpinSTMi.dat'
#============================================
def write_STM(sp, name='SpinSTMi.dat'):
    with open(name, 'w') as file :
        for n in range(len(sp.X)):
            file.write('%.8f' %sp.X[n] + '    '
                    + '%.8f' %sp.Y[n] +  '    '
                    + '%.8f' %sp.Z[n] +  '    '
                    + '%.8f' %sp.mx[n] + '    '
                    + '%.8f' %sp.my[n] + '    '
                    + '%.8f' %sp.mz[n] + '    '
                    + '%.8f' %sp.magmom[n] + '\n')


#=============================================
# function to visualize the created lattice with matplotlib
#=============================================
def show_lattice(spinlattice, details=None, filename='spinorientation.png', zoom=None):
    import matplotlib.pyplot as plt
    from mpl_toolkits.axes_grid1.inset_locator import (inset_axes, InsetPosition, mark_inset)
    #================================================================
    # function adds the parameters that define the DW to the plot
    #================================================================
    def DWdetails(ax):
        direction = np.absolute(spinlattice.direction)
        r0 = spinlattice.r0
        R0 = r0*direction
        size = spinlattice.size
        width = spinlattice.dw_width
        ax.arrow(0, 0, direction[0]*size, direction[1]*size, head_width=1, head_length=1, color='k', ls='-', width=0.00002)
        ax.arrow(R0[0], R0[1], -direction[1]*size/2.0, direction[0]*size/2.0, head_width=0, head_length=0, color='k', ls='-', width=0.00002)
        ax.arrow(R0[0], R0[1], direction[1]*size/2.0, -direction[0]*size/2.0, head_width=0, head_length=0, color='k', ls='-', width=0.00002)
        ax.plot(R0[0], R0[1] , marker='h', markersize=10, c='k', ls='')
        def dw_1dprofile(R, r0, w):
            theta = 2.0*np.arctan(np.exp((R -r0)/w))
            return np.cos(theta)
        axx = plt.axes([0,0,1,1])
        ip = InsetPosition(ax, [0.75,0.75,0.25,0.25])
        axx.set_axes_locator(ip)
        x = np.linspace(0, size, 100)
        axx.plot(x, dw_1dprofile(x, r0, width), ls='-', color='b')
        axx.set_xlabel(r'r|$_{||n}$ /a', fontsize=10)
        axx.set_ylabel(r'mz', fontsize=10)
    #================================================================
    # function adds a circle according to skyrmion radius to the plot
    #================================================================
    def Skdetails(ax):
        popt = spinlattice.sk_popt
        rad = spinlattice.sk_radius
        size = spinlattice.size
        circle = plt.Circle((popt[0], popt[1]), rad, color='k', fill=False)
        ax.add_artist(circle)
        def theta_1d(r,r0,c,w):
            comp1 = np.arcsin(np.tanh((-abs(r-r0) -c)*2.0/w))
            comp2 = np.arcsin(np.tanh((-abs(r-r0) +c)*2.0/w))
            return np.pi +comp1 +comp2
        #axx = plt.axes([0,0,1,1])
        #ip = InsetPosition(ax, [0.75,0.75,0.25,0.25])
        #axx.set_axes_locator(ip)
        #x = np.linspace(0, size, 100)
        #axx.plot(x, theta_1d(x, popt[0], popt[2], popt[3]), ls='-', color='b')
        #axx.set_xlabel(r'x /a', fontsize=10)
        #axx.set_ylabel(r'mz', fontsize=10)
        #ax.set_xlim(size/2 -20, size/2 +20 )
        #ax.set_ylim(-20, 20 )
    #================================================================
    # function adds a direction of @Q to the plot, as well as an inset with
    # the rotation along @Q
    #================================================================
    def SSdetails(ax):
        size = spinlattice.size
        Q = spinlattice.Q
        ax.arrow(0, 0, Q[0]*size, Q[1]*size, head_width=1, head_length=1, color='k', ls='-', width=0.00002)
    #================================================================
    # main
    #================================================================
    fig = plt.figure()
    fig.set_size_inches(6,6)
    plt.subplots_adjust(wspace=0.3,hspace=0.3)
    ax0 = fig.add_subplot(1,1,1)
    ax0.set_xlabel('x / a', fontsize=20)
    ax0.set_ylabel('y / a', fontsize=20)
    ax0.xaxis.set_tick_params(labelsize=15, direction='in', which='both')
    ax0.yaxis.set_tick_params(labelsize=15, direction='in', which='both')
    X,Y = spinlattice.X, spinlattice.Y
    mx, my, mz = spinlattice.mx, spinlattice.my, spinlattice.mz
    # get color for spins depending on s^z
    c =1.0 -(np.arctan2(mz,np.sqrt(1-np.asarray(mz)**2)) + np.pi/2.0)/np.pi
    c = plt.cm.hsv(c*0.7)
    # plot results
    ax0.quiver(X,Y, mx, my, scale=10, units='width', pivot='middle', color=c, width=0.005)
    ax0.scatter(X,Y, marker='.', c=c)
    if details == 'DW':
        DWdetails(ax0)
    elif details == 'Sk':
        Skdetails(ax0)
    elif details == 'SS':
        SSdetails(ax0)
    if zoom != None:
        # BSP for zoom in center : zoom = [spinlattice.size/2, 0, 10]
        xc, yc, dist = zoom
        ax0.set_xlim(xc -dist, xc +dist)
        ax0.set_ylim(yc -dist, yc +dist)
    else :
        ax0.axis('equal')
    plt.tight_layout()
    cwd = os.getcwd()
    plt.savefig(cwd + '/' + filename)




#=============================================
# function for visualisation of hessian eigenvectors
#=============================================
def show_eigenvector(vectorlattice):
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MultipleLocator, NullFormatter, LogLocator
    # renormalize vectors
    norm = 1/max(vectorlattice.magmom)
    # plot like @show_lattice
    fig = plt.figure()
    fig.set_size_inches(4,4)
    plt.subplots_adjust(left=0.01,right=0.99,top=0.99,bottom=0.01)
    ax0 = fig.add_subplot(1,1,1)
    #ax0.set_xlabel('x / a', fontsize=20)
    #ax0.set_ylabel('y / a', fontsize=20)
    ax0.xaxis.set_tick_params(labelsize=15, direction='in', which='both')
    ax0.yaxis.set_tick_params(labelsize=15, direction='in', which='both')
    ax0.xaxis.set_major_formatter(NullFormatter())
    ax0.yaxis.set_major_formatter(NullFormatter())

    X,Y = vectorlattice.X, vectorlattice.Y
    mx, my, mz = vectorlattice.mx*norm, vectorlattice.my*norm, vectorlattice.mz*norm
    c = np.arctan2(mz,1)
    if c.ptp() > 0 :
        c = (c.ravel() - c.min()) / c.ptp()
        c = 1 - np.concatenate((c, np.repeat(c, 2)))
        c = plt.cm.seismic(1-c)
    else :
        c = plt.cm.seismic([0 for n in range(len(mz))])
    #ax0.quiver(X,Y, mx, my, scale=15, units='width', pivot='middle', linewidths=1, color=c)
    widths=[1.8 for x in range(mx.size)]
    ax0.quiver(X,Y, mx, my, scale=14, pivot='middle', linewidths=widths, edgecolors=c, color=c, headwidth=6)
    ax0.scatter(X,Y, marker='.', s=4, c=c)
    #ax0.axis('equal')
    ax0.set_xlim(vectorlattice.size/2 -10, vectorlattice.size/2 +10 )
    ax0.set_ylim(-10, 10 )
    #plt.tight_layout()
    cwd = os.getcwd()
    plt.savefig(cwd + '/vectorlattice.png')


#=============================================
# function for visualisation of hessian eigenvectors
#=============================================
def show_eigenvector_translation(spinlattice, vectorlattice, amplitude):
    import matplotlib.pyplot as plt
    from magnetisations import rotate_to_axis, rotation_matrix, rotate_spins, SpinLattice
    # renormalize vectors
    # plot like @show_lattice

    if spinlattice.size != vectorlattice.size :
        print 'original lattice and eigenvector are of different sizes'
        return 0

    fig = plt.figure()
    fig.set_size_inches(8,8)
    plt.subplots_adjust(wspace=0.3,hspace=0.3)
    ax0 = fig.add_subplot(1,1,1)
    ax0.set_xlabel('x / a', fontsize=20)
    ax0.set_ylabel('y / a', fontsize=20)
    ax0.xaxis.set_tick_params(labelsize=15, direction='in', which='both')
    ax0.yaxis.set_tick_params(labelsize=15, direction='in', which='both')
    X,Y = vectorlattice.X, vectorlattice.Y
    mx, my, mz = [], [], []
    # normalise the eigenvectors, so that the bigest corresponds to 1
    norm = 1/max(vectorlattice.magmom)

    # for each spin:
    #   find the axis of rotation as the cross product of the spin and the corresponding component of the eigenvector
    #   rotate each spin in this direction using @amplitude*magnitude(eig vec) as angle
    for m in range(len(spinlattice.mx)):
        axis, ang = rotate_to_axis([vectorlattice.mx[m], vectorlattice.my[m], vectorlattice.mz[m]], [spinlattice.mx[m], spinlattice.my[m], spinlattice.mz[m]])
        mat = rotation_matrix(axis, amplitude*vectorlattice.magmom[m]*norm)
        tempx, tempy, tempz = rotate_spins([spinlattice.mx[m]], [spinlattice.my[m]], [spinlattice.mz[m]], mat)
        mx.append(tempx)
        my.append(tempy)
        mz.append(tempz)

    c = np.arctan2(mz,1)
    if c.ptp() > 0 :
        c = (c.ravel() - c.min()) / c.ptp()
        c = 1 - np.concatenate((c, np.repeat(c, 2)))
        c = plt.cm.hsv(c*0.7)
    else :
        c = plt.cm.hsv([0 for n in range(len(mz))])
    ax0.quiver(X,Y, mx, my, scale=8, units='width', pivot='middle', color=c)
    ax0.scatter(X,Y, marker='.', c=c)
    ax0.axis('equal')
    ax0.set_xlim(spinlattice.size/2 -10, spinlattice.size/2 +10 )
    ax0.set_ylim(-10, 10 )
    #plt.tight_layout()
    cwd = os.getcwd()
    plt.savefig(cwd + '/translated_lattice_amp_'+ str(amplitude) + '.png')







#=============================================
# function to visualize the topological density
# of every unit cell of the lattice.
#=============================================
def show_topodensity(spinlattice, filename='topolodensity.png', zoom=None):
    import matplotlib.pyplot as plt
    from propertyfunctions import get_spherical_area

    fig = plt.figure()
    fig.set_size_inches(8,8)
    plt.subplots_adjust(wspace=0.3,hspace=0.3)
    ax0 = fig.add_subplot(1,1,1)
    ax0.set_xlabel('x / a', fontsize=20)
    ax0.set_ylabel('y / a', fontsize=20)
    ax0.axis('equal')
    ax0.xaxis.set_tick_params(labelsize=15, direction='in', which='both')
    ax0.yaxis.set_tick_params(labelsize=15, direction='in', which='both')

    X,Y = spinlattice.X, spinlattice.Y
    mx, my, mz = spinlattice.mx, spinlattice.my, spinlattice.mz
    size = int(np.sqrt(len(mx)))
    xs, ys, qs = [], [], []
    Q_neg, Q_pos = 0., 0.
    for n in range(size-1):
        for m in range(size-1):
            index1 = n*size + m
            index2 = (n+1)*(size-1) + (m+1) +n
            index3 = (n+1)*(size-1) + (m+2) +n
            index4 = n*size + (m+1)
            S1 = np.asarray([my[index1], mx[index1], mz[index1]])
            S2 = np.asarray([my[index2], mx[index2], mz[index2]])
            S3 = np.asarray([my[index3], mx[index3], mz[index3]])
            S4 = np.asarray([my[index4], mx[index4], mz[index4]])

            # calculate spherical area of the first triangle in unitcell
            area1 = get_spherical_area(S1, S2, S3)
            qs.append(area1)
            xs.append([X[index1], X[index2], X[index3]])
            ys.append([Y[index1], Y[index2], Y[index3]])
            # calculate 2 triangle in unitcell
            area2 = get_spherical_area(S1, S3, S4)
            qs.append(area2)
            xs.append([X[index1], X[index3], X[index4]])
            ys.append([Y[index1], Y[index3], Y[index4]])

            # CHECK FOR POSITIVE AND NEGATIV PARTIAL CHARGES
            if area1 < 0. :
                Q_neg += area1
            elif area1 > 0. :
                Q_pos += area1
            if area2 < 0. :
                Q_neg += area2
            elif area2 > 0. :
                Q_pos += area2

    print 'Q_neg = ', Q_neg/4./np.pi
    print 'Q_pos = ', Q_pos/4./np.pi
    Q = sum(qs)/4./np.pi

    #c = np.arctan2(qs,max(max(qs), abs(min(qs))))
    #c = (c.ravel() - c.min()) / c.ptp()
    #c = np.concatenate((c, np.repeat(c, 2)))
    #c = plt.cm.viridis(c)

    max_value = max([abs(q) for q in qs])
    c = plt.cm.seismic(-np.array(qs)/max_value/2.+0.5)
    # ZOOM FOR FASTER PLOTTING
    if zoom != None:
        # BSP for zoom in center : zoom = [spinlattice.size/2, 0, 10]
        xc, yc, dist = zoom
        ax0.set_xlim(xc -dist, xc +dist)
        ax0.set_ylim(yc -dist, yc +dist)
    for p in range(len(qs)):
        if zoom != None :
            if any([xs[p][n] > xc+dist for n in range(3)]) or any([xs[p][n] < xc-dist for n in range(3)]) or any([ys[p][n] > yc+dist for n in range(3)]) or any([ys[p][n] < yc-dist for n in range(3)]) :
                continue
            else :
                ax0.plot(xs[p], ys[p], marker='o', markersize=3, color='k', ls='')
                ax0.fill(xs[p], ys[p], c=c[p])
        else :
            ax0.plot(xs[p], ys[p], marker='o', markersize=3, color='k', ls='')
            ax0.fill(xs[p], ys[p], c=c[p])
    #fig.colorbar(plt.cm.ScalarMappable(), ax=ax0)
    #ax0.set_xlim(spinlattice.size/2 -10, spinlattice.size/2 +10 )
    #ax0.set_ylim(-10, 10)
    plt.tight_layout()
    cwd = os.getcwd()
    plt.savefig(cwd + '/' + filename)


#============================================
# function that creates a histogram of all angles,
# up to 6 shells of neighbours are considered
#============================================
def show_anglehist(spinlattice):
    import matplotlib.pyplot as plt
    #================================================================
    # the fuction runs through all lattice points and checks all neighbours relative positions
    # to avoid double counting for point n just points m\in{n, size} are considered
    # if position matches a shell distant, add the angle to the prober bin
    #================================================================
    def NNangles_hex(splat):
        size =len(splat.mz)
        #eps = np.finfo(np.float32).eps
        bin1, bin2, bin3, bin4, bin5, bin6 = [], [], [], [], [], []
        for n in range(size):
            Rn = [splat.X[n], splat.Y[n]]
            Mn = [splat.mx[n], splat.my[n], splat.mz[n]]
            for m in range(n+1, size):
                Rm = [splat.X[m], splat.Y[m]]
                Mm = [splat.mx[m], splat.my[m], splat.mz[m]]
                d = round(dist(Rn, Rm), 5)
                if d < 4 :
                    if d == 1.0: bin1.append(angle(Mn,Mm))
                    elif d == 1.73205: bin2.append(angle(Mn,Mm))
                    elif d == 2.0: bin3.append(angle(Mn,Mm))
                    elif d == 2.64575: bin4.append(angle(Mn,Mm))
                    elif d == 3.0: bin5.append(angle(Mn,Mm))
                    elif d == 3.46410: bin6.append(angle(Mn,Mm))
        return [np.asarray(bin1), np.asarray(bin2), np.asarray(bin3), np.asarray(bin4), np.asarray(bin5), np.asarray(bin6)]
    #================================================================
    # funtion for the distance of 2 n-dimensional vectos @x, @y
    #================================================================
    def dist(x,y):
        assert len(x) == len(y)
        d = 0.0
        for n in range(len(x)):
            d += (x[n] - y[n])**2
        return np.sqrt(d)
    #================================================================
    # function returns the angle between to n-dimensional vectors in degree
    #================================================================
    def angle(x,y):
        assert len(x) == len(y)
        ang = np.dot(x,y)
        if ang > 1.0 :
            ang = ang - np.finfo(np.float32).eps
        return np.arccos(ang) *180.0/np.pi
    #================================================================
    # main
    #================================================================
    fig=plt.figure()
    fig.set_size_inches(8,8)
    ax0 = fig.add_subplot(1,1,1)
    ax0.set_ylabel('count', fontsize=20)
    ax0.set_xlabel(r'$\phi$ /deg', fontsize=20)
    ax0.xaxis.set_tick_params(labelsize=15, direction='in', which='both')
    ax0.yaxis.set_tick_params(labelsize=15, direction='in', which='both')
    colors = ['red', 'tan', 'lime', 'blue', 'violet', 'darkgreen']
    ks = ['k', 'k', 'k', 'k', 'k', 'k']
    labels = ['nn=1', 'nn=2', 'nn=3', 'nn=4', 'nn=5', 'nn=6']
    bins = NNangles_hex(spinlattice)
    #bins = [np.random.randn(n) for n in [10, 9, 8, 7, 6, 5]]
    ax0.hist(bins, 15, color=colors, density=False, histtype='bar', label=labels)
    ax0.hist(bins, 15, color=ks, density=False, histtype='step', fill=False)
    plt.legend(loc='upper center', fontsize=15)
    plt.tight_layout()




#=====================================================================
# IMPUT: SpinLattice object @sp and a target .png-file with name @image_name
# OUTPUT: povray image of lattice with name  @image_name
# DISCRIBTION: The function uses vapory-library to render a povray image of
#              the given SpinLattice object. The colormap can be choosen to
#              any of plt.cm. Notice that np.arctan2(y,x) has reversed order
#              of entries. According to these anles, every spin is rotated:
#              @theta around y-axis, @phi around z-axis
#=====================================================================
def spinpov(sp, image_name):
    import matplotlib.pyplot as plt
    from magnetisations import SpinLattice
    from matplotlib.colors import LinearSegmentedColormap
    import sys
    sys.path.append('/home/goerzen/libraries/vapory')
    from vapory import *
    # set standard objects
    # Note that povray uses a left handed coordinate system. Therefore we change
    # it to right handed by defining @up and @right.
    #gratio = 1.61803398875
    gratio = 1.0
    camera = Camera('sky', [0,0,1],
                    'look_at', [sp.size//2, 0,0],
                    'location', [sp.size/2.0,0,sp.size/2.],
                    'up', [0,0,1],
                    'right', [-1,0,0],
                    'angle', 40)
    objects = []
    #objects.append(LightSource([sp.size//2, -sp.size//2, 40], 'color', [1.,1.,1.],  ))
    objects.append(Background( "color", [1,1,1] ))
    objects.append(LightSource([sp.size/2.0, 0, 30], 0.7, 'area_light', (5,0,0), (0,5,0), 5,5, 'adaptive', 1, 'jitter'  ))
    # get the color code according to @sp.mz from plt.cm
    c =1.0 -(np.arctan2(sp.mz,np.sqrt(1-np.asarray(sp.mz)**2)) + np.pi/2.0)/np.pi
    #========================================
    # create your own colorcode, if wanted
    #cmap_name = 'wbr'
    #colors = [(1, 1, 1), (0, 0, 0), (0.545, 0, 0)]
    #cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=265)
    #c = cm(c)
    #========================================
    #c = plt.cm.inferno(c)
    c = plt.cm.hsv(c*0.7)
    # add cons to list of objects. rotation is in [deg]
    for n in range(len(sp.X)):
        theta = np.arccos(sp.mz[n])*180.0/np.pi
        phi = np.arctan2(sp.my[n],sp.mx[n])*180.0/np.pi
        cone = Cone([0.0, 0.0,0.5], 0.0, [0.0, 0.0, -0.5], 0.38,
                    'rotate', [0., theta, 0.],
                    'rotate', [0., 0., phi],
                    'translate', [gratio*sp.X[n], gratio*sp.Y[n], gratio*sp.Z[n]],
                    Texture(Pigment('color', c[n][:-1])),
                    Finish('ambient', 1.0, 'reflection',0.0,'metallic', 0.0))
        objects.append(cone)
    # build the scene and render
    scene = Scene( camera, objects= objects)
    scene.render(image_name, width=700, height=700, antialiasing=0.001)





def show_fft(sp, complex=False):
    from mpl_toolkits import mplot3d
    from mpl_toolkits.mplot3d import proj3d
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MultipleLocator, NullFormatter
    from scipy.interpolate import griddata

    def lattice_fft(sp):
        L = sp.size
        xfft = np.fft.ifft2(np.asarray(sp.mx).reshape(L, L)).transpose()
        xfft = np.fft.fftshift(xfft).reshape(sp.size**2)
        yfft = np.fft.ifft2(np.asarray(sp.my).reshape(L, L)).transpose()
        yfft = np.fft.fftshift(yfft).reshape(sp.size**2)
        zfft = np.fft.ifft2(np.asarray(sp.mz).reshape(L, L)).transpose()
        zfft = np.fft.fftshift(zfft).reshape(sp.size**2)
        return xfft, yfft, zfft

    def SpinD_mesh(xdata, ydata, zdata):
        xi = np.linspace(min(xdata), max(xdata), 200)
        yi = np.linspace(min(ydata), max(ydata), 200)
        xig, yig = np.meshgrid(xi, yi)
        zig = griddata((xdata, ydata), zdata, (xi[None,:], yi[:,None]), method='cubic')
        return xig, yig, zig

    def reciproce_lattice(sp):
        latvec = np.asarray([ [0.5, -0.86602540378, 0.0], [0.5, 0.86602540378, 0.0], [0.0, 0.0, 1.0] ])
        spat = np.dot(latvec[0], np.cross(latvec[1], latvec[2]))
        recvec = np.asarray([ np.cross(latvec[1], latvec[2]), np.cross(latvec[2], latvec[0]), np.cross(latvec[0], latvec[1]) ])*2.0*np.pi/spat
        recX, recY, recZ = [], [], []
        for n in range(sp.size):
            r0 = n*recvec[0]/np.linalg.norm(recvec[0])/sp.size*2
            for m in range(sp.size) :
                r = r0 + m*recvec[1]/np.linalg.norm(recvec[1])/sp.size*2
                recX.append(r[0])
                recY.append(r[1])
                recZ.append(r[2])
        # resize recX, recY to the form of the brillouin zone
        recX = [ (-1.0 +2.0*(x-min(recX))/(max(recX)-min(recX))) for x in recX ]
        recY = [ np.cos(np.pi/6.0)*0.666*(-1.0 +2.0*(y-min(recY))/(max(recY)-min(recY))) for y in recY ]
        return recX, recY, recZ

    def simple_lattice(sp):
        simX, simY, simZ = [], [], []
        for n in range(sp.size):
            r0 = [n,0,0]
            for m in range(sp.size) :
                r = r0 + [0,m,0]
                simX.append(r[0]/sp.size)
                simY.append(r[1]/sp.size)
                simZ.append(r[2]/sp.size)
        return simX, simY, simZ

    fig=plt.figure()
    fig.set_size_inches(8,2)
    ax0 = fig.add_subplot(1,3,1)
    ax1 = fig.add_subplot(1,3,2)
    ax2 = fig.add_subplot(1,3,3)
    plt.subplots_adjust(wspace=0.05,hspace=0.05)
    ax0.set_title(r'FFT(s$_{x}$)')
    ax1.set_title(r'FFT(s$_{y}$)')
    ax2.set_title(r'FFT(s$_{z}$)')
    ax0.axis('equal')
    ax1.axis('equal')
    ax2.axis('equal')
    ax0._axis3don = False
    ax1._axis3don = False
    ax2._axis3don = False
    ax0.xaxis.set_tick_params(labelsize=8, direction='in', which='both')
    ax0.yaxis.set_tick_params(labelsize=8, direction='in', which='both')
    ax1.xaxis.set_tick_params(labelsize=8, direction='in', which='both')
    ax1.yaxis.set_tick_params(labelsize=8, direction='in', which='both')
    ax2.xaxis.set_tick_params(labelsize=8, direction='in', which='both')
    ax2.yaxis.set_tick_params(labelsize=8, direction='in', which='both')

    ax0.spines['left'].set_position('center')
    ax0.spines['bottom'].set_position('center')
    # Eliminate upper and right axes
    ax0.spines['right'].set_color('none')
    ax0.spines['top'].set_color('none')
    # Show ticks in the left and lower axes only
    ax0.xaxis.set_ticks_position('bottom')
    ax0.yaxis.set_ticks_position('left')

    ax1.spines['left'].set_position('center')
    ax1.spines['bottom'].set_position('center')
    # Eliminate upper and right axes
    ax1.spines['right'].set_color('none')
    ax1.spines['top'].set_color('none')
    # Show ticks in the left and lower axes only
    ax1.xaxis.set_ticks_position('bottom')
    ax1.yaxis.set_ticks_position('left')

    ax2.spines['left'].set_position('center')
    ax2.spines['bottom'].set_position('center')
    # Eliminate upper and right axes
    ax2.spines['right'].set_color('none')
    ax2.spines['top'].set_color('none')
    # Show ticks in the left and lower axes only
    ax2.xaxis.set_ticks_position('bottom')
    ax2.yaxis.set_ticks_position('left')

    ax0.set_xticks( np.array([-1, -0.666, 0.666, 1]))
    ax0.set_xticklabels(['-M', '-K', 'K', 'M'])
    ax0.yaxis.set_major_formatter(NullFormatter())

    ax1.set_xticks( np.array([-1, -0.666, 0.666, 1]))
    ax1.set_xticklabels(['-M', '-K', 'K', 'M'])
    ax1.yaxis.set_major_formatter(NullFormatter())

    ax2.set_xticks( np.array([-1, -0.666, 0.666, 1]))
    ax2.set_xticklabels(['-M', '-K', 'K', 'M'])
    ax2.yaxis.set_major_formatter(NullFormatter())

    # main call
    xfft, yfft, zfft = lattice_fft(sp)
    # get the reciproke coordinates
    recX, recY, recZ = reciproce_lattice(sp)
    #recX, recY, recZ = simple_lattice(sp)
    xigX, yigX, zigX = SpinD_mesh(recX, recY, np.absolute(xfft))
    xigY, yigY, zigY = SpinD_mesh(recX, recY, np.absolute(yfft))
    xigZ, yigZ, zigZ = SpinD_mesh(recX, recY, np.absolute(zfft))
    lim = max(max(np.absolute(sp.mx)), max(np.absolute(sp.my)), max(np.absolute(sp.mz)))
    # note: if colors shall be interpolated use @shading='gouraud'
    ax0.pcolormesh(xigX, yigX, zigX, shading='gouraud', cmap='coolwarm')
    ax1.pcolormesh(xigY, yigY, zigY, shading='gouraud', cmap='coolwarm')
    ax2.pcolormesh(xigZ, yigZ, zigZ, shading='gouraud', cmap='coolwarm')

    ax0.text(0.55, np.cos(np.pi/6.0)*0.666*0.5, "M", ha="center", va="center", rotation=0, size=8)
    ax0.plot(0.5, np.cos(np.pi/6.0)*0.666*0.5, marker='o', color='k', markersize='3')

    ax1.text(0.55, np.cos(np.pi/6.0)*0.666*0.5, "M", ha="center", va="center", rotation=0, size=8)
    ax1.plot(0.5, np.cos(np.pi/6.0)*0.666*0.5, marker='o', color='k', markersize='3')

    ax2.text(0.55, np.cos(np.pi/6.0)*0.666*0.5, "M", ha="center", va="center", rotation=0, size=8)
    ax2.plot(0.5, np.cos(np.pi/6.0)*0.666*0.5, marker='o', color='k', markersize='3')

    plt.tight_layout()
    cwd = os.getcwd()
    plt.savefig(cwd + '/spinlattice_fft.png')

    # make a new plot with real and imaginary components
    if complex :

        fig2=plt.figure()
        fig2.set_size_inches(8,2)
        ax0 = fig2.add_subplot(2,3,1)
        ax1 = fig2.add_subplot(2,3,2)
        ax2 = fig2.add_subplot(2,3,3)
        ax01 = fig2.add_subplot(2,3,4)
        ax11 = fig2.add_subplot(2,3,5)
        ax21 = fig2.add_subplot(2,3,6)
        plt.subplots_adjust(wspace=0.05,hspace=0.05)
        ax0.set_title(r'$\Re$(FFT(s$_{x}$))')
        ax1.set_title(r'$\Re$(FFT(s$_{y}$))')
        ax2.set_title(r'$\Re$(FFT(s$_{z}$))')
        ax01.set_title(r'$\Im$(FFT(s$_{x}$))')
        ax11.set_title(r'$\Im$(FFT(s$_{y}$))')
        ax21.set_title(r'$\Im$(FFT(s$_{z}$))')
        ax0.axis('equal')
        ax1.axis('equal')
        ax2.axis('equal')
        ax01.axis('equal')
        ax11.axis('equal')
        ax21.axis('equal')
        ax0._axis3don = False
        ax1._axis3don = False
        ax2._axis3don = False
        ax01._axis3don = False
        ax11._axis3don = False
        ax21._axis3don = False
        ax0.xaxis.set_tick_params(labelsize=15, direction='in', which='both')
        ax0.yaxis.set_tick_params(labelsize=15, direction='in', which='both')
        ax1.xaxis.set_tick_params(labelsize=15, direction='in', which='both')
        ax1.yaxis.set_tick_params(labelsize=15, direction='in', which='both')
        ax2.xaxis.set_tick_params(labelsize=15, direction='in', which='both')
        ax2.yaxis.set_tick_params(labelsize=15, direction='in', which='both')
        ax01.xaxis.set_tick_params(labelsize=15, direction='in', which='both')
        ax01.yaxis.set_tick_params(labelsize=15, direction='in', which='both')
        ax11.xaxis.set_tick_params(labelsize=15, direction='in', which='both')
        ax11.yaxis.set_tick_params(labelsize=15, direction='in', which='both')
        ax21.xaxis.set_tick_params(labelsize=15, direction='in', which='both')
        ax21.yaxis.set_tick_params(labelsize=15, direction='in', which='both')

        ax0.spines['left'].set_position('center')
        ax0.spines['bottom'].set_position('center')
        # Eliminate upper and right axes
        ax0.spines['right'].set_color('none')
        ax0.spines['top'].set_color('none')
        # Show ticks in the left and lower axes only
        ax0.xaxis.set_ticks_position('bottom')
        ax0.yaxis.set_ticks_position('left')

        ax1.spines['left'].set_position('center')
        ax1.spines['bottom'].set_position('center')
        # Eliminate upper and right axes
        ax1.spines['right'].set_color('none')
        ax1.spines['top'].set_color('none')
        # Show ticks in the left and lower axes only
        ax1.xaxis.set_ticks_position('bottom')
        ax1.yaxis.set_ticks_position('left')

        ax2.spines['left'].set_position('center')
        ax2.spines['bottom'].set_position('center')
        # Eliminate upper and right axes
        ax2.spines['right'].set_color('none')
        ax2.spines['top'].set_color('none')
        # Show ticks in the left and lower axes only
        ax2.xaxis.set_ticks_position('bottom')
        ax2.yaxis.set_ticks_position('left')

        ax01.spines['left'].set_position('center')
        ax01.spines['bottom'].set_position('center')
        # Eliminate upper and right axes
        ax01.spines['right'].set_color('none')
        ax01.spines['top'].set_color('none')
        # Show ticks in the left and lower axes only
        ax01.xaxis.set_ticks_position('bottom')
        ax01.yaxis.set_ticks_position('left')

        ax11.spines['left'].set_position('center')
        ax11.spines['bottom'].set_position('center')
        # Eliminate upper and right axes
        ax11.spines['right'].set_color('none')
        ax11.spines['top'].set_color('none')
        # Show ticks in the left and lower axes only
        ax11.xaxis.set_ticks_position('bottom')
        ax11.yaxis.set_ticks_position('left')

        ax21.spines['left'].set_position('center')
        ax21.spines['bottom'].set_position('center')
        # Eliminate upper and right axes
        ax21.spines['right'].set_color('none')
        ax21.spines['top'].set_color('none')
        # Show ticks in the left and lower axes only
        ax21.xaxis.set_ticks_position('bottom')
        ax21.yaxis.set_ticks_position('left')

        ax0.set_xticks( np.array([-1, -0.666, 0.666, 1]))
        ax0.set_xticklabels(['-M', '-K', 'K', 'M'])
        ax0.yaxis.set_major_formatter(NullFormatter())

        ax1.set_xticks( np.array([-1, -0.666, 0.666, 1]))
        ax1.set_xticklabels(['-M', '-K', 'K', 'M'])
        ax1.yaxis.set_major_formatter(NullFormatter())

        ax2.set_xticks( np.array([-1, -0.666, 0.666, 1]))
        ax2.set_xticklabels(['-M', '-K', 'K', 'M'])
        ax2.yaxis.set_major_formatter(NullFormatter())

        ax01.set_xticks( np.array([-1, -0.666, 0.666, 1]))
        ax01.set_xticklabels(['-M', '-K', 'K', 'M'])
        ax01.yaxis.set_major_formatter(NullFormatter())

        ax11.set_xticks( np.array([-1, -0.666, 0.666, 1]))
        ax11.set_xticklabels(['-M', '-K', 'K', 'M'])
        ax11.yaxis.set_major_formatter(NullFormatter())

        ax21.set_xticks( np.array([-1, -0.666, 0.666, 1]))
        ax21.set_xticklabels(['-M', '-K', 'K', 'M'])
        ax21.yaxis.set_major_formatter(NullFormatter())

        xigX_re, yigX_re, zigX_re = SpinD_mesh(recX, recY, [z.real for z in xfft])
        xigY_re, yigY_re, zigY_re = SpinD_mesh(recX, recY, [z.real for z in yfft])
        xigZ_re, yigZ_re, zigZ_re = SpinD_mesh(recX, recY, [z.real for z in zfft])

        xigX_im, yigX_im, zigX_im = SpinD_mesh(recX, recY, [z.imag for z in xfft])
        xigY_im, yigY_im, zigY_im = SpinD_mesh(recX, recY, [z.imag for z in yfft])
        xigZ_im, yigZ_im, zigZ_im = SpinD_mesh(recX, recY, [z.imag for z in zfft])

        ax0.pcolormesh(xigX_re, yigX_re, zigX_re, shading='gouraud', cmap='seismic')
        ax1.pcolormesh(xigY_re, yigY_re, zigY_re, shading='gouraud', cmap='seismic')
        ax2.pcolormesh(xigZ_re, yigZ_re, zigZ_re, shading='gouraud', cmap='seismic')

        ax01.pcolormesh(xigX_im, yigX_im, zigX_im, shading='gouraud', cmap='seismic')
        ax11.pcolormesh(xigY_im, yigY_im, zigY_im, shading='gouraud', cmap='seismic')
        ax21.pcolormesh(xigZ_im, yigZ_im, zigZ_im, shading='gouraud', cmap='seismic')


    plt.tight_layout()
    #cwd = os.getcwd()
    #plt.savefig(cwd + '/spinlattice_fft.png')
    plt.show()









def show_hilbert_transform(sp):
    from mpl_toolkits import mplot3d
    from mpl_toolkits.mplot3d import proj3d
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MultipleLocator, NullFormatter
    from scipy.interpolate import griddata
    from scipy import signal


    def lattice_fft(sp):
        L = sp.size
        xfft = np.fft.ifft2(np.asarray(sp.mx).reshape(L, L)).transpose()
        xfft = np.fft.fftshift(xfft).reshape(sp.size**2)
        yfft = np.fft.ifft2(np.asarray(sp.my).reshape(L, L)).transpose()
        yfft = np.fft.fftshift(yfft).reshape(sp.size**2)
        zfft = np.fft.ifft2(np.asarray(sp.mz).reshape(L, L)).transpose()
        zfft = np.fft.fftshift(zfft).reshape(sp.size**2)
        return xfft, yfft, zfft

    def lattice_hilbert_trafo(sp):
        L = sp.size

        xfft, yfft, zfft = lattice_fft(sp)

        xfft = signal.hilbert2(np.asarray(np.absolute(xfft)).reshape(L, L))
        xfft = np.imag(xfft).reshape(sp.size**2)
        #xfft = np.fft.fftshift(xfft).reshape(sp.size**2)
        #xfft = np.fft.fftshift(xfft).reshape(sp.size**2)
        yfft = signal.hilbert2(np.asarray(np.absolute(yfft)).reshape(L, L))
        yfft = np.imag(yfft).reshape(sp.size**2)
        #yfft = np.fft.fftshift(yfft).reshape(sp.size**2)
        zfft = signal.hilbert2(np.asarray(np.absolute(zfft)).reshape(L, L))
        zfft = np.imag(zfft).reshape(sp.size**2)
        #zfft = np.fft.fftshift(zfft).reshape(sp.size**2)
        return xfft, yfft, zfft

    def SpinD_mesh(xdata, ydata, zdata):
        xi = np.linspace(min(xdata), max(xdata), 200)
        yi = np.linspace(min(ydata), max(ydata), 200)
        #xi = np.linspace(-1.17, 1.17, 200)
        #yi = np.linspace(-np.cos(np.pi/6.0), np.cos(np.pi/6.0), 200)
        xig, yig = np.meshgrid(xi, yi)
        zig = griddata((xdata, ydata), zdata, (xi[None,:], yi[:,None]), method='cubic')
        return xig, yig, zig

    def reciproce_lattice(sp):
        latvec = np.asarray([ [0.5, -0.86602540378, 0.0], [0.5, 0.86602540378, 0.0], [0.0, 0.0, 1.0] ])
        spat = np.dot(latvec[0], np.cross(latvec[1], latvec[2]))
        recvec = np.asarray([ np.cross(latvec[1], latvec[2]), np.cross(latvec[2], latvec[0]), np.cross(latvec[0], latvec[1]) ])*2.0*np.pi/spat
        recX, recY, recZ = [], [], []
        for n in range(sp.size):
            r0 = n*recvec[0]/np.linalg.norm(recvec[0])/sp.size*2
            for m in range(sp.size) :
                r = r0 + m*recvec[1]/np.linalg.norm(recvec[1])/sp.size*2
                recX.append(r[0])
                recY.append(r[1])
                recZ.append(r[2])
        # resize recX, recY to the form of the brillouin zone
        recX = [ (-1.0 +2.0*(x-min(recX))/(max(recX)-min(recX))) for x in recX ]
        recY = [ np.cos(np.pi/6.0)*0.666*(-1.0 +2.0*(y-min(recY))/(max(recY)-min(recY))) for y in recY ]
        return recX, recY, recZ

    # main call
    xfft, yfft, zfft = lattice_hilbert_trafo(sp)

    fig=plt.figure()
    fig.set_size_inches(8,4)
    ax0 = fig.add_subplot(1,3,1)
    ax1 = fig.add_subplot(1,3,2)
    ax2 = fig.add_subplot(1,3,3)
    plt.subplots_adjust(wspace=0.05,hspace=0.05)
    ax0.set_title(r'FFT(s$_{x}$)')
    ax1.set_title(r'FFT(s$_{y}$)')
    ax2.set_title(r'FFT(s$_{z}$)')
    ax0.axis('equal')
    ax1.axis('equal')
    ax2.axis('equal')
    ax0._axis3don = False
    ax1._axis3don = False
    ax2._axis3don = False
    ax0.xaxis.set_tick_params(labelsize=15, direction='in', which='both')
    ax0.yaxis.set_tick_params(labelsize=15, direction='in', which='both')
    ax1.xaxis.set_tick_params(labelsize=15, direction='in', which='both')
    ax1.yaxis.set_tick_params(labelsize=15, direction='in', which='both')
    ax2.xaxis.set_tick_params(labelsize=15, direction='in', which='both')
    ax2.yaxis.set_tick_params(labelsize=15, direction='in', which='both')

    ax0.spines['left'].set_position('center')
    ax0.spines['bottom'].set_position('center')
    # Eliminate upper and right axes
    ax0.spines['right'].set_color('none')
    ax0.spines['top'].set_color('none')
    # Show ticks in the left and lower axes only
    ax0.xaxis.set_ticks_position('bottom')
    ax0.yaxis.set_ticks_position('left')

    ax1.spines['left'].set_position('center')
    ax1.spines['bottom'].set_position('center')
    # Eliminate upper and right axes
    ax1.spines['right'].set_color('none')
    ax1.spines['top'].set_color('none')
    # Show ticks in the left and lower axes only
    ax1.xaxis.set_ticks_position('bottom')
    ax1.yaxis.set_ticks_position('left')

    ax2.spines['left'].set_position('center')
    ax2.spines['bottom'].set_position('center')
    # Eliminate upper and right axes
    ax2.spines['right'].set_color('none')
    ax2.spines['top'].set_color('none')
    # Show ticks in the left and lower axes only
    ax2.xaxis.set_ticks_position('bottom')
    ax2.yaxis.set_ticks_position('left')

    ax0.set_xticks( np.array([-1, -0.666, 0.666, 1]))
    ax0.set_xticklabels(['-M', '-K', 'K', 'M'])
    ax0.yaxis.set_major_formatter(NullFormatter())

    ax1.set_xticks( np.array([-1, -0.666, 0.666, 1]))
    ax1.set_xticklabels(['-M', '-K', 'K', 'M'])
    ax1.yaxis.set_major_formatter(NullFormatter())

    ax2.set_xticks( np.array([-1, -0.666, 0.666, 1]))
    ax2.set_xticklabels(['-M', '-K', 'K', 'M'])
    ax2.yaxis.set_major_formatter(NullFormatter())

    # get the reciproke coordinates
    recX, recY, recZ = reciproce_lattice(sp)
    #recX, recY, recZ = simple_lattice(sp)
    xigX, yigX, zigX = SpinD_mesh(recX, recY, xfft)
    xigY, yigY, zigY = SpinD_mesh(recX, recY, yfft)
    xigZ, yigZ, zigZ = SpinD_mesh(recX, recY, zfft)
    lim = max(max(np.absolute(sp.mx)), max(np.absolute(sp.my)), max(np.absolute(sp.mz)))
    # note: if colors shall be interpolated use @shading='gouraud'
    ax0.pcolormesh(xigX, yigX, zigX, shading='gouraud', cmap='coolwarm')
    ax1.pcolormesh(xigY, yigY, zigY, shading='gouraud', cmap='coolwarm')
    ax2.pcolormesh(xigZ, yigZ, zigZ, shading='gouraud', cmap='coolwarm')

    ax0.text(0.55, np.cos(np.pi/6.0)*0.666*0.5, "M", ha="center", va="center", rotation=0, size=15)
    ax0.plot(0.5, np.cos(np.pi/6.0)*0.666*0.5, marker='o', color='k', markersize='3')

    ax1.text(0.55, np.cos(np.pi/6.0)*0.666*0.5, "M", ha="center", va="center", rotation=0, size=15)
    ax1.plot(0.5, np.cos(np.pi/6.0)*0.666*0.5, marker='o', color='k', markersize='3')

    ax2.text(0.55, np.cos(np.pi/6.0)*0.666*0.5, "M", ha="center", va="center", rotation=0, size=15)
    ax2.plot(0.5, np.cos(np.pi/6.0)*0.666*0.5, marker='o', color='k', markersize='3')

    plt.tight_layout()
    plt.show()
