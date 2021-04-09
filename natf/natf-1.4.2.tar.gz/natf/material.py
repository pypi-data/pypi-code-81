#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
''' class Material.'''

thisdir = os.path.dirname(os.path.abspath(__file__))
appendix16 = os.path.join(thisdir, "data", "appendix16")

class Material(object):
    """calsee Material, used to store material information"""

    def __init__(self):
        self._mat_id = -1
        self._atom_density = -1.0
        self._density = -1.0
        self._mcnp_material_nuclide = []
        self._mcnp_material_atom_fraction = []
        self._mcnp_material_mass_fraction = []
        self._fispact_material_nuclide = []
        self._fispact_material_atom_kilogram = []

    @property
    def mat_id(self):
        return self._mat_id

    @mat_id.setter
    def mat_id(self, value):
        if not isinstance(value, int):
            raise ValueError('mat_id must be an integer!')
        if value > 100000 or value < 0:
            raise ValueError(
                'mat_id must between 0 ~ 100000(the max cell number of MCNP')
        self._mat_id = value

    @property
    def atom_density(self):
        return self._atom_density

    @atom_density.setter
    def atom_density(self, value):
        if not isinstance(value, float) and not isinstance(value, int):
            raise ValueError('atom_density must be a float')
        if value < 0:
            raise ValueError('atom_density should be larger than 0')
        if value > 1:
            raise ValueError(
                'atom_density is larger than 1.0, No material fits')
        self._atom_density = value

    @property
    def density(self):
        return self._density

    @density.setter
    def density(self, value):
        if not isinstance(value, float) and not isinstance(value, int):
            raise ValueError('density should be a float!')
        if value < 0:
            raise ValueError('density should be larger than 0!')
        if value > 30:
            raise ValueError(
                'density larger than 30, greater than the densitiest material in the world!')
        self._density = value

    @property
    def mcnp_material_nuclide(self):
        return self._mcnp_material_nuclide

    @mcnp_material_nuclide.setter
    def mcnp_material_nuclide(self, value):
        if not isinstance(value, list):
            raise ValueError('mcnp_material_nuclide should be a list')
        for i in range(len(value)):
            if not isinstance(value[i], str):
                raise ValueError(
                    'mcnp_material_nuclide should be a list of string')
            if not value[i].isdigit():
                raise ValueError(
                    'mcnp_material_nuclide should be a list of string that composed of digit')
            if len(value[i]) < 3 or len(value[i]) > 6:
                raise ValueError(
                    'mcnp_material_nuclide should be a list of string with length between 3~6')
        self._mcnp_material_nuclide = value

    @property
    def mcnp_material_atom_fraction(self):
        return self._mcnp_material_atom_fraction

    @mcnp_material_atom_fraction.setter
    def mcnp_material_atom_fraction(self, value):
        if not isinstance(value, list):
            raise ValueError('mcnp_material_atom_fraction should be a list')
        fraction_sum = 0.0
        for i in range(len(value)):
            if not isinstance(
                    value[i],
                    float) and not isinstance(
                    value[i],
                    int):
                raise ValueError(
                    'mcnp_material_atom_fraction should be a list of float/int')
            if value[i] < 0 or value[i] > 1:
                raise ValueError(
                    'mcnp_material_atom_fraction should be a list of float between 0 ~ 1')
            fraction_sum += value[i]
        if abs(fraction_sum - 1) > 1e-3:
            raise ValueError(
                'mcnp_material_atom_fraction should be a list that sum to be 1.0')
        if len(self._mcnp_material_nuclide) != 0 and len(
                value) != len(self._mcnp_material_nuclide):
            raise ValueError(
                'the lenght of mcnp_material_atom_fraction should equals to the length of mcnp_material_nuclide! check them')
        self._mcnp_material_atom_fraction = value

    @property
    def mcnp_material_mass_fraction(self):
        return self._mcnp_material_mass_fraction

    @mcnp_material_mass_fraction.setter
    def mcnp_material_mass_fraction(self, value):
        if not isinstance(value, list):
            raise ValueError('mcnp_material_mass_fraction should be a list')
        fraction_sum = 0.0
        for i in range(len(value)):
            if not isinstance(
                    value[i],
                    float) and not isinstance(
                    value[i],
                    int):
                raise ValueError(
                    'mcnp_material_mass_fraction should be a list of float/int')
            if value[i] < 0 or value[i] > 1:
                raise ValueError(
                    'mcnp_material_mass_fraction should be a list of float between 0 ~ 1')
            fraction_sum += value[i]
        if abs(fraction_sum - 1) > 1e-3:
            raise ValueError(
                'mcnp_material_mass_fraction should be a list that sum to be 1.0')
        if len(self._mcnp_material_nuclide) != 0 and len(
                value) != len(self._mcnp_material_nuclide):
            raise ValueError(
                'the lenght of mcnp_material_mass_fraction should equals to the length of mcnp_material_nuclide! check them')
        self._mcnp_material_mass_fraction = value

    # fispact_material_nuclide is a read only variable, so it doesn't have a
    # setter
    @property
    def fispact_material_nuclide(self):
        return self._fispact_material_nuclide

    # fispact_material_atom_kilogram is a read only variable, so it doesn't
    # have a setter
    @property
    def fispact_material_atom_kilogram(self):
        return self._fispact_material_atom_kilogram

    # convert the mcnp material to fispact material
    def mat_mcnp2fispact(self):
        if len(self._mcnp_material_nuclide) == 0:
            return
        if self._density < 0.0:
            raise Exception(
                'the density of the material should be set before convert')
        # convert the mcnp nuclide to fispact nuclide
        ELE_TABLE = ('H','HE','LI','BE','B',
                     'C','N','O','F','NE',
                     'NA','MG','AL','SI','P',
                     'S','CL','AR','K','CA',
                     'SC','TI','V','CR','MN',
                     'FE','CO','NI','CU','ZN',
                     'GA','GE','AS','SE','BR',
                     'KR','RB','SR','Y','ZR',
                     'NB','MO','TC','RU','RH',
                     'PD','AG','CD','IN','SN',
                     'SB','TE','I','XE','CS',
                     'BA','LA','CE','PR','ND',
                     'PM','SM','EU','GD','TB',
                     'DY','HO','ER','TM','YB',
                     'LU','HF','TA','W','RE',
                     'OS','IR','PT','AU','HG',
                     'TL','PB','BI','PO','AT',
                     'RN','FR','RA','AC','TH',
                     'PA','U','NP','PU','AM',
                     'CM','BK','CF','ES','FM')
        for i in range(len(self._mcnp_material_nuclide)):
            nuc = self._mcnp_material_nuclide[i]
            p = int(nuc) // 1000  # get the p number
            a = int(nuc) % 1000  # get the a number
            scale = self._atom_density * \
                self._mcnp_material_atom_fraction[i] * 1e24 * 1e3 / self._density
            if a != 0:
                self._fispact_material_nuclide.append(
                    ELE_TABLE[p - 1] + str(a))
                self._fispact_material_atom_kilogram.append(scale)
            if a == 0:
                # open the abundance file
                fin = open(appendix16)
                for line in fin:
                    line_ele = line.split()
                    if int(line_ele[0]) == p:
                        if (line_ele[1]) == '0.0':
                            errormessage = ''.join(
                                ['Nuclide: ', nuc, ' has no natural isotopes\n'])
                            raise ValueError(errormessage)
                        # get the start number
                        start_a = int(line_ele[3])
                        abundance_list = [float(x) for x in line_ele[4:]]
                        a_list = [x + start_a for x in range(len(abundance_list))]
                        isotopes = []
                        for item in a_list:
                            tempiso = ''.join([ELE_TABLE[p - 1], str(item)])
                            isotopes.append(tempiso)
                        # treat the isotope that has 0.0 abundance
                        real_isotopes = []
                        real_abundance_list = []
                        for i in range(len(abundance_list)):
                            # this is a isotope with 0.0 abundance
                            if abundance_list[i] < 1e-6:
                                pass
                            else:
                                real_abundance_list.append(abundance_list[i])
                                real_isotopes.append(isotopes[i])
                        self._fispact_material_nuclide.extend(real_isotopes)
                        self._fispact_material_atom_kilogram.extend(
                            map(lambda x: x * scale / 100.0, real_abundance_list))
                fin.close()
