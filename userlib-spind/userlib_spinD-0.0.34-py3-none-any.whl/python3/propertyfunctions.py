import numpy as np
import sys


# ============================================
# function for the topological charge of a lattice, see B.Berg and M.Luescher
# works just on a lattice constructed in the way
# the class 'Lattices' does. For other constructions
# S1,S2,S3,S4 have to be assigned disfferently.
# But the calculation of the spherical area is nice in every way.
# Input : mag = [my, mx,mz]
# Output : float Q
# ============================================
def topocharge(mag):
    Q = 0
    size = int(np.sqrt(len(mag[0])))
    for n in range(size - 1):
        for m in range(size - 1):
            index1 = n * size + m
            index2 = (n + 1) * (size - 1) + (m + 1) + n
            index3 = (n + 1) * (size - 1) + (m + 2) + n
            index4 = n * size + (m + 1)
            S1 = np.asarray([mag[0][index1], mag[1][index1], mag[2][index1]])
            S2 = np.asarray([mag[0][index2], mag[1][index2], mag[2][index2]])
            S3 = np.asarray([mag[0][index3], mag[1][index3], mag[2][index3]])
            S4 = np.asarray([mag[0][index4], mag[1][index4], mag[2][index4]])
            area1 = get_spherical_area(S1, S2, S3)
            area2 = get_spherical_area(S1, S3, S4)
            Q += area1 + area2
    return Q / 4.0 / np.pi


# ============================================
# function returns the spherical area created by three spins
# the sign of the area is the sign of the spat product S1*(S2xS3)
# inspired by implementation of B. Dupe
# ============================================
def get_spherical_area(S1, S2, S3):
    con = 1 + np.dot(S1, S2) + np.dot(S2, S3) + np.dot(S3, S1)
    # FM CASE
    if con >= 4. - 10e-8:
        area = 0.
    else:
        mat = [S1, S2, S3]
        det_mat = np.linalg.det(mat)
        # EXCEPTIONAL CASE
        if abs(con) <= 10e-8 and abs(det_mat) <= 10e-8:
            area = 0.
        # NON-EXCEPTIONAL NON-COLINEAR CASE
        else:
            area = 2.0 * np.arctan2(det_mat, con)
    return area


# ============================================
# funktion for calculation of the skyrmion radius.
# method adopted from S.v. Malottki
# Input: SpinLattice object
# ============================================
def skyrmionradius(splat):
    from scipy.optimize import curve_fit, fmin
    # ============================================
    # 2d fit function for the skyrmion profile
    # ============================================
    def sk_2dprofile(R, r0x, r0y, c, w):
        r = np.sqrt((R[0] - r0x) ** 2 + (R[1] - r0y) ** 2)
        mzs = np.cos(theta(r, c, w))
        return mzs

    # ============================================
    # analytic function for the azimuthal angle @theta of a skyrmion
    # and its derivation @dtheta_dr
    # @r is the distance from the centrum
    # @c, @w the fit parameters
    # ============================================
    def theta(r, c, w):
        comp1 = np.arcsin(np.tanh((-abs(r) - c) * 2.0 / w))
        comp2 = np.arcsin(np.tanh((-abs(r) + c) * 2.0 / w))
        return np.pi + comp1 + comp2

    def dtheta_dr(r, c, w):
        comp1 = 2.0 * np.sqrt(-np.tanh(2.0 * (-c + abs(r)) / w) ** 2 + 1) / w
        comp2 = 2.0 * np.sqrt(-np.tanh(2.0 * (c + abs(r)) / w) ** 2 + 1) / w
        return -comp1 - comp2

    # ============================================
    # calculates the radius determined by @c, @w using
    # lilley criteria
    # ============================================
    def sk_radius(c, w):
        x0 = fmin(lambda x: dtheta_dr(x, c, w), 0, disp=False, xtol=1.0E-10)[0]
        rad = x0 - theta(x0, c, w) / dtheta_dr(x0, c, w)
        return rad

    # ================================================================
    # main
    # ================================================================
    # 1) Find the minimum of magnetisation, as it is nearly the sk center
    index = np.where(splat.mz == min(splat.mz))[0][0]
    # 2) make a 2d fit to mz using sk_2dprofile function
    start_para = [splat.X[index], splat.Y[index], 2.5, 3.0]
    popt, pcov = curve_fit(sk_2dprofile, [splat.X, splat.Y], splat.mz, start_para, maxfev=2000)
    popt, pcov = curve_fit(sk_2dprofile, [splat.X, splat.Y], splat.mz, popt)
    # the estimated parameters c,w determine the Radius
    radius = sk_radius(popt[2], popt[3])
    return radius, popt, np.sqrt(np.diag(pcov))


