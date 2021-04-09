import numpy as np
import sys
from python3.propertyfunctions import *



class MultiLayer():

    def __init__(self, size=None, key=None, number_layers=None, path=None):
        # CHECK THE INPUT GIVEN
        #if size == None :
        #    print('ERROR: enter kwarg @size=symmetric_xy_system_size_of_single_layer')
        #    exit()
        if number_layers == None:
            print('ERROR: enter kwarg @number_layers=total_number_of_layers')
            exit()
        # INITIALISE LAYERS
        self.Layer = [None for _ in range(number_layers)]
        self.number_layers = number_layers
        # HANDLE READING IN A STM FILE
        if path != None:
            # DO THE ACTUAL READING
            data = np.loadtxt(path, usecols = (0,1,2,3,4,5,6), unpack=False)
            # CHECK IF @number_layers MATCHES THE DATA GIVEN
            if len(data)%number_layers != 0 :
                print('Data given to @MultiLayer has not '+str(number_layers)+' layers, as stated')
                exit()
            size = int(np.sqrt(len(data)//number_layers))
            print('Read in '+str(number_layers)+' layers with size '+str(size))
            # PRESET SpinLattice OBJECTS
            for m in range(number_layers):
                # SpinLattices ARE ARBITRARILY INITIALISED WITH @key='hex'. SHOULD INTERFERE WITH ANYTHING
                self.Layer[m] = SpinLattice(size=size, key='hex', magmom=1.)
            for n in range(len(data)):
                index_layer = n%number_layers
                self.Layer[index_layer].X[n//2], self.Layer[index_layer].Y[n//2], self.Layer[index_layer].Z[n//2] = data[n][0], data[n][1], data[n][2]
                self.Layer[index_layer].mx[n//2], self.Layer[index_layer].my[n//2], self.Layer[index_layer].mz[n//2] = data[n][3], data[n][4], data[n][5]
                self.Layer[index_layer].magmom[n//2] = data[n][6]
            print('Finished setting up @Multilayer object from file '+path)


    #==================================================
    # ADDS A LAYER TO THE @MultiLayer CLASS
    # INPUT: -@SL: @SpinLattice OBJECT RESEMBLIMG THE LAYER TO ADD
    #        -@index_layer: INDEX IN THE ARRAY OF LAYERS
    #        -@zpos_uc: z-POSITION OF THE UNITCELL CONTAINING THE LAYER
    #==================================================
    def add_layer(self, SL, index_layer=0, zpos_uc=0.):
        self.Layer[index_layer] = SL
        self.size = SL.size
        # SET z-POSITION TO z-POSITION OF THE CORRESPONDING UNITCELL
        self.Layer[index_layer].Z = [zpos_uc for n in range(self.Layer[index_layer].size**2)]


    def write_STM(self, name='SpinSTMi.dat'):
        with open(name, 'w') as file :
            for n in range(len(self.Layer[0].X)):
                for m in range(self.number_layers):
                    file.write('%.8f' %self.Layer[m].X[n] + '\t'
                            + '%.8f' %self.Layer[m].Y[n] +  '\t'
                            + '%.8f' %self.Layer[m].Z[n] +  '\t'
                            + '%.8f' %self.Layer[m].mx[n] + '\t'
                            + '%.8f' %self.Layer[m].my[n] + '\t'
                            + '%.8f' %self.Layer[m].mz[n] + '\t'
                            + '%.8f' %self.Layer[m].magmom[n] + '\n')





#==================================================
# class of a general spin lattice.
# this is the core class that contains all necessary instances of the lattice itself.
#==================================================
class SpinLattice():
    def __init__(self, size=None, key=None, path=None, magmom=None, uplo=1., AFM=False, a1_0=None, a2_0=None):
        if size and key and magmom:
            self.setDefault(size, key, magmom, uplo, AFM, a1_0, a2_0)
        elif isinstance(path, str) :
            try:
                self.setSTM(path)
            except:
                print('No SpinSTM found at location:'+ path)
                sys.exit()
        else:
            print('Input Error: make shure you choose one of following:\n 1) size=.., key=.., magmom=..\n 2) path=..')
            sys.exit()

    #==============================================
    # initial configuration of FM state
    #==============================================
    def setDefault(self, size, key, magmom, uplo, AFM, a1_0, a2_0):
        self.size = size
        lat = Lattices(key, size, a1_0, a2_0)
        self.X, self.Y, self.Z = lat.X, lat.Y, lat.Z
        self.mx = [0. for n in range(len(self.X))]
        self.my = [0. for n in range(len(self.X))]
        # if @AFM is true, build initial lattice with alternating z-component
        if AFM and key=='quad' :
            self.mz = [uplo*(-1)**(n%2 + n//size) for n in range(len(self.X))]
        elif AFM and key=='hex' :
            print('Input Error: AFM not possible on hexagonal lattice')
            sys.exit()
        # if no @AFM, build usual FM lattice
        else:
            self.mz = [uplo for n in range(len(self.X))]
        self.magmom = [magmom for n in range(len(self.X))]
    #==============================================
    # takes the spin configuration from STM file as initial one
    #==============================================
    def setSTM(self, STMpath):
        data = np.loadtxt(STMpath, usecols = (0,1,2,3,4,5,6), unpack=True)
        self.X, self.Y, self.Z = data[0], data[1], data[2]
        self.mx, self.my, self.mz = data[3], data[4], data[5]
        self.size = int(np.sqrt(len(self.X)))
        self.magmom = data[6]


    #============================================
    # write spin configuration
    # default name is 'SpinSTMi.dat'
    #============================================
    def write_STM(self, name='SpinSTMi.dat'):
        with open(name, 'w') as file :
            for n in range(len(self.X)):
                file.write('%.8f' %self.X[n] + '\t'
                        + '%.8f' %self.Y[n] +  '\t'
                        + '%.8f' %self.Z[n] +  '\t'
                        + '%.8f' %self.mx[n] + '\t'
                        + '%.8f' %self.my[n] + '\t'
                        + '%.8f' %self.mz[n] + '\t'
                        + '%.8f' %self.magmom[n] + '\n')

    #==============================================
    # method to add a skyrmion to the box
    #==============================================
    def addSkyrmion(self, ursprung, vorticity, helicity, c, w, AFM=False, uplo=1, elongation=False, angl_elongation=0., ab_elongation=[1.,1.]):
        mag = Magnetisation_Skyrmion(self.X, self.Y, ursprung, vorticity, helicity, c, w, AFM, uplo, elongation, angl_elongation, ab_elongation)
        for m in range(len(mag.mz)):
            if (uplo==1 and mag.mz[m] < (1.0-5*10**(-4))) or (uplo==-1 and mag.mz[m] > -(1.0-5*10**(-4))):
                self.mx[m] = mag.mx[m]
                self.my[m] = mag.my[m]
                self.mz[m] = mag.mz[m]

    #==============================================
    # method to add a skyrmion to the box
    #==============================================
    def add_chimera(self, ursprung, vorticity, helicity, c, w, AFM=False, uplo=1, sym_chimera=True, angl_chimera=0., elongation=False, angl_elongation=0., ab_elongation=[1.,1.]):
        mag = Magnetisation_Chimera(self.X, self.Y, ursprung, vorticity, helicity, c, w, AFM, uplo, sym_chimera, angl_chimera, elongation, angl_elongation, ab_elongation)
        for m in range(len(mag.mz)):
            if (uplo==1 and mag.mz[m] < (1.0-5*10**(-4))) or (uplo==-1 and mag.mz[m] > -(1.0-5*10**(-4))):
                self.mx[m] = mag.mx[m]
                self.my[m] = mag.my[m]
                self.mz[m] = mag.mz[m]

    #==============================================
    # method to add a meron to the box
    #==============================================
    def add_meron(self, ursprung, vorticity, helicity, c, w, AFM=False, uplo=1):
        mag = Magnetisation_Meron(self.X, self.Y, ursprung, vorticity, helicity, c, w, AFM, uplo)
        for m in range(len(mag.mz)):
            if (uplo==1 and mag.mz[m] < 0.51) or (uplo==-1 and mag.mz[m] > -0.51):
                self.mx[m] = mag.mx[m]
                self.my[m] = mag.my[m]
                self.mz[m] = mag.mz[m]

    #==============================================
    # method to add a bimeron to the box
    #==============================================
    def add_bimeron(self, pos0, R, a1, a2):
        mag = Magnetisation_Bimeron(self.X, self.Y, pos0, R, a1, a2)
        for m in range(len(mag.mz)):
            self.mx[m] = mag.mx[m]
            self.my[m] = mag.my[m]
            self.mz[m] = mag.mz[m]

    #==============================================
    # method to add a skyrmion to the box
    #==============================================
    def addSkyrmionlattice(self, k, vorticity, helicity, c, w, AFM=False, uplo=1, onside=True):
        index_dist = self.size//k
        if onside :
            delta_X = 0.0
            delta_Y = 0.0
        else :
            delta_X = self.X[1]
            delta_Y = self.Y[1]/2.
        # Iterate through all lattice sides (+1 for treating periodic boundaries)
        for n in range(self.size+1):
            for m in range(self.size+1):
                # If lattice side matches periodic kriteria, decide, if periodic
                # boundary conditions apply or not and set the proper position for
                # the skyrmion center
                if n%index_dist == 0 and m%index_dist == 0 :
                    if n >= self.size and m >= self.size :
                        skyrmion_index = (n-1)*self.size + m -1
                        pos = [self.X[skyrmion_index] + self.X[self.size] + self.X[1] + delta_X, self.Y[skyrmion_index]+ self.Y[self.size]+ self.Y[1]+ delta_Y]
                    elif n >= self.size :
                        skyrmion_index = (n-1)*self.size +m
                        pos = [self.X[skyrmion_index] + self.X[self.size] + delta_X, self.Y[skyrmion_index]+ self.Y[self.size]+ delta_Y]
                    elif m >= self.size :
                        skyrmion_index = n*self.size + m -1
                        pos = [self.X[skyrmion_index] + self.X[1] + delta_X, self.Y[skyrmion_index]+ self.Y[1]+ delta_Y]
                    # this is the case, when no periodic boundary conditions have to be considered
                    else :
                        skyrmion_index = n*self.size + m
                        pos = [self.X[skyrmion_index] +delta_X, self.Y[skyrmion_index]+ delta_Y]
                    # PLACE SKYRMION
                    self.addSkyrmion(pos, vorticity, helicity, c, w, AFM=AFM, uplo=uplo)

    #==============================================
    # method to create a 3q state for the whole box
    #==============================================
    def add3qstate(self, init=None):
        mag = Magnetisation_3qstate(self.X, self.Y, init)
        self.mx = mag.mx
        self.my = mag.my
        self.mz = mag.mz
    #==============================================
    # method to create a 1q state for the whole box
    #==============================================
    def add1qstate(self, Rq, Iq, Q, phase=0.0):
        mag = Magnetisation_1qstate(self.X, self.Y, self.Z, Rq, Iq, Q, phase)
        self.Q, self.Rq, self.Iq = mag.Q, mag.Rq, mag.Iq
        self.mx = mag.mx
        self.my = mag.my
        self.mz = mag.mz

    #==============================================
    # method to create a 1q state for the whole box
    #==============================================
    def add_superposition(self, sl1, sl2):
        mag = Magnetisation_superposition(self.X, self.Y, self.Z, sl1, sl2)
        self.mx = mag.mx
        self.my = mag.my
        self.mz = mag.mz
    #==============================================
    # method to add a domainwall to the box
    #==============================================
    def addDomainwall(self, r0, direction, width, heli=np.pi):
        mag = Magnetisation_Domainwall(self.X, self.Y, r0, direction, width, heli)
        self.r0 = r0
        self.direction = np.asarray(direction)/np.linalg.norm(direction)
        self.dw_width = width
        for m in range(len(mag.mz)):
            if mag.mz[m] < (1.0-10**(-2)):
                self.mx[m] = mag.mx[m]
                self.my[m] = mag.my[m]
                self.mz[m] = mag.mz[m]

    #==============================================
    # method to add the row wise antiferromagnet to the whole box
    #==============================================
    def addRWAFM(self, init='inplaneX'):
        mag = Magnetisation_RWAFM(self.X, self.Y, init)
        self.mx = mag.mx
        self.my = mag.my
        self.mz = mag.mz

    #==============================================
    # method to return the topological charge of the lattice
    #==============================================
    def getTopocharge(self):
        mag = [self.mx, self.my, self.mz]
        self.topo_charge = topocharge(mag)
    #==============================================
    # method to return the radius of an isolated skyrmion.
    # if the lattice inhabitats more than one skyrmion or
    # something else, an exception will be raised
    #==============================================
    def getSkradius(self):
        self.sk_radius, self.sk_popt, self.sk_pcov = skyrmionradius(self)
    #==============================================
    # method for finding the width of a domainwall
    #==============================================
    def getDWwidth(self):
        self.r0, self.phi, self.dw_width = dwwidth(self)
        self.direction = np.asarray([np.cos(self.phi), np.sin(self.phi)])






#===============================================================
# class for the construction of the lattice in such a way, that
# the result can be used in the Spindynamics code
# quad or hex can be chosen
#===============================================================
class Lattices():
    def __init__(self, key, size, a1_0=None, a2_0=None):
        if key == 'quad':
            self.X, self.Y, self.Z = self.build_quadratic_lattice(size, a1_0, a2_0)
        elif key == 'hex':
            self.X, self.Y, self.Z = self.build_hexagonal_lattice(size, a1_0, a2_0)
    #==============================================
    # method returns lists @X, @Y, @Z so, that (X[n], Y[n], Z[n])
    # is a point on the hexagonal lattice
    # The kwargs a1_0 and a2_0 define the zero point of the lattice in units of
    # the right handed lattice vectors. These are only important for Multilayers
    #==============================================
    def build_hexagonal_lattice(self, size, a1_0=None, a2_0=None):
        c1 = 0.5
        c2 = -round(np.sqrt(3.0/4.0),8)
        if a1_0 and a2_0:
            x0 = 0.0 + c1 * (a1_0 + a2_0)
            y0 = 0.0  + c2 * (a2_0 - a1_0)
        else:
            x0, y0 = 0.0, 0.0
        X, Y, Z = [], [], []
        for n in range(size):
            for m in range(size):
                X.append(x0 + m*c1)
                Y.append(y0 - m*c2)
                Z.append(0)
            x0 += c1
            y0 += c2
        return X,Y,Z
    #==============================================
    # method returns lists @X, @Y, @Z so, that (X[n], Y[n], Z[n])
    # is a point on the quadratic lattice
    # The kwargs a1_0 and a2_0 define the zero point of the lattice in units of
    # the right handed lattice vectors. These are only important for Multilayers
    #==============================================
    def build_quadratic_lattice(self, size, a1_0=None, a2_0=None):
        if a1_0 and a2_0:
            x0 = 0.0 + a1_0
            y0 = 0.0 + a2_0
        else:
            x0, y0 = 0.0, 0.0
        x = np.linspace(0, size-1, size)
        y = np.linspace(0, size-1, size)
        X, Y, Z = [], [], []
        for n in x:
            for m in y:
                 X.append(n + x0)
                 Y.append(m + y0)
                 Z.append(0)
        return X,Y,Z




#==============================================================
# takes parameters and arrays X,Y and returns diskret magnetisation
# for skyrmions with corresponding structure
#===============================================================
class Magnetisation_Skyrmion():
    def __init__(self, X, Y, pos0, m, g, c, w, AFM, uplo, elongation, angl_elongation, ab_elongation):
        self.mx, self.my, self.mz = self.build_skyrmion(X, Y, pos0, m, g, c, w, uplo, AFM, elongation, angl_elongation, ab_elongation)

    #==========================================================
    # functions for the polar and azimutal angle of an skyrmion.
    # theta is the standard bogdanov profile
    #==========================================================
    def theta(self, r,c,w):
        comp1 = np.arcsin(np.tanh((-r -c)*2/w))
        comp2 = np.arcsin(np.tanh((-r +c)*2/w))
        return np.pi + comp1 + comp2

    def phi(self, p, m, g):
        return  m*p + g
    #==========================================================
    # here the magnetisation of the skyrmion is build with
    # respect to the profile parameters, helicity and vorticity
    #==========================================================
    def build_skyrmion(self, X, Y, pos0, m, g, c, w, uplo, AFM, elongation, angl_elongation, ab_elongation):
        assert len(X) == len(Y)
        mx, my, mz = [], [], []
        for n in range(len(X)):
            x, y = X[n]-pos0[0], Y[n]-pos0[1]
            r, p = np.sqrt(x**2 + y**2), np.arctan2(y,x)
            # HANDLE ELONGATION OF SKYRMION IF CHOSEN. USE ELLIPTIC PARAMETERISATION FOR RADIAL DISTANCE @r
            if elongation :
                #r = r/(1+exz*abs(np.cos(p-angl_elongation)))
                r = r*(2.-np.sqrt((ab_elongation[0]*np.cos(p-angl_elongation))**2 + (ab_elongation[1]*np.sin(p-angl_elongation))**2))

            # SET AZIMUTHAL ANGLE FOR RADIAL THETA PROFILE
            th = self.theta(r,c,w)
            ph = self.phi(p, m, g)
            # alternate sign of spin if @AFM is True
            if AFM :
                sign = (-1)**(n%2 + n//int(np.sqrt(len(X))))
            else :
                sign = 1
            # actually setting of vector components resembling spin
            mx.append(sign*np.sin(th)*np.cos(ph))
            my.append(sign*np.sin(th)*np.sin(ph))
            mz.append(sign*np.cos(th)*float(uplo))
        return mx, my, mz


#==============================================================
# takes parameters and arrays X,Y and returns diskret magnetisation
# for skyrmions with corresponding structure
#===============================================================
class Magnetisation_Chimera():
    def __init__(self, X, Y, pos0, m, g, c, w, AFM, uplo, sym_chimera, angl_chimera, elongation, angl_elongation, ab_elongation):
        self.mx, self.my, self.mz = self.build_chimera(X, Y, pos0, m, g, c, w, uplo, AFM, sym_chimera, angl_chimera, elongation, angl_elongation, ab_elongation)

    #==========================================================
    # functions for the polar and azimutal angle of an skyrmion.
    # theta is the standard bogdanov profile
    #==========================================================
    def theta(self, r,c,w):
        comp1 = np.arcsin(np.tanh((-r -c)*2/w))
        comp2 = np.arcsin(np.tanh((-r +c)*2/w))
        return np.pi + comp1 + comp2

    def phi(self, p, m, g):
        return  m*p + g
    #==========================================================
    # here the magnetisation of the skyrmion is build with
    # respect to the profile parameters, helicity and vorticity
    #==========================================================
    def build_chimera(self, X, Y, pos0, m, g, c, w, uplo, AFM, sym_chimera, angl_chimera, elongation, angl_elongation, ab_elongation):
        assert len(X) == len(Y)
        mx, my, mz = [], [], []
        for n in range(len(X)):
            x, y = X[n]-pos0[0], Y[n]-pos0[1]
            r, p = np.sqrt(x**2 + y**2), np.arctan2(y,x)
            # HANDLE ELONGATION OF SKYRMION IF CHOSEN. USE ELLIPTIC PARAMETERISATION FOR RADIAL DISTANCE @r
            if elongation :
                #r = r/(1+exz*abs(np.cos(p-angl_elongation)))
                r = r*(2.-np.sqrt((ab_elongation[0]*np.cos(p-angl_elongation))**2 + (ab_elongation[1]*np.sin(p-angl_elongation))**2))

            # SET AZIMUTHAL ANGLE FOR RADIAL THETA PROFILE
            th = self.theta(r,c,w)
            # chimera case: change vorticity if @p switches half planes
            # the idea is to map @p to @p_tmp, which is 0<p_tmp<pi/2 for every spin, whos vorticity has to be switched
            # EDIT: IF WE WANT TO HAVE SYMMETRIC CHIMERA STATES, WE HAVE TO DEVIDE NOT ONLY INTO HALF PLANES
            #       INSTEAD WE HAVE TO HAVE INTERVALS OF pi/m , WITH VORTICITY @m
            if sym_chimera :
                plane_devider = m
            else :
                plane_devider = 1
            # MAP POLAR ANGLE TO EASIER TO HANDLE INTERVALL
            p_tmp = p + np.pi/2. -angl_chimera
            #p_tmp = p -angl_chimera
            # SINCE p=arctan(x,y) IS IN [-pi, +pi], SUBTRACTING @angl_chimera CAN VIOLATE THESE BOUNDARIES --> HANDLE THIS BY MAPPING BACK
            if p_tmp < -np.pi :
                p_tmp += 2.*np.pi
            # DECIDE; WHICH VORTICITY TO TAKE, DEPENDING ON INTERVALL WE ARE IN RIGHT NOW
            if (p_tmp > 0) and (p_tmp < np.pi/plane_devider) :
                ph = self.phi(p, -m, g + np.pi + 2*angl_chimera)
            else :
                ph = self.phi(p, m, g)

            # alternate sign of spin if @AFM is True
            if AFM :
                sign = (-1)**(n%2 + n//int(np.sqrt(len(X))))
            else :
                sign = 1
            # actually setting of vector components resembling spin
            mx.append(sign*np.sin(th)*np.cos(ph))
            my.append(sign*np.sin(th)*np.sin(ph))
            mz.append(sign*np.cos(th)*float(uplo))
        return mx, my, mz


#==============================================================
# takes parameters and arrays X,Y and returns diskret magnetisation
# for skyrmions with corresponding structure
#===============================================================
class Magnetisation_Meron():
    def __init__(self, X, Y, pos0, m, g, c, w, AFM, uplo):
        self.mx, self.my, self.mz = self.build_meron(X, Y, pos0, m, g, c, w, uplo)
    #==========================================================
    # functions for the polar and azimutal angle of an skyrmion.
    # theta is the standard bogdanov profile
    #==========================================================
    def theta(self, r,c,w):
        comp1 = np.arcsin(np.tanh((-r -c)*2/w))
        comp2 = np.arcsin(np.tanh((-r +c)*2/w))
        return np.pi + comp1/2. + comp2/2.

    def phi(self, p, m, g):
        return  m*p + g
    #==========================================================
    # here the magnetisation of the skyrmion is build with
    # respect to the profile parameters, helicity and vorticity
    #==========================================================
    def build_meron(self, X, Y, pos0, m, g, c, w, uplo):
        assert len(X) == len(Y)
        mx, my, mz = [], [], []
        for n in range(len(X)):
            x, y = X[n]-pos0[0], Y[n]-pos0[1]
            r, p = np.sqrt(x**2 + y**2), np.arctan2(y,x)
            th = self.theta(r,c,w)
            ph = self.phi(p,m,g)
            mx.append(np.sin(th)*np.cos(ph))
            my.append(np.sin(th)*np.sin(ph))
            mz.append(np.cos(th)*float(uplo))
        return mx, my, mz

#============================================================
# takes the position arrays X, Y, and the Bimeron parameters a1, a2, R
# R --> distance between the Meron centers
# a1, a2 --> paramteters with determine if the Bimeron is roud or elliptical
# a1 = a2 --> round Bimeron
# pos0 --> zero point as array
#============================================================
class Magnetisation_Bimeron():
    def __init__(self, X, Y, pos0, R, a1, a2):
        self.mx, self.my, self.mz = self.build_bimeron(X, Y, pos0, R, a1, a2)

    #===============================================
    #magnetisation direction in spherical coordinates
    #===============================================
    def theta(self, R, c_i, c_j, a1, a2):
        rho = np.sqrt(a1*c_i**2 + a2*c_j**2)
        return np.arccos(R * c_i / (rho**2 + (R**2)/4 ))

    def phi(self, R, c_i, c_j):
        return np.arctan((c_i - R/2)/(c_j)) - np.arctan((c_i + R/2)/(c_j))

    def build_bimeron(self, X, Y, pos0, R, a1, a2):
        r = 1
        assert len(X) == len(Y)
        mx, my, mz = np.zeros(len(X)), np.zeros(len(X)), np.zeros(len(X))
        for n in range(len(X)):
            theta_c = self.theta(R, X[n]-pos0[0], Y[n]-pos0[1], a1, a2)
            phi_c   = self.phi(R, X[n]-pos0[0], Y[n]-pos0[1])
            mx[n] = np.round(r*np.sin(theta_c)*np.cos(phi_c),8)
            my[n] = np.round(r*np.sin(theta_c)*np.sin(phi_c),8)
            mz[n] = np.round(r*np.cos(theta_c),8)
        return mx, my, mz


#==================================================
# class for magnetisation identified with the
# 1q-state also known as simple spin spiral
#==================================================
class Magnetisation_1qstate():

    def __init__(self, X, Y, Z, Rq, Iq, Q, phase):
        # reshape Rq, Iq, Q with respect to lattice vectors
        latvec = np.asarray([ [0.5, -0.86602540378, 0.0],
                            [0.5, 0.86602540378, 0.0],
                            [0.0, 0.0, 1.0] ]).astype('float')
        spat = np.dot(latvec[0], np.cross(latvec[1], latvec[2]))
        Q = ( Q[0]*np.cross(latvec[1], latvec[2])
            + Q[1]*np.cross(latvec[2], latvec[0])
            + Q[2]*np.cross(latvec[0], latvec[1]) )*2.0*np.pi/spat
        self.Q = Q
        Rq = Rq[0]*latvec[0] + Rq[1]*latvec[1] + Rq[2]*latvec[2]
        self.Rq = Rq/np.linalg.norm(Rq)
        Iq = Iq[0]*latvec[0] + Iq[1]*latvec[1] + Iq[2]*latvec[2]
        self.Iq = Iq/np.linalg.norm(Iq)
        # calculate magnetisation
        self.mx, self.my, self.mz = self.build_1qstate(X, Y, Z,
                                                       self.Rq, self.Iq, self.Q, phase)

    def build_1qstate(self, X, Y, Z, Rq, Iq, Q, phase):
        mx, my, mz = [], [], []
        for n in range(len(X)):
            R = np.asarray([X[n], Y[n], Z[n]]).astype('float')
            dot = np.dot(R, Q) + phase
            mx.append(Rq[0]*np.cos(dot) - Iq[0]*np.sin(dot))
            my.append(Rq[1]*np.cos(dot) - Iq[1]*np.sin(dot))
            mz.append(Rq[2]*np.cos(dot) - Iq[2]*np.sin(dot))
        return mx,my,mz


#==================================================
# class for magnetisation identified with the
# 3q-state, definitions from Dissertation Phillip Kurz S.111
#==================================================
class Magnetisation_3qstate():
    def __init__(self, X, Y, init):
        self.mx, self.my, self.mz = self.build_3qstate(X, Y)
        if init == 'ori3':
            self.mx, self.my, self.mz = self.align_ori3(self.mx, self.my, self.mz)
        elif init == 'ori2':
            self.mx, self.my, self.mz = self.align_ori2(self.mx, self.my, self.mz)
        elif init == 'ori1':
            self.mx, self.my, self.mz = self.align_ori1(self.mx, self.my, self.mz)
    #==================================================
    # Input: arrays X, Y, so that (X[i], Y[i]) is a point on
    # the lattice
    # Note: A,B,C can be chosen to generate other multi-q-states
    #==================================================
    def build_3qstate(self, X, Y):
        q1 = 2.0*np.pi*np.asarray([0, 1.0/np.sqrt(3)])
        q2 = 2.0*np.pi*np.asarray([0.5, 1.0/np.sqrt(3)/2])
        q3 = 2.0*np.pi*np.asarray([0.5, -1.0/np.sqrt(3)/2])
        A = 1.0/np.sqrt(3)
        B = 1.0/np.sqrt(3)
        C = 1.0/np.sqrt(3)
        mx, my, mz = [], [], []
        for n in range(len(X)):
            R = np.asarray([X[n], Y[n]])
            mx.append(A*np.cos(np.dot(q1,R)))
            my.append(B*np.cos(np.dot(q2,R)))
            mz.append(C*np.cos(np.dot(q3,R)))
        return mx,my,mz
    #==================================================
    # turns the magnetisation of the initial PK state into
    # highly symmetrical ori3
    #==================================================
    def align_ori3(self, mx, my, mz):
        # 1) rotate spins, so that Spin 0 is aligned with z-axis
        axis1, ang1 = rotate_to_axis([0.0, 0.0, 1.0], [mx[0], my[0], mz[0]])
        mat1 = rotation_matrix(axis1, ang1)
        mx, my, mz = rotate_spins(mx, my, mz, mat1)
        # 2) rotate Spins, so that Spin 1 points along (1/2 +isqrt(3)/2)
        axis2, ang2 = rotate_to_axis([0.5, np.sqrt(3.0)/2.0, 0.0], [mx[1], my[1], 0.0])
        mat2 = rotation_matrix(axis2, ang2)
        mx,my,mz = rotate_spins(mx,my,mz, mat2)
        return mx, my, mz

    def align_ori2(self, mx, my, mz):
        # start with a ori3 configuration
        mx, my, mz = self.align_ori3(mx, my, mz)
        # now rotate by \tau/2 around y-axis
        rotmat = rotation_matrix([0.0, 1.0, 0.0], np.arccos(-1.0/3.0)/2.0)
        mx,my,mz = rotate_spins(mx,my,mz, rotmat)
        return mx, my, mz

    def align_ori1(self, mx, my, mz):
        # start with a ori3 configuration
        mx, my, mz = self.align_ori2(mx, my, mz)
        # now rotate by \tau/2 around y-axis
        rotmat = rotation_matrix([0.0, 1.0, 0.0], -np.pi/2.0)
        mx,my,mz = rotate_spins(mx,my,mz, rotmat)
        return mx, my, mz



#==================================================
# class for magnetisation identified with the
# 1q-state also known as simple spin spiral
#==================================================
class Magnetisation_superposition():

    def __init__(self, X, Y, Z, sl1, sl2):
        self.mx, self.my, self.mz = self.build_superposition(X, Y, Z, sl1, sl2)

    def lattice_fft(self, sp):
        L = sp.size
        xfft = (np.fft.ifft2(np.asarray(sp.mx).reshape(L, L)).transpose()).reshape(sp.size**2)
        yfft = (np.fft.ifft2(np.asarray(sp.my).reshape(L, L)).transpose()).reshape(sp.size**2)
        zfft = (np.fft.ifft2(np.asarray(sp.mz).reshape(L, L)).transpose()).reshape(sp.size**2)
        return xfft, yfft, zfft

    def inverse_lattice_fft(self, fft_x, fft_y, fft_z):
        L = int(np.sqrt(len(fft_x)))
        x = (np.fft.fft2(np.asarray(fft_x).reshape(L, L)).transpose()).reshape(L**2)
        y = (np.fft.fft2(np.asarray(fft_y).reshape(L, L)).transpose()).reshape(L**2)
        z = (np.fft.fft2(np.asarray(fft_z).reshape(L, L)).transpose()).reshape(L**2)
        return x, y, z

    def normalise_inverse_fft(self, x,y,z):
        for n in range(len(x)):
            norm = np.sqrt(x[n]**2 + y[n]**2 + z[n]**2)
            x[n] = x[n]/norm
            y[n] = y[n]/norm
            z[n] = z[n]/norm
        return x,y,z

    def build_superposition(self, X, Y, Z, sl1, sl2):
        mx, my, mz = [], [], []
        # calculate fourier representation
        sl1_x, sl1_y, sl1_z = self.lattice_fft(sl1)
        sl2_x, sl2_y, sl2_z = self.lattice_fft(sl2)
        # build superposition of waves
        sl_x = (sl1_x + sl2_x)*np.sqrt(2.)
        sl_y = (sl1_y + sl2_y)*np.sqrt(2.)
        sl_z = (sl1_z + sl2_z)*np.sqrt(2.)
        # transform back to real space image
        mx, my, mz = self.inverse_lattice_fft(sl_x, sl_y, sl_z)
        mx, my, mz = self.normalise_inverse_fft(mx.real, my.real, mz.real)
        return mx, my, mz



#==================================================
# class for magnetisation identified with the
# 3q-state, definitions from Dissertation Phillip Kurz S.111
#==================================================
class Magnetisation_RWAFM():
    def __init__(self, X, Y, init):
        self.mx, self.my, self.mz = self.build_3qstate(X, Y, init)
    #==================================================
    # Input: arrays X, Y, so that (X[i], Y[i]) is a point on
    # the lattice
    # Note: A,B,C can be chosen to generate other multi-q-states
    #==================================================
    def build_3qstate(self, X, Y, init):
        if init == 'outofplane':
            A, B, C = 0, 0, 1
        elif init == 'inplaneY':
            A, B, C = 0, 1, 0
        elif init == 'inplaneX':
            A, B, C = -1, 0, 0
        q1 = 2.0*np.pi*np.asarray([0, 1.0/np.sqrt(3)])
        q2 = 2.0*np.pi*np.asarray([0.5, 1.0/np.sqrt(3)/2])
        q3 = 2.0*np.pi*np.asarray([0.5, -1.0/np.sqrt(3)/2])
        mx, my, mz = [], [], []
        for n in range(len(X)):
            R = np.asarray([X[n], Y[n]])
            mx.append(A*np.cos(np.dot(q1,R)))
            my.append(B*np.cos(np.dot(q2,R)))
            mz.append(C*np.cos(np.dot(q3,R)))
        return mx,my,mz


#==============================================================
# takes parameters and arrays X,Y and returns diskret magnetisation
# for skyrmions with corresponding structure
#===============================================================
class Magnetisation_Domainwall():
    def __init__(self, X, Y, r0, direction, width, heli):
        self.mx, self.my, self.mz = self.build_domainwall(X, Y, r0, direction, width, heli)

    def build_domainwall(self, X, Y, r0, direction, width, heli):
        mx, my, mz = [], [], []
        direction = np.asarray(direction)/np.linalg.norm(direction)
        R0 = np.absolute(direction)*r0
        # construct axis for rotation:
        axismat = rotation_matrix([0.0, 0.0, 1.0], heli)
        axis = rotate_spins([direction[0]], [direction[1]], [0.0], axismat)
        axis = np.asarray([axis[0][0], axis[1][0], axis[2][0]])
        # rotate every spin with own matrix according to @theta and @axis
        # the angle theta is given by the DW profile
        for n in range(len(X)):
            r = np.asarray([X[n], Y[n]])
            arg = np.dot(r-R0, direction)/width
            theta = 2.0*np.arctan(np.exp(arg))
            mat = rotation_matrix(axis, theta)
            mag = rotate_spins([0.0] ,[0.0], [1.0], mat)
            mx.append(mag[0][0])
            my.append(mag[1][0])
            mz.append(mag[2][0])
        return mx, my, mz




#==========================================
# LEVEL +1 ROUTINES
# (TAKE @SpinLattice and also return @SpinLattice)
#==========================================

#==============================================
# method for deviding AFM-Lattice in two sublattices
#==============================================
def afm_sublattices(sl):
    X1,Y1,Z1,mx1,my1,mz1,magmom1 = [],[],[],[],[],[],[]
    X2,Y2,Z2,mx2,my2,mz2,magmom2 = [],[],[],[],[],[],[]
    #seperate every second spin and write it in to a sublattice
    for n in range(len(sl.X)):
        if (n%2 + n//sl.size)%2 == 0:
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
            magmom2.append(sl.magmom[n])
    # make them seperate @SpinLattice objects
    sl1 = SpinLattice(size=int(np.sqrt(len(X1))), key='quad', magmom=1.)
    sl2 = SpinLattice(size=int(np.sqrt(len(X2))), key='quad', magmom=1.)
    sl1.X, sl1.Y, sl1.Z = X1, Y1, Z1
    sl1.mx, sl1.my, sl1.mz, sl1.magmom = mx1, my1, mz1, magmom1
    sl2.X, sl2.Y, sl2.Z = X2, Y2, Z2
    sl2.mx, sl2.my, sl2.mz, sl2.magmom = mx2, my2, mz2, magmom2

    return sl1, sl2
