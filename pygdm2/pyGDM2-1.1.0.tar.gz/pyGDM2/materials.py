# encoding: utf-8
#
#Copyright (C) 2017-2021, P. R. Wiecha
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Collection of dielectric functions and tools to load tabulated data
"""

from __future__ import print_function
from __future__ import absolute_import

import numpy as np

#==============================================================================
# Internal definitions
#==============================================================================
class _interp1dPicklable:
    """wrapper for pickleable version of `scipy.interpolate.interp1d`
    
    **Note:** there might be still pickle-problems with certain c / fortran 
    wrapped libraries
    
    From: http://stackoverflow.com/questions/32883491/pickling-scipy-interp1d-spline
    """
    def __init__(self, xi, yi, **kwargs):
        from scipy.interpolate import interp1d
        self.xi = xi
        self.yi = yi
        self.args = kwargs
        self.f = interp1d(xi, yi, **kwargs)

    def __call__(self, xnew):
        return self.f(xnew)

    def __getstate__(self):
        return self.xi, self.yi, self.args

    def __setstate__(self, state):
        from scipy.interpolate import interp1d
        self.f = interp1d(state[0], state[1], **state[2])




#==============================================================================
# General purpose
#==============================================================================
class dummy(object):
    """constant index
    
    Material with spectrally constant refractive index
    
    Parameters
    ----------
    n : complex, default: (2.0 + 0.0j)
        complex refractive index of constant material (returned dielectric 
        function will be n**2)
        
    """
    
    def __init__(self, n=(2.0 + 0.0j)):
        """Define constant material"""
        self.n = complex(n)
        self.__name__ = 'constant index material, n={}'.format(np.round(self.n, 3))
    
    def epsilon(self, wavelength):
        """Dummy material: Constant dielectric function
    
        constant dielectric function material
        
        Parameters
        ----------
        wavelength : real
            wavelength at which to evaluate dielectric function (in nm)
        
        """
        eps = complex(self.n**2)
        return eps


class fromFile(object):
    """tabulated dispersion
    
    Use tabulated data provided from textfile for the complex material 
    refractive index
    
    Parameters
    ----------
    refindex_file : str
        path to text-file with the tabulated refractive index 
        (3 whitespace separated columns: #1 wavelength, #2 real(n), #3 imag(n))
        
        Data can be obtained e.g. from https://refractiveindex.info/ 
        using the *"Full database record"* export function.
    
    unit_wl : str, default: 'micron'
        Units of the wavelength in file, one of ['micron', 'nm']
    
    interpolate_order : int, default: 1
        interpolation order for data (1: linear, 2: square, 3: cubic)
        "1" uses `numpy.interp`, "2" and "3" require `scipy` 
        (using `scipy.interpolate.interp1d`)
    
    name : str, default: None
        optional name attribute for material class. By default use filename.
    
    """
    
    def __init__(self, refindex_file, unit_wl='micron', interpolate_order=1, name=None):
        """Use tabulated dispersion"""
        wl, n, k = np.loadtxt(refindex_file).T
        
        if unit_wl.lower() in ['micron', 'microns', 'um']:
            factor_wl = 1.0E3  # micron --> nm
        elif unit_wl.lower() in ['nanometer', 'nm']:
            factor_wl = 1
        else:
            raise ValueError("`unit_wl` must be one of ['micron', 'nm'].")
        self.wl = wl * factor_wl
        self.n_real = n
        self.n_imag = k
        self.n_cplx = self.n_real + 1.0j*self.n_imag
        
        self.interpolate_order = interpolate_order
        if self.interpolate_order > 1:
            self.f = _interp1dPicklable(self.wl, self.n_cplx, kind=self.interpolate_order)
        
        if name == None:
            self.__name__ = 'tabulated n ({})'.format(refindex_file)
        else:
            self.__name__ = name
    
    def epsilon(self, wavelength):
        """Tabulated interpolated dielectric function
    
        constant dielectric function material
        
        Parameters
        ----------
        wavelength : real
            wavelength at which to evaluate dielectric function (in nm)
        
        """
        if self.interpolate_order == 1:
            n_r = np.interp(wavelength, self.wl, self.n_real)
            n_i = np.interp(wavelength, self.wl, self.n_imag)
            eps = (n_r + 1j*n_i)**2
        else:
            eps = self.f(wavelength)**2
        return eps




#==============================================================================
# Metals
#==============================================================================
class gold(object):
    """gold index
    
    Complex dielectric function of gold from:
    P. B. Johnson and R. W. Christy. Optical Constants of the Noble Metals, 
    Phys. Rev. B 6, 4370-4379 (1972)
    
    Parameters
    ----------
    interpolate_order : int, default: 1
        interpolation order for data (1: linear, 2: square, 3: cubic)
        "1" uses `numpy`, "2" and "3" require `scipy` (`scipy.interpolate.interp1d`)
    
    """
    __name__ = 'Gold, Johnson/Christy'
    
    def __init__(self, interpolate_order=1):
        """gold dispersion"""
        self.wl = 1239.19/np.array([0.1,0.2,0.3,0.4,0.5,0.5450000,0.5910000,0.6360000,0.64,0.77,0.89,1.02,1.14,1.26,1.39,1.51,1.64,1.76,1.88,2.01,2.13,2.26,2.38,2.50,2.63,2.75,2.88,3.00,3.12,3.25,3.37,3.50,3.62,3.74,3.87,3.99,4.12,4.24,4.36,4.49,4.61,4.74,4.86,4.98,5.11,5.23,5.36,5.48,5.60])[::-1]
        self.n_real = np.array([25.17233,7.60352,3.53258,2.02586,1.299091,1.097350,0.9394755,0.8141369,0.92,0.56,0.43,0.35,0.27,0.22,0.17,0.16,0.14,0.13,0.14,0.21,0.29,0.43,0.62,1.04,1.31,1.38,1.45,1.46,1.47,1.46,1.48,1.50,1.48,1.48,1.54,1.53,1.53,1.49,1.47,1.43,1.38,1.35,1.33,1.33,1.32,1.32,1.30,1.31,1.30])[::-1]
        self.n_imag = np.array([77.92804,43.34848,29.52751,22.25181,17.77038,16.24777,14.94747,13.82771,13.78,11.21,9.519,8.145,7.15,6.35,5.66,5.08,4.542,4.103,3.697,3.272,2.863,2.455,2.081,1.833,1.849,1.914,1.948,1.958,1.952,1.933,1.895,1.866,1.871,1.883,1.898,1.893,1.889,1.878,1.869,1.847,1.803,1.749,1.688,1.631,1.577,1.536,1.497,1.460,1.427])[::-1]
        self.n_cplx = self.n_real + 1.0j*self.n_imag
        
        self.interpolate_order = interpolate_order
        if self.interpolate_order > 1:
            self.f = _interp1dPicklable(self.wl, self.n_cplx, kind=self.interpolate_order)
    
    def epsilon(self, wavelength):
        """Gold dielectric function
        
        Parameters
        ----------
        wavelength: real
            wavelength at which to evaluate dielectric function (in nm)
        
        """
        if self.interpolate_order == 1:
            n_r = np.interp(wavelength, self.wl, self.n_real)
            n_i = np.interp(wavelength, self.wl, self.n_imag)
            eps = (n_r + 1j*n_i)**2
        else:
            eps = self.f(wavelength)**2
        return eps


class silver(object):
    """gold index
    
    Complex dielectric function of silver from:
    P. B. Johnson and R. W. Christy. Optical Constants of the Noble Metals, 
    Phys. Rev. B 6, 4370-4379 (1972)
    
    Parameters
    ----------
    interpolate_order : int, default: 1
        interpolation order for data (1: linear, 2: square, 3: cubic)
        "1" uses `numpy`, "2" and "3" require `scipy` (`scipy.interpolate.interp1d`)
    
    """
    __name__ = 'Silver, Johnson/Christy'
    
    def __init__(self, interpolate_order=1):
        """silver dispersion"""
        self.wl = 1000*np.array([ 0.1879 , 0.1916 , 0.1953 , 0.1993 , 0.2033 , 0.2073 , 0.2119 , 0.2164 , 0.2214 , 0.2262 , 0.2313 , 
                                0.2371 , 0.2426 , 0.249 , 0.2551 , 0.2616 , 0.2689 , 0.2761 , 0.2844 , 0.2924 , 0.3009 , 0.3107 , 
                                0.3204 , 0.3315 , 0.3425 , 0.3542 , 0.3679 , 0.3815 , 0.3974 , 0.4133 , 0.4305 , 0.4509 , 0.4714 , 
                                0.4959 , 0.5209 , 0.5486 , 0.5821 , 0.6168 , 0.6595 , 0.7045 , 0.756 , 0.8211 , 0.892 , 0.984 , 1.088 , 1.216 , 1.393 , 1.61 , 1.937])
        self.n_real = np.array([ 1.07 , 1.1 , 1.12 , 1.14 , 1.15 , 1.18 , 1.2 , 1.22 , 1.25 , 1.26 , 1.28 , 1.28 , 1.3 , 1.31 , 
                                1.33 , 1.35 , 1.38 , 1.41 , 1.41 , 1.39 , 1.34 , 1.13 , 0.81 , 0.17 , 0.14 , 0.1 , 0.07 , 0.05 , 
                                0.05 , 0.05 , 0.04 , 0.04 , 0.05 , 0.05 , 0.05 , 0.06 , 0.05 , 0.06 , 0.05 , 0.04 , 0.03 , 0.04 , 
                                0.04 , 0.04 , 0.04 , 0.09 , 0.13 , 0.15 , 0.24 , ])
        self.n_imag = np.array([ 1.212 , 1.232 , 1.255 , 1.277 , 1.296 , 1.312 , 1.325 , 1.336 , 1.342 , 1.344 , 1.357 , 1.367 , 
                                1.378 , 1.389 , 1.393 , 1.387 , 1.372 , 1.331 , 1.264 , 1.161 , 0.964 , 0.616 , 0.392 , 0.829 , 
                                1.142 , 1.419 , 1.657 , 1.864 , 2.07 , 2.275 , 2.462 , 2.657 , 2.869 , 3.093 , 3.324 , 3.586 , 
                                3.858 , 4.152 , 4.483 , 4.838 , 5.242 , 5.727 , 6.312 , 6.992 , 7.795 , 8.828 , 10.1 , 11.85 , 14.08 , ])
        self.n_cplx = self.n_real + 1.0j*self.n_imag
        
        self.interpolate_order = interpolate_order
        if self.interpolate_order > 1:
            self.f = _interp1dPicklable(self.wl, self.n_cplx, kind=self.interpolate_order)
    
    def epsilon(self, wavelength):
        """Silver dielectric function
        
        Parameters
        ----------
        wavelength: real
            wavelength at which to evaluate dielectric function (in nm)
        
        """
        if self.interpolate_order == 1:
            n_r = np.interp(wavelength, self.wl, self.n_real)
            n_i = np.interp(wavelength, self.wl, self.n_imag)
            eps = (n_r + 1j*n_i)**2
        else:
            eps = self.f(wavelength)**2
        return eps



class alu(object):
    """alu index
    
    Complex dielectric function of aluminium from:
    A. D. Rakić, A. B. Djurišic, J. M. Elazar, and M. L. Majewski. 
    Optical properties of metallic films for vertical-cavity optoelectronic 
    devices, Appl. Opt. 37, 5271-5283 (1998)
    
    Parameters
    ----------
    interpolate_order : int, default: 1
        interpolation order for data (1: linear, 2: square, 3: cubic)
        "1" uses `numpy`, "2" and "3" require `scipy` (`scipy.interpolate.interp1d`)

    """
    __name__ = 'Aluminium, Rakic'
    
    def __init__(self, interpolate_order=1):
        """alu dispersion"""
        self.wl = 1239.19/np.array([0.1,0.2,0.3,0.4,0.5,0.5450000,0.5910000,0.6360000,0.64,0.77,0.89,1.02,1.14,1.26,1.39,1.51,1.64,1.76,1.88,2.01,2.13,2.26,2.38,2.50,2.63,2.75,2.88,3.00,3.12,3.25,3.37,3.50,3.62,3.74,3.87,3.99,4.12,4.24,4.36,4.49,4.61,4.74,4.86,4.98,5.11,5.23,5.36,5.48,5.60])[::-1]
        self.n_real = np.array([28.842,12.493,7.0377,4.42,3.0379,2.6323,2.3078,2.0574,2.0379,1.5797,1.3725,1.3007,1.3571,1.5656,2.1077,2.7078,2.3029,1.6986,1.3879,1.2022,1.0767,.95933,.86160,0.77308,0.68783,0.61891,0.55416,0.50256,0.45783,0.41611,0.38276,0.35151,0.32635,0.30409,0.28294,0.26559,0.24887,0.23503,0.22254,0.21025,0.19997,0.18978,0.18114,0.17313,0.16511,0.15823,0.15126,0.14523,0.13956])[::-1]
        self.n_imag = np.array([99.255,55.533,39.303,30.285,24.498,22.52,20.782,19.304,19.182,15.847,13.576,11.666,10.250,9.0764,8.1465,8.1168,8.4545,8.0880,7.5779,7.1027,6.7330,6.3818,6.0889,5.8179,5.5454,5.3107,5.0734,4.8691,4.6779,4.4849,4.3185,4.1501,4.0048,3.8682,3.7294,3.6090,3.4862,3.3793,3.2782,3.1745,3.0838,2.9906,2.9088,2.8308,2.7502,2.6792,2.6056,2.5406,2.4783])[::-1]
        self.n_cplx = self.n_real + 1.0j*self.n_imag
        
        self.interpolate_order = interpolate_order
        if self.interpolate_order > 1:
            self.f = _interp1dPicklable(self.wl, self.n_cplx, kind=self.interpolate_order)
    
    def epsilon(self, wavelength):
        """Aluminium dielectric function
        
        Parameters
        ----------
        wavelength: real
            wavelength at which to evaluate dielectric function (in nm)
        
        """
        if self.interpolate_order == 1:
            n_r = np.interp(wavelength, self.wl, self.n_real)
            n_i = np.interp(wavelength, self.wl, self.n_imag)
            eps = (n_r + 1j*n_i)**2
        else:
            eps = self.f(wavelength)**2
        return eps




#==============================================================================
# Dielectrica
#==============================================================================
class silicon(object):
    """silicon index
    
    Complex dielectric function of silicon from:
    Edwards, D. F. in Handbook of Optical Constants of Solids 
    (ed. Palik, E. D.) 547–569 (Academic Press, 1997).

    Parameters
    ----------
    interpolate_order : int, default: 1
        interpolation order for data (1: linear, 2: square, 3: cubic)
        "1" uses `numpy`, "2" and "3" require `scipy` (`scipy.interpolate.interp1d`)
    
    """
    __name__ = 'Silicon, Palik'
    
    def __init__(self, interpolate_order=1):
        """silicon dispersion"""
        self.wl = 1239.19/np.array([0.70,0.80,0.90,1.00,1.10,1.20,1.3,1.4,2.0,2.2,2.4,2.6,2.8,3.0,3.2,3.4,3.6,3.8,4.0,4.4,4.8])[::-1]
        self.n_real = np.array([3.459338,3.476141,3.496258,3.519982,3.539048,3.57,3.6,3.63,3.94,4.08,4.26,4.5,4.82,5.31,6.18,6.53,5.25,5.01,4.91,2.92,1.6])[::-1]
        self.n_imag = np.array([0.0000000,0.0000000,0.0000000,0.0000000,0.000017,0.00038,0.00157,0.00346,0.01,0.01,0.01,0.02,0.11,0.25,0.65,2.93,3.13,3.33,3.74,5.28,3.91])[::-1]
        self.n_cplx = self.n_real + 1.0j*self.n_imag
        
        self.interpolate_order = interpolate_order
        if self.interpolate_order > 1:
            self.f = _interp1dPicklable(self.wl, self.n_cplx, kind=self.interpolate_order)
    
        
    def epsilon(self, wavelength):
        """Silicon dielectric function
        
        Parameters
        ----------
        wavelength: real
            wavelength at which to evaluate dielectric function (in nm)
        
        """
        if self.interpolate_order == 1:
            n_r = np.interp(wavelength, self.wl, self.n_real)
            n_i = np.interp(wavelength, self.wl, self.n_imag)
            eps = (n_r + 1j*n_i)**2
        else:
            eps = self.f(wavelength)**2
        return eps



class sio2(object):
    """SiO2 refractive index
    
    Contributed by C. Majorel
    
    Complex dielectric function for SiO2 from:
        - range 210nm --> 6700nm :
          I. H. Malitson. 
          *Interspecimen comparison of the refractive index of fused silica*,
          J. Opt. Soc. Am. 55, 1205-1208 (1965)
    
        - range 7000nm --> 50000nm :
         S. Popova, T. Tolstykh, V. Vorobev. 
         *Optical characteristics of amorphous quartz in the 1400–200 cm-1 region*,
         Opt. Spectrosc. 33, 444–445 (1972)
         
    Parameters
    ----------
    interpolate_order : int, default: 1
        interpolation order for data (1: linear, 2: square, 3: cubic)
        "1" uses `numpy`, "2" and "3" require `scipy` (`scipy.interpolate.interp1d`)
    """
    __name__ = 'SiO2'

    def __init__(self, interpolate_order=1):
        self.wl = 1239.19/np.array([0.0247838 , 0.02554873, 0.02631368, 0.02707902, 0.02784384,
           0.0286088 , 0.02937374, 0.03013888, 0.03090404, 0.03166935,
           0.03243443, 0.03319911, 0.03396437, 0.03472969, 0.03549467,
           0.03625907, 0.03702501, 0.0377894 , 0.03855481, 0.03931939,
           0.04008507, 0.04085017, 0.04161428, 0.04237996, 0.04314428,
           0.04391021, 0.04467481, 0.04543984, 0.04620568, 0.04696926,
           0.04773459, 0.04850059, 0.04926609, 0.05002988, 0.0507948 ,
           0.05155987, 0.05232624, 0.0530907 , 0.05385441, 0.05462115,
           0.05538527, 0.05615071, 0.05691668, 0.05767967, 0.05844684,
           0.05921206, 0.05997435, 0.06074163, 0.06150437, 0.06227085,
           0.06303744, 0.06380013, 0.06456469, 0.06533056, 0.06609718,
           0.06686036, 0.06762661, 0.06839174, 0.06915509, 0.06991988,
           0.07068564, 0.07145188, 0.07221808, 0.07297939, 0.07374814,
           0.07451085, 0.07527579, 0.07604259, 0.07680612, 0.07757058,
           0.07833555, 0.0791006 , 0.0798653 , 0.08063444, 0.08139714,
           0.08216351, 0.08292779, 0.08368947, 0.08445951, 0.08522041,
           0.08598917, 0.08675371, 0.0875196 , 0.08828026, 0.08904786,
           0.08980939, 0.09057744, 0.09134527, 0.09210569, 0.09287192,
           0.09363684, 0.09440009, 0.09516857, 0.09593481, 0.0966984 ,
           0.09746657, 0.09823147, 0.09899265, 0.09975769, 0.10052649,
           0.10129067, 0.10204974, 0.10282028, 0.10358522, 0.10434406,
           0.10511409, 0.10587748, 0.10664286, 0.10741007, 0.10816952,
           0.10893978, 0.10970166, 0.11046443, 0.11123788, 0.11200199,
           0.1127664 , 0.11353092, 0.11429533, 0.11505942, 0.11582297,
           0.11658576, 0.11735865, 0.11811934, 0.11887855, 0.11964758,
           0.12041493, 0.12118032, 0.12194352, 0.12270423, 0.12347449,
           0.12424203, 0.12500656, 0.12576779, 0.12653834, 0.12730532,
           0.12806842, 0.12882732, 0.12959527, 0.13035872, 0.13113122,
           0.13188484, 0.13266139, 0.13341839, 0.13418408, 0.13494392,
           0.13571241, 0.13647467, 0.13724554, 0.1380098 , 0.13878262,
           0.13954842, 0.14030684, 0.14107354, 0.14183244, 0.14259954,
           0.1433584 , 0.14412538, 0.14490061, 0.1456671 , 0.14642444,
           0.14718969, 0.14796299, 0.1487266 , 0.1494801 , 0.15025949,
           0.15101024, 0.15178711, 0.15255324, 0.15330818, 0.15407062,
           0.15484068, 0.15559895, 0.15636467, 0.15713797, 0.15789883,
           0.15866709, 0.15942236, 0.16020556, 0.16095467, 0.16173192,
           0.16249541, 0.16326614, 0.1640225 , 0.1647859 , 0.16555645,
           0.1663119 , 0.16707429, 0.16784369, 0.16859728, 0.16938081,
           0.17014829, 0.17089919, 0.17168052, 0.17244503, 0.17319217,
           0.17397024, 0.17473068, 0.1754978 , 0.17627169, 0.17702714,
           0.185, 0.191, 0.198, 0.205, 0.212, 0.22 , 0.228, 0.236, 0.244,
           0.253, 0.261, 0.271, 0.28 , 0.29 , 0.3  , 0.311, 0.322, 0.333,
           0.345, 0.357, 0.37 , 0.383, 0.396, 0.41 , 0.425, 0.44 , 0.455,
           0.471, 0.488, 0.505, 0.523, 0.541, 0.56 , 0.58 , 0.6  , 0.621,
           0.643, 0.666, 0.69 , 0.714, 0.739, 0.765, 0.792, 0.82 , 0.849,
           0.879, 0.91 , 0.942, 0.975, 1.009, 1.045, 1.081, 1.119, 1.159,
           1.2  , 1.242, 1.286, 1.331, 1.378, 1.427, 1.477, 1.529, 1.583,
           1.639, 1.696, 1.756, 1.818, 1.882, 1.948, 2.017, 2.088, 2.162,
           2.238, 2.317, 2.398, 2.483, 2.57 , 2.661, 2.755, 2.852, 2.953,
           3.056, 3.164, 3.276, 3.39 , 3.51 , 3.634, 3.762, 3.894, 4.031,
           4.174, 4.321, 4.474, 4.631, 4.794, 4.963, 5.138, 5.318, 5.505,
           5.7  , 5.901])[::-1]
        self.n_real = np.array([2.1269 , 2.1333 , 2.14   , 2.1468 , 2.1538 , 2.161  , 2.1683 ,
           2.1757 , 2.1834 , 2.1911 , 2.199  , 2.2071 , 2.2153 , 2.2237 ,
           2.2323 , 2.2411 , 2.2502 , 2.2597 , 2.2696 , 2.2801 , 2.2912 ,
           2.3031 , 2.3162 , 2.3307 , 2.3469 , 2.3655 , 2.3873 , 2.4135 ,
           2.4458 , 2.4867 , 2.5393 , 2.6066 , 2.6892 , 2.7833 , 2.8778 ,
           2.9553 , 2.996  , 2.9849 , 2.9235 , 2.8434 , 2.797  , 2.7727 ,
           2.6253 , 2.2223 , 1.627  , 1.0459 , 0.64964, 0.47899, 0.47742,
           0.57308, 0.70859, 0.83655, 0.93929, 1.0193 , 1.0825 , 1.1338 ,
           1.1767 , 1.2133 , 1.2454 , 1.274  , 1.3002 , 1.3245 , 1.3474 ,
           1.3692 , 1.3903 , 1.4108 , 1.4309 , 1.4508 , 1.4706 , 1.4904 ,
           1.5102 , 1.5301 , 1.5502 , 1.5706 , 1.5915 , 1.6128 , 1.6347 ,
           1.6574 , 1.6809 , 1.7053 , 1.7308 , 1.7571 , 1.7842 , 1.8118 ,
           1.8395 , 1.8665 , 1.8922 , 1.9155 , 1.9355 , 1.9511 , 1.9613 ,
           1.9654 , 1.9628 , 1.9533 , 1.9371 , 1.9148 , 1.8878 , 1.8574 ,
           1.8258 , 1.795  , 1.7676 , 1.7455 , 1.7306 , 1.7241 , 1.7263 ,
           1.7367 , 1.7541 , 1.7771 , 1.804  , 1.8333 , 1.8637 , 1.8942 ,
           1.9241 , 1.9532 , 1.9813 , 2.0083 , 2.0346 , 2.0603 , 2.0859 ,
           2.1118 , 2.1385 , 2.1668 , 2.1976 , 2.232  , 2.2716 , 2.3179 ,
           2.3728 , 2.4379 , 2.5138 , 2.5994 , 2.6914 , 2.784  , 2.8688 ,
           2.9357 , 2.9745 , 2.9763 , 2.9355 , 2.8522 , 2.7339 , 2.5964 ,
           2.4584 , 2.3276 , 2.1858 , 1.9957 , 1.7328 , 1.4105 , 1.0751 ,
           0.77982, 0.5599 , 0.42224, 0.35117, 0.32322, 0.31913, 0.32728,
           0.34129, 0.35732, 0.3727 , 0.38552, 0.39445, 0.39873, 0.39805,
           0.39251, 0.3825 , 0.36867, 0.3518 , 0.33282, 0.31265, 0.2923 ,
           0.27281, 0.25535, 0.24142, 0.23338, 0.23579, 0.25819, 0.31199,
           0.38597, 0.45799, 0.52129, 0.57619, 0.62405, 0.66613, 0.70345,
           0.73681, 0.76686, 0.79409, 0.81893, 0.8417 , 0.86269, 0.88212,
           0.90019, 0.91703, 0.9328 , 0.9476 , 0.96153, 0.97467, 0.98709,
           0.99885, 1.01   , 1.0206 , 1.0307,
           1.15964941, 1.19732567, 1.22808884, 1.25372896, 1.2753724 ,
           1.29374603, 1.3096384 , 1.32341054, 1.33548236, 1.34611712,
           1.35552622, 1.36388143, 1.37137013, 1.37809977, 1.38412081,
           1.38955534, 1.39450357, 1.398982  , 1.4030709 , 1.40677821,
           1.41016968, 1.41327416, 1.41611729, 1.41874595, 1.42115442,
           1.42336137, 1.42540443, 1.42729609, 1.42902873, 1.4306517 ,
           1.43213721, 1.43352988, 1.43481962, 1.43601396, 1.43713496,
           1.43817294, 1.43914807, 1.44005094, 1.44091337, 1.44171217,
           1.44246458, 1.44317393, 1.4438434 , 1.44447599, 1.44508615,
           1.44566458, 1.44621385, 1.44673635, 1.44724558, 1.44773225,
           1.44820966, 1.44866831, 1.44912146, 1.44957109, 1.45000696,
           1.45044774, 1.4508854 , 1.45132408, 1.45176538, 1.45221382,
           1.45267127, 1.45313961, 1.45361885, 1.45411617, 1.45462988,
           1.45516603, 1.4557247 , 1.45631041, 1.4569256 , 1.45757581,
           1.45826079, 1.45898656, 1.45975629, 1.46057308, 1.46144499,
           1.46237644, 1.46337193, 1.46443603, 1.46558083, 1.46680482,
           1.46812182, 1.46952865, 1.47105251, 1.47270468, 1.47446828,
           1.47639513, 1.47846765, 1.48071444, 1.48315043, 1.48579144,
           1.48868328, 1.4918215 , 1.49526272, 1.49899922, 1.50310096,
           1.50760959, 1.51257212, 1.51804177, 1.52407891, 1.53084643,
           1.53835762])[::-1]
        self.n_imag = np.array([2.6352e-02, 2.9326e-02, 3.2541e-02, 3.6005e-02, 3.9724e-02,
           4.3703e-02, 4.7942e-02, 5.2444e-02, 5.7205e-02, 6.2220e-02,
           6.7483e-02, 7.2984e-02, 7.8707e-02, 8.4637e-02, 9.0753e-02,
           9.7031e-02, 1.0344e-01, 1.0995e-01, 1.1653e-01, 1.2313e-01,
           1.2970e-01, 1.3620e-01, 1.4256e-01, 1.4872e-01, 1.5460e-01,
           1.6013e-01, 1.6524e-01, 1.6997e-01, 1.7459e-01, 1.8005e-01,
           1.8869e-01, 2.0509e-01, 2.3667e-01, 2.9283e-01, 3.8235e-01,
           5.0927e-01, 6.6912e-01, 8.4656e-01, 1.0168e+00, 1.1582e+00,
           1.2919e+00, 1.5093e+00, 1.8693e+00, 2.2623e+00, 2.4709e+00,
           2.3613e+00, 1.9957e+00, 1.5470e+00, 1.1472e+00, 8.4325e-01,
           6.4166e-01, 5.2139e-01, 4.4773e-01, 3.9781e-01, 3.6046e-01,
           3.3034e-01, 3.0472e-01, 2.8211e-01, 2.6164e-01, 2.4278e-01,
           2.2521e-01, 2.0870e-01, 1.9314e-01, 1.7843e-01, 1.6451e-01,
           1.5135e-01, 1.3893e-01, 1.2723e-01, 1.1623e-01, 1.0592e-01,
           9.6296e-02, 8.7350e-02, 7.9080e-02, 7.1492e-02, 6.4607e-02,
           5.8466e-02, 5.3138e-02, 4.8732e-02, 4.5407e-02, 4.3376e-02,
           4.2918e-02, 4.4364e-02, 4.8095e-02, 5.4510e-02, 6.3994e-02,
           7.6872e-02, 9.3353e-02, 1.1348e-01, 1.3710e-01, 1.6378e-01,
           1.9287e-01, 2.2343e-01, 2.5429e-01, 2.8410e-01, 3.1140e-01,
           3.3471e-01, 3.5261e-01, 3.6393e-01, 3.6779e-01, 3.6384e-01,
           3.5228e-01, 3.3396e-01, 3.1038e-01, 2.8351e-01, 2.5554e-01,
           2.2861e-01, 2.0446e-01, 1.8428e-01, 1.6870e-01, 1.5779e-01,
           1.5130e-01, 1.4871e-01, 1.4939e-01, 1.5270e-01, 1.5805e-01,
           1.6489e-01, 1.7276e-01, 1.8127e-01, 1.9010e-01, 1.9898e-01,
           2.0768e-01, 2.1606e-01, 2.2405e-01, 2.3174e-01, 2.3955e-01,
           2.4839e-01, 2.5997e-01, 2.7696e-01, 3.0319e-01, 3.4335e-01,
           4.0252e-01, 4.8529e-01, 5.9474e-01, 7.3159e-01, 8.9351e-01,
           1.0749e+00, 1.2666e+00, 1.4571e+00, 1.6338e+00, 1.7877e+00,
           1.9219e+00, 2.0559e+00, 2.2144e+00, 2.3996e+00, 2.5754e+00,
           2.6841e+00, 2.6819e+00, 2.5650e+00, 2.3684e+00, 2.1422e+00,
           1.9265e+00, 1.7402e+00, 1.5855e+00, 1.4582e+00, 1.3533e+00,
           1.2668e+00, 1.1955e+00, 1.1365e+00, 1.0871e+00, 1.0446e+00,
           1.0069e+00, 9.7180e-01, 9.3744e-01, 9.0224e-01, 8.6486e-01,
           8.2419e-01, 7.7932e-01, 7.2947e-01, 6.7391e-01, 6.1185e-01,
           5.4230e-01, 4.6388e-01, 3.7502e-01, 2.7665e-01, 1.8314e-01,
           1.1748e-01, 7.8079e-02, 5.3868e-02, 3.8185e-02, 2.7613e-02,
           2.0285e-02, 1.5101e-02, 1.1372e-02, 8.6501e-03, 6.6368e-03,
           5.1287e-03, 3.9857e-03, 3.1103e-03, 2.4340e-03, 1.9077e-03,
           1.4959e-03, 1.1725e-03, 9.1794e-04, 7.1740e-04, 5.5945e-04,
           4.3518e-04, 3.3757e-04, 2.6108e-04, 2.0129e-04, 1.5469e-04,
           0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.])[::-1]
        
        self.n_cplx = self.n_real + 1.0j*self.n_imag
        
        self.interpolate_order = interpolate_order
        if self.interpolate_order > 1:
            self.f = _interp1dPicklable(self.wl, self.n_cplx, kind=self.interpolate_order)
    
    def n_cmplx(self, wavelength):
        if self.interpolate_order == 1:
            n_r = np.interp(wavelength, self.wl, self.n_real)
            n_i = np.interp(wavelength, self.wl, self.n_imag)
            n_c = n_r + 1j*n_i
        else:
            n_c = self.f(wavelength)
        return n_c
    
    def epsilon(self, wavelength):
        return self.n_cmplx(wavelength)**2



class tio2(object):
    """TiO2 dispersion 
    
    model for visible and NIR range (~500nm - ~1500nm)
    from https://refractiveindex.info/?shelf=main&book=TiO2&page=Devore-o
    """
    def __init__(self):
        self.__name__ = 'TiO2 (Devore)'
    
    def epsilon(self, wavelength):
        """TiO2 dielectric function
        
        Parameters
        ----------
        wavelength : real
            wavelength (in nm) at which to evaluate dielectric function
        
        """
        eps = 5.913 + 0.2441 / ((wavelength/1E3)**2 - 0.0803)
        eps = complex(eps)
        
        return eps



# =============================================================================
# Hyperdoped dielectrics (having a plasmon resonance)
# =============================================================================
class hyperdopedConstantDielectric(object):    
    """hyperdoped material with constant ref.index + dopant plasmon resonance
    
    Parameters
    ----------
    n : complex
        constant complex refractive index
    N_dop : float
        Dopant density (cm^-3)
    factor_gamma : float. default: 0.1
        ratio damping term and plasmon frequency. The default of 0.1 is chosen 
        arbitrarily, resulting in some reasonably broad resonances. The 
        correct value must be obtained experimentally.
    carrier : string, default: 'electron'
        carrier type. 'electron' or 'hole'
    act_eff : float 
        Activation efficiency of dopants, value between 0 and 1. 
        (0=0%, 1=100% activated dopants; the latter being the default behavior)
    
    Notes
    -----
    For details about the theory and for a discussion on how to choose a value 
    for the damping term, see:
        
    [1] C. Majorel et al. "Theory of plasmonic properties of hyper-doped 
    silicon nanostructures". **Optics Communications** 453, 124336 (2019).   
    URL https://doi.org/10.1016/j.optcom.2019.124336
    """    
    
    e = 4.8027e-10          # elementary charge (StatC) 1StatC = 3.33564e-10C 
    me = 9.109e-28          # electron mass (g)
    c=2.99792458e17                 #vitesse de la lumière en nm/s
    def __init__(self, n, N_dop, factor_gamma=0.1, act_eff=1.0, carrier='electron'):
        """Define constant material"""
        self.n = complex(n)
        self.__name__ = 'constant index material, n={}'.format(self.n)
        
        if carrier == 'electron':
            self.m0 = 0.3*self.me
        elif carrier == 'hole':
            self.m0 = 0.4*self.me
        
        self.act_eff = act_eff    
        self.N_dop = N_dop
        self.factor_gamma = factor_gamma
        self.wp = np.sqrt(4.*np.pi*self.N_dop*self.act_eff*self.e**2/self.m0)
        
    def pure_epsilon(self, wavelength):
        """Constant dielectric function
        
        Parameters
        ----------
        wavelength : real
            wavelength at which to evaluate dielectric function (in nm)
        """        
        self.pure_eps = complex(self.n**2)
        return self.pure_eps

    def epsilon(self, wavelength):
        """Doped dummy material: adding a plasmon resonance
        
        Parameters
        ----------
        wavelength : real
            wavelength at which to evaluate dielectric function (in nm)
        
        """        
        self.frequency = 2*np.pi*self.c/wavelength
        self.pure_eps = self.pure_epsilon(wavelength)
        self.Gamma = self.factor_gamma*self.wp
        eps = self.pure_eps - (self.wp**2/(self.frequency*(self.frequency+1.0j*self.Gamma)))
        return eps



class hyperdopedFromFile(fromFile):
    """Add doping-induced plasmon response to tabulated dielectric permittivity
    
    Parameters
    ----------
    refindex_file : str
        path to text-file with the tabulated refractive index 
        (3 whitespace separated columns: #1 wavelength, #2 real(n), #3 imag(n))        
        Data can be obtained e.g. from https://refractiveindex.info/ 
        using the *"Full database record"* export function.
    
    Ndop : float
        Dopant density (cm^-3)
        
    damping : float 
        damping term (s^-1). See [1] for a discussion on how to choose the damping.
        
    k_mass : float
        ratio between the mass of the electron and the effective mass in the material
        
    unit_wl : str, default: 'micron'
        Units of the wavelength in file, one of ['micron', 'nm']
    
    interpolate_order : int, default: 1
        interpolation order for data (1: linear, 2: square, 3: cubic)
        "1" uses `numpy.interp`, "2" and "3" require `scipy` 
        (using `scipy.interpolate.interp1d`)
    
    name : str, default: None
        optional name attribute for material class. By default use filename.
        
    
    Notes
    -----
    For details about the theory and for a discussion on how to choose a value 
    for the damping term, see:
        
    [1] C. Majorel et al. "Theory of plasmonic properties of hyper-doped 
    silicon nanostructures". **Optics Communications** 453, 124336 (2019).   
    URL https://doi.org/10.1016/j.optcom.2019.124336
    """
    e = 4.8027e-10          # elementary charge (StatC) 1StatC = 3.33564e-10C 
    me = 9.109e-28          # electron mass (g)
    c=2.99792458e17         # speed of light (nm/s)
        
    def __init__(self, refindex_file, Ndop, k_mass, damping, 
                 unit_wl='micron', interpolate_order=1, name=None):
        super(self.__class__, self).__init__(refindex_file, unit_wl, 
                                                     interpolate_order, name)
        self.Ndop = Ndop
        self.k_mass = k_mass
        self.damping = damping
    
    
    def epsilon_undoped(self, wavelength):
        """permittivity from undoped material (as from file)"""
        return super().epsilon(wavelength)
        

    def epsilon(self, wavelength):
        """permittivity including plasmon response through doping"""
        self.pure_eps = self.epsilon_undoped(wavelength)
        self.m0 = self.k_mass*self.me
        self.wp = np.sqrt(4.*np.pi*self.Ndop*self.e**2/self.m0)
        self.frequency = 2*np.pi*self.c/wavelength
        eps_dop = self.pure_eps - (self.wp**2/(self.frequency*(self.frequency+1.0j*self.damping*2.*np.pi)))
        return eps_dop
    
    
    
class hyperdopedSilicon(object):
    """hyperdoped silicon with plasmon resonance
    
    Complex dielectric function of silicon (<1770nm) from:
    Edwards, D. F. in Handbook of Optical Constants of Solids 
    (ed. Palik, E. D.) 547–569 (Academic Press, 1997).
    
    and range 1770nm --> 22220 nm :
    
    Parameters
    ----------
    N_dop : float
        Dopant density (cm^-3)
    factor_gamma : float, default: 0.1
        ratio damping term and plasmon frequency. The default of 0.1 is an arbitrary
        resulting in some reasonably broad resonances. The correct value must 
        be obtained experimentally.
    carrier : string, default: 'electron'
        carrier type. 'electron' or 'hole'
    act_eff : float , default: 1
        Activation efficiency of dopants, value between 0 and 1. 
        (0=0%, 1=100% activated dopants; the latter being the default behavior)
    
    Notes
    -----
    See also:
    [1] D. Chandler-Horowitz and P. M. Amirtharaj. 
    "High-accuracy, midinfrared refractive index values of silicon". 
    **J. Appl. Phys.** 97, 123526 (2005).
    URL https://doi.org/10.1063/1.1923612
    
    [2] C. Majorel et al. "Theory of plasmonic properties of hyper-doped 
    silicon nanostructures". **Optics Communications** 453, 124336 (2019).   
    URL https://doi.org/10.1016/j.optcom.2019.124336
    """    
    __name__ = 'hyperdoped silicon'
    e = 4.8027e-10          # elementary charge (StatC) 1StatC = 3.33564e-10C 
    me = 9.109e-28          # electron mass (g)
    c=2.99792458e17         # speed of light (nm/s)
    def __init__(self, N_dop, factor_gamma=0.1, act_eff=1.0, carrier='electron'):
        if carrier == 'electron':
            self.m0 = 0.3*self.me
        elif carrier == 'hole':
            self.m0 = 0.4*self.me
        
        self.act_eff = act_eff    
        self.N_dop = N_dop
        self.factor_gamma = factor_gamma
        self.wp = np.sqrt(4.*np.pi*self.N_dop*self.act_eff*self.e**2/self.m0)
        
        self.wl = 1239.19/np.array([0.05576,0.0619,0.0751,0.07597,0.0769,0.0986,0.1240,0.1982,0.4956,0.70,0.80,0.90,1.00,1.10,1.20,1.3,1.4,2.0,2.2,2.4,2.6,2.8,3.0,3.2,3.4,3.6,3.8,4.0,4.4,4.8])[::-1]
        self.n_real = np.array([3.416898,3.416966,3.417140,3.417153,3.417167,3.417532,3.418072,3.420365,3.440065,3.459338,3.476141,3.496258,3.519982,3.539048,3.57,3.6,3.63,3.94,4.08,4.26,4.5,4.82,5.31,6.18,6.53,5.25,5.01,4.91,2.92,1.6])[::-1]
        self.n_imag = np.array([0.0000762,0.000211,0.0008,0.024,0.017,0.000191,0.0000666,0.0000026,0.0000000,0.0000000,0.0000000,0.0000000,0.0000000,0.000017,0.00038,0.00157,0.00346,0.01,0.01,0.01,0.02,0.11,0.25,0.65,2.93,3.13,3.33,3.74,5.28,3.91])[::-1]
        
    
    def pure_epsilon(self, wavelength):
        """Pure Silicon dielectric function
        
        Parameters
        ----------
        wavelength: real
            wavelength at which to evaluate dielectric function (in nm)
        """
        n_r = np.interp(wavelength, self.wl, self.n_real)
        n_i = np.interp(wavelength, self.wl, self.n_imag)
        self.pure_eps = (n_r + 1j*n_i)**2
        return self.pure_eps

    def epsilon(self, wavelength):
        """Doped Silicon dielectric function: adding a plasmon resonance
        
        Parameters
        ----------
        wavelength: real
            wavelength at which to evaluate dielectric function (in nm)
        """        
        self.frequency = 2*np.pi*self.c/wavelength
        self.pure_eps = self.pure_epsilon(wavelength)
        self.Gamma = self.factor_gamma*self.wp
        eps = self.pure_eps - (self.wp**2/(self.frequency*(self.frequency+1.0j*self.Gamma)))
        return eps






## -- list of all available material classes
MAT_LIST = [dummy, gold, silver, alu, silicon,  sio2, tio2,
            fromFile,
            hyperdopedConstantDielectric, hyperdopedSilicon, 
            hyperdopedFromFile]