# ============================================
# function to find the width of a domainwall using curve_fit
# ============================================
def dwwidth(splat):
    from scipy.optimize import curve_fit, fmin
    X, Y, mx, my, mz = np.asarray(splat.X), np.asarray(splat.Y), np.asarray(splat.mx), np.asarray(splat.my), np.asarray(
        splat.mz)

    # ============================================
    # 2d fit function for the domainwall profile and a straight line
    # ============================================
    def dw_2dprofile(R, r0, phi, w):
        theta = 2.0 * np.arctan(np.exp((R[0] * np.cos(phi) + R[1] * np.sin(phi) - r0) / w))
        return np.cos(theta)

    def dw_2dprofile_reduzed(R, w):
        theta = 2.0 * np.arctan(np.exp((R[0] * np.cos(init_phi) + R[1] * np.sin(init_phi) - init_r0) / w))
        return np.cos(theta)

    def gerade(x, y0, m):
        return y0 + x * m

    # ============================================
    # the functions returns the initial values for @phi, the angle between @direction
    # and the x-axis, and also @r0, the distance to the wall on this line
    # ============================================
    def get_init_values():
        # find points inside the DW and fit them with a straight line
        index = np.where(abs(mz) < 0.1)
        popt, pcov = curve_fit(gerade, X[index[0]], Y[index[0]])
        # calculate the initial guess for the angle between @direction and x-axis
        # by using the slope of the fitted straight line
        phi = np.pi / 2.0 - np.arctan(abs(popt[1]))
        # to find @r0 set arg=(r-r0)n=0 => r0=rx*cos(phi) + ry*sin(phi)
        # which corresponds to a position on the domainwall
        r0 = splat.X[index[0][0]] * np.cos(phi) + splat.Y[index[0][0]] * np.sin(phi)
        return r0, phi

    # ============================================
    # main
    # ============================================
    # determine situation: down->up, up->down
    dir = np.sign(splat.mz[0])
    # get initial values for @r0 and @phi and fit DW with them to get @init_w
    init_r0, init_phi = get_init_values()
    popt, pcov = curve_fit(dw_2dprofile_reduzed, [splat.X, splat.Y], np.asarray(splat.mz) * dir, [1.0])
    init_w = popt[0]
    start_para = [init_r0, init_phi, init_w]
    # fit the DW profile to the data using reasonable start parameters
    popt, pcov = curve_fit(dw_2dprofile, [splat.X, splat.Y], np.asarray(splat.mz) * dir, start_para)
    return popt[0], popt[1], popt[2]


# ==============================================
# INPUT: initial and final images @init and @final. optionaly the number of images
#        to generate
# OUTPUT: the methods writes the sequence of images to the folder @'geodasic_path'
# DESCRIPTION: This method calculates @steps images on the geodasic
#              path between the initial image @init and the final image
#              @final.
# CONVENTION: the initial image is @image_0 and the final @image_(steps)
# ==============================================
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
        write_STM(final, name='image_' + str(steps) + '.dat')
        if make_pov:
            spinpov(init, 'image_0')
            spinpov(final, 'image_' + str(steps))

        # for each image on the geodasic path, calculate the spin configuration
        for n in range(1, steps):
            sl = SpinLattice(size=init.size, key='hex', magmom=init.magmom[0])
            for m in range(len(init.mx)):
                axis, ang = rotate_to_axis([final.mx[m], final.my[m], final.mz[m]],
                                           [init.mx[m], init.my[m], init.mz[m]])
                mat = rotation_matrix(axis, ang * float(n) / float(steps))
                tempx, tempy, tempz = rotate_spins([init.mx[m]], [init.my[m]], [init.mz[m]], mat)
                sl.mx[m], sl.my[m], sl.mz[m] = tempx[0], tempy[0], tempz[0]
            tag = 'image_' + str(n)
            write_STM(sl, name=tag + '.dat')
            if make_pov:
                spinpov(sl, tag)


# ==============================================
# INPUT: @SPinLattice OBJECT TO WORK ON
#        @key TO SPECIFY LATTICE TYPE ('hex', OR 'quad')
#        @mode = 'translation' OR 'helicity' TO SPECIFY TYPE OF MODE
# OUTPUT: PARTITION FUNCTION CONSIDERING STATISTICAL VOLUME FOR ZERO-MODE
# DESCRIPTION: METHOD RETURNS THE GOLDSTONE-VOLUME OF A SPECIFIED CONTINUES MODE
# ==============================================
def zero_mode_partitionfunction(SL, key=None, mode=None, resolution=1e4):
    # DECIDE WHICH KIND OF MODE WE WANT TO HAVE THE VOLUME FOR
    if mode == None:
        print('ERROR: set @mode= \'translation\' or \'helicity\' ')
        exit()
    # =================================================
    # TRANSLATION MODE PART
    # =================================================
    elif mode == 'translation':
        if key == None:
            print('ERROR: set @key= \'hex\' or \'quad\' ')
            exit()
        # WE NEED THE 2D-VOLUME OF THE UNITCELL
        elif key == 'hex':
            trans_vec = np.array([[0.5, 0.86602540378, 0.0], [1., 0., 0.]])
        elif key == 'quad':
            trans_vec = np.array([[1., 0., 0.], [0., 1., 0.]])
        unitcell_span = np.cross(trans_vec[0], trans_vec[1])
        unitcell_volume = abs(unitcell_span[2])

        # TRANSLATION ALONG LATTICE VECTOR [0.5, 0.86602540378, 0.0]
        mx_tmp = [None for _ in range(len(SL.mx))]
        my_tmp = [None for _ in range(len(SL.my))]
        mz_tmp = [None for _ in range(len(SL.mz))]
        for n in range(len(SL.mx)):
            # NEW INDEX FOR TRANSLATED SPIN @n IS FOUND CONSIDERING PERIODIC BOUNDARY CONDITIONS
            if (n + 1) % SL.size != 0:
                new_index = n + 1
            else:
                new_index = (n // SL.size) * SL.size
            # COPY CURRENT SPIN TO NEW LOCATION ON TEMPORARY LATTICE @SL_new1
            mx_tmp[new_index], my_tmp[new_index], mz_tmp[new_index] = SL.mx[n], SL.my[n], SL.mz[n]
        # GET THE GEODASIC DISTANCE OF LATTICES
        geo_dist1 = geodasic_dist_data_orientated(SL.mx, SL.my, SL.mz, mx_tmp, my_tmp, mz_tmp)

        # TRANSLATION ALONG LATTICE VECTOR [1.0, 0.0, 0.0]
        for n in range(len(SL.mx)):
            # NEW INDEX FOR TRANSLATED SPIN @n IS FOUND CONSIDERING PERIODIC BOUNDARY CONDITIONS
            if n < SL.size * (SL.size - 1):
                if (n + 1) % SL.size != 0:
                    new_index = n + SL.size + 1
                else:
                    new_index = n + 1
            else:
                if (n + 1) % SL.size != 0:
                    new_index = n % SL.size + 1
                else:
                    new_index = 0
            # COPY CURRENT SPIN TO NEW LOCATION ON TEMPORARY LATTICE @SL_new2
            mx_tmp[new_index], my_tmp[new_index], mz_tmp[new_index] = SL.mx[n], SL.my[n], SL.mz[n]
        # GET THE GEODASIC DISTANCE OF LATTICES
        geo_dist2 = geodasic_dist_data_orientated(SL.mx, SL.my, SL.mz, mx_tmp, my_tmp, mz_tmp)
        return (geo_dist1 * geo_dist2) * unitcell_volume

    # =================================================
    # HELICITY MODE PART
    # =================================================
    elif mode == 'helicity_discrete':
        # DEFINE z-AXIS AS AXIS OF ROTATION AND RESOLUTION FOR POLAR ANGLE @ang
        axis, ang = [0., 0., 1.], 2. * np.pi / resolution
        rot_mat = rotation_matrix(axis, ang)
        # CREATE NEW LATTICE WITH INPLANE COMPONENTS ROTATED BY @ang
        mx_tmp, my_tmp, mz_tmp = rotate_spins(SL.mx, SL.my, SL.mz, rot_mat)
        # SINCE ROTATIONS ARE UNITARY PROJECTIONS, A FULL ROTATION BY 2pi CAN BE INTERPOLATED BY
        # MULTIPLYING THE RESULT BY @resolution
        geo_dist = geodasic_dist_data_orientated(SL.mx, SL.my, SL.mz, mx_tmp, my_tmp, mz_tmp)
        return resolution * geo_dist

    # =================================================
    # SEMI ANALYTICAL APPROACH TO HELICITY VOLUME
    # =================================================
    elif mode == 'helicity':
        dist = 0.
        for n in range(len(SL.mz)):
            dist += 1. - SL.mz[n] ** 2.
        return 2. * np.pi * np.sqrt(dist)


# =================================================
# FUNCTIONS FOR CALCULATING THE GEODASIC DISTANCE.
# INPUT CAN BE EITHER SPINLATTICE OBJECT OR ARRAYS
# CONTAINING SPINS FOR DATAORIENTATED APPROACH
# =================================================
def geodasic_dist_data_orientated(mx1, my1, mz1, mx2, my2, mz2):
    dist = 0.
    for n in range(len(mx1)):
        vec1 = np.array([mx1[n], my1[n], mz1[n]])
        vec2 = np.array([mx2[n], my2[n], mz2[n]])
        if vec2[0] == None:
            print('NoneType in vec2 at indices: ', n)
            exit()
        prod = np.dot(vec1, vec2)
        norm = np.linalg.norm(np.cross(vec1, vec2))
        if prod >= 1.0:
            continue
        else:
            dist += np.arctan2(norm, prod) ** 2
    return np.sqrt(dist)


def geodasic_dist(SL1, SL2):
    length = len(SL1.mx)
    dist = 0.
    for n in range(length):
        vec1 = np.array([SL1.mx[n], SL1.my[n], SL1.mz[n]])
        vec2 = np.array([SL2.mx[n], SL2.my[n], SL2.mz[n]])
        prod = np.dot(vec1, vec2)
        norm = np.linalg.norm(np.cross(vec1, vec2))
        if prod >= 1.0:
            continue
        else:
            dist += np.arctan2(norm, prod) ** 2
    return np.sqrt(dist)


# ================================================================
# family of functions to rotate or mirror spin orientations on the lattice
# ================================================================
# rodriguez rotation matrix for given angle
# ================================================================
def rotation_matrix(axis, angle):
    import scipy.linalg as sclin
    norm = np.linalg.norm(axis)
    if norm > 0:
        return sclin.expm(np.cross(np.eye(3), np.asarray(axis) / norm * angle))
    else:
        return sclin.expm(np.cross(np.eye(3), np.asarray([0.0, 0.0, 0.0])))


# ================================================================
# use householder transformation for mirroring vector at plane
# decribed by normal vector plane_normal
# ================================================================
def mirror_matrix(plane_normal):
    N = np.asarray(plane_normal) / np.linalg.norm(plane_normal)
    return np.identity(3) - 2.0 * np.outer(N, N)


# ================================================================
# rotatation matrix to rotate vec to axis
# ================================================================
def rotate_to_axis(axis, vec):
    N = np.cross(vec, axis)
    if np.linalg.norm(N) > 0:
        N = N / np.linalg.norm(N)
        prod = np.dot(np.asarray(axis) / np.linalg.norm(axis), np.asarray(vec) / np.linalg.norm(vec))
        if prod >= 1.0:
            ang = 0.0
        else:
            ang = np.arccos(prod)
    else:
        ang = 0.0
    return N, ang


# ================================================================
# rotates all vectors in given set using Mat
# ================================================================
def rotate_spins(mx, my, mz, Mat):
    mx_tmp = [None for _ in range(len(mx))]
    my_tmp = [None for _ in range(len(my))]
    mz_tmp = [None for _ in range(len(mz))]
    for n in range(len(mz)):
        mx_tmp[n], my_tmp[n], mz_tmp[n] = np.dot(Mat, np.asarray([mx[n], my[n], mz[n]]))
    return mx_tmp, my_tmp, mz_tmp


# ================================================================
# RETURNS THE RECIPROCE REPRESENTATION OF @SpinLattice ON BRAVAIS LATTICE
# ================================================================
def bravais_lattice(sp, key='hex'):
    def lattice_fft(self, sp):
        L = sp.size
        xfft = (np.fft.ifft2(np.asarray(sp.mx).reshape(L, L)).transpose()).reshape(sp.size ** 2)
        yfft = (np.fft.ifft2(np.asarray(sp.my).reshape(L, L)).transpose()).reshape(sp.size ** 2)
        zfft = (np.fft.ifft2(np.asarray(sp.mz).reshape(L, L)).transpose()).reshape(sp.size ** 2)
        return xfft, yfft, zfft

    def inverse_lattice_fft(self, fft_x, fft_y, fft_z):
        L = int(np.sqrt(len(fft_x)))
        x = (np.fft.fft2(np.asarray(fft_x).reshape(L, L)).transpose()).reshape(L ** 2)
        y = (np.fft.fft2(np.asarray(fft_y).reshape(L, L)).transpose()).reshape(L ** 2)
        z = (np.fft.fft2(np.asarray(fft_z).reshape(L, L)).transpose()).reshape(L ** 2)
        return x, y, z

    def reciproce_lattice(sp):
        latvec = np.asarray([[0.5, -0.86602540378, 0.0], [0.5, 0.86602540378, 0.0], [0.0, 0.0, 1.0]])
        spat = np.dot(latvec[0], np.cross(latvec[1], latvec[2]))
        recvec = np.asarray([np.cross(latvec[1], latvec[2]), np.cross(latvec[2], latvec[0]),
                             np.cross(latvec[0], latvec[1])]) * 2.0 * np.pi / spat
        recX, recY, recZ = [], [], []
        for n in range(sp.size):
            r0 = n * recvec[0] / np.linalg.norm(recvec[0]) / sp.size * 2
            for m in range(sp.size):
                r = r0 + m * recvec[1] / np.linalg.norm(recvec[1]) / sp.size * 2
                recX.append(r[0])
                recY.append(r[1])
                recZ.append(r[2])
        # resize recX, recY to the form of the brillouin zone
        recX = [(-1.0 + 2.0 * (x - min(recX)) / (max(recX) - min(recX))) for x in recX]
        recY = [np.cos(np.pi / 6.0) * 0.666 * (-1.0 + 2.0 * (y - min(recY)) / (max(recY) - min(recY))) for y in recY]
        return recX, recY, recZ

    # main call
    xfft, yfft, zfft = lattice_fft(sp)
    # get the reciproke coordinates
    recX, recY, recZ = reciproce_lattice(sp)
    return recX, recY, recZ, xfft, yfft, zfft


# ==============================================
# AFM FUNCTIONS

# ==============================================
# Function to get two sub lattices
# ==============================================
def get_AFM_sublattices(sl):
    X1, Y1, Z1, mx1, my1, mz1, magmom1 = [], [], [], [], [], [], []
    X2, Y2, Z2, mx2, my2, mz2, magmom2 = [], [], [], [], [], [], []
    # seperate every second spin and write it in to a sublattice
    for n in range(len(sl.X)):
        if (n % 2 + n // sl.size) % 2 == 0:
            X1.append(sl.X[n])
            Y1.append(sl.Y[n])
            Z1.append(sl.Z[n])
            mx1.append(sl.mx[n])
            my1.append(sl.my[n])
            mz1.append(sl.mz[n])
            magmom1.append(sl.magmom[n])
        else:
            X2.append(sl.X[n])
            Y2.append(sl.Y[n])
            Z2.append(sl.Z[n])
            mx2.append(sl.mx[n])
            my2.append(sl.my[n])
            mz2.append(sl.mz[n])
            mom2.append(sl.magmom[n])
    # make the sublattices a property of the object self
    SubSL1 = [X1, Y1, Z1, mx1, my1, mz1, magmom1]
    SubSL2 = [X2, Y2, Z2, mx2, my2, mz2, magmom2]
    return SubSL1, SubSL2
