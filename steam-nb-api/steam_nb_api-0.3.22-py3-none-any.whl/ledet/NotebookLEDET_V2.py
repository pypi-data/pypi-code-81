import os
import copy
import numpy as np
import yaml
import subprocess
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from dataclasses import dataclass, asdict
from steam_nb_api.ledet.Solenoids import Solenoid
from steam_nb_api.ledet.Solenoids import Solenoid_magnet

from steam_nb_api.ledet.ParametersLEDET import ParametersLEDET
from steam_nb_api.ledet.Simulation import RunSimulations
from steam_nb_api.roxie_parser.geometricFunctions import close_pairs_ckdtree, close_pairs_pdist
import sys
import csv
from pathlib import Path
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.lines as lines

from steam_nb_api.ledet.ParametersLEDET import ParametersLEDET
from steam_nb_api.utils import misc
from steam_nb_api.roxie_parser import MagneticCoil
from steam_nb_api.utils.SelfMutualInductanceCalculation import SelfMutualInductanceCalculation

from steam_nb_api.roxie_parser import CableDatabase
from steam_nb_api.roxie_parser import ConductorPosition
from steam_nb_api.roxie_parser.geometricFunctions import close_pairs_ckdtree, close_pairs_pdist
from steam_nb_api.resources.ResourceReader import ResourceReader

@dataclass
class MagnetGeometry:
    xPos: np.ndarray = np.array([])
    yPos: np.ndarray = np.array([])
    iPos: np.ndarray = np.array([])
    xBarePos: np.ndarray = np.array([])
    yBarePos: np.ndarray = np.array([])
    xS: np.ndarray = np.array([])
    yS: np.ndarray = np.array([])
    iS: np.ndarray = np.array([])
    x: np.ndarray = np.array([])
    y: np.ndarray = np.array([])
    x_ave: np.ndarray = np.array([])
    y_ave: np.ndarray = np.array([])
    x_ave_group: np.ndarray = np.array([])
    y_ave_group: np.ndarray = np.array([])
@dataclass
class MagnetField:
    B: np.ndarray = np.array([])
    Bx: np.ndarray = np.array([])
    By: np.ndarray = np.array([])

def _read_yaml(type_str, elem_name):
    """
    Reads yaml file and returns it as dictionary
    :param type_str: type of file, e.g.: quench, coil, wire
    :param elem_name: file name, e.g. ColSol.1
    :return: dictionary for file named: type.name.yam
    """
    file_path = os.path.join('ledet', 'Inputs', f"{type_str}.{elem_name}.yaml")
    fullfileName = ResourceReader.getResourcePath(file_path)
    with open(fullfileName, 'r') as stream:
        data = yaml.safe_load(stream)
    return data

class Notebook_LEDET:
    def __init__(self, nameMagnet, typeMagnet = 'Cos-Theta', verbose = False, recalc_field=True, headerLines =1):
        self.AvailableConductor = ['Type2', 'W1']
        self.AvailableOptions = ['cos_theta', 'solenoid']
        self.AvailableTransients = ['FPA']
        self.AvailablePlotOptions = ['Default']
        self.AvailableVariables = ['Default']
        self.AvailableSimulations = ['2D', '2D+1D', '3D']

        self.supercon_dict = {'Nb-Ti': 1, "Nb3Sn(Summer's fit)": 2, "BSCCO2212": 3, "Nb3Sn(Bordini's fit)": 4}
        self.stabil_dict = {'Cu': 1, 'Ag': 2, 'SS': 3}
        self.insul_dict = {'G10': 1, 'Kapton': 2, 'Helium': 3, 'void': 4}

        # Intrinsic objects
        self.nameMagnet = nameMagnet
        print('Initializing ', nameMagnet)
        self.Magnet = ParametersLEDET()

        # miscellaneous
        self.verbose = verbose
        self.Magnet.Options.headerLines = headerLines
        self.selectedFont = {'fontname':'DejaVu Sans', 'size':14}
        self.text = {'x': [], 'y': [], 't': []}
        self.typeMagnet = typeMagnet

        if typeMagnet == 'solenoid':
            self.solenoid_data = _read_yaml('magnet', self.nameMagnet)
            self._setUp_Solenoid(recalc_field)

        # Start loading
        self.nStrands, self.polarities_inGroup, self.nHalfTurns, self.nTurns, self.nGroups, self.nCoilSections = 0, 0, 0, 0, 0, 0
        self.strandToGroup, self.strandToHalfTurn, self.halfTurnToTurn, self.strandToCoilSection, self.HalfTurnToCoilSection, self.HalfTurnToGroup\
            = np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([])
        [self.MagnetField, self.MagnetGeometry] = self._load_ROXIE()
        self.elPairs_GroupTogether = np.array([])

        if typeMagnet == 'solenoid':    # this can be only done after _load_ROXIE has been called.
            self.load_ConductorData(self.Solenoid.wires, self.Solenoid.wire_groups)
            max_distance = 0.5E-3
            self.set_ThermalConnections(max_distance)
            self.set_ElectricalOrder([0], [0])  # solenoid does not use any of the inputs, so it does not matter
            self.set_SimulationType('2D')
        # Further variables
        self.ConductorTypes = []
        self.ConductorGroups = np.array([])
        self.SimulationType = ''
        self.MPZ = np.array([])
        self.flag_Busbar = 0
        return

    def _setUp_Solenoid(self, recalc_field):
        self.Magnet.Options.flag_typeWindings = 1
        self.Solenoid = Solenoid_magnet(self.nameMagnet)
        self.Magnet.flagIron = self.solenoid_data['flagIron']
        self.Magnet.flagSelfField = self.solenoid_data['flagSelfField']
        field_map_file = os.path.join(os.getcwd(), f"{self.nameMagnet}_All_NoIron_NoSelfField.map2d")
        Ind_matrix_file = os.path.join(os.getcwd(), f"{self.nameMagnet}_selfMutualInductanceMatrix.csv")
        if recalc_field:
            if self.Magnet.flagIron == 1 or self.Magnet.flagSelfField == 1:
                raise Exception(
                    'Can not calculate magnetic field using soleno and account for self field or iron effect')
            else:
                self.Solenoid.save_B_map(field_map_file)
                self.Solenoid.save_L_M(Ind_matrix_file)
        self.Magnet.Inputs.I00 = self.solenoid_data['I']
        self.Magnet.Inputs.T00 = self.solenoid_data['T']  # [K]

        self.Magnet.Inputs.M_m = np.sum(np.loadtxt(Ind_matrix_file, delimiter=',', skiprows=1))
        if not isinstance(self.Magnet.Inputs.M_m, np.ndarray):
            self.Magnet.Inputs.M_m = np.array([self.Magnet.Inputs.M_m])
        self.Magnet.Inputs.M_InductanceBlock_m = np.array([0])

    def _load_ROXIE(self):
        # Select ROXIE .cadata file with conductor data
        currentDirectory = Path(os.path.split(os.getcwd())[0])
        fileNameCadata = os.path.join(currentDirectory, 'resources', 'roxie_parser', 'roxie.cadata')
        fileName = self.nameMagnet + '_All_WithIron_WithSelfField.map2d'
        fileNameData = self.nameMagnet + '_All_WithIron_WithSelfField.data'
        if self.typeMagnet == 'solenoid' and self.solenoid_data['flagIron']==0 and self.solenoid_data['flagSelfField']==0:
            fileName = self.nameMagnet + '_All_NoIron_NoSelfField.map2d'

        print('O - Loading field maps from: ', fileName)
        strandToGroup = np.array([])
        strandToHalfTurn = np.array([])
        idx = []
        x = []
        y = []
        Bx = []
        By = []
        Area = []
        I = []
        fillFactor = []

        # Read file
        file = open(fileName, "r")
        fileContent = file.read()
        # Separate rows
        fileContentByRow = fileContent.split("\n")

        for index in range(len(fileContentByRow) - 1):
            if index > self.Magnet.Options.headerLines:
                fc = fileContentByRow[index]
                row = fc.split()
                strandToGroup = np.hstack([strandToGroup, int(row[0])])
                strandToHalfTurn = np.hstack([strandToHalfTurn, int(row[1])])
                idx = np.hstack([idx, float(row[2])])
                x = np.hstack([x, float(row[3]) / 1000])  # in [m]
                y = np.hstack([y, float(row[4]) / 1000])  # in [m]
                Bx = np.hstack([Bx, float(row[5])])
                By = np.hstack([By, float(row[6])])
                Area = np.hstack([Area, float(row[7])])
                I = np.hstack([I, float(row[8])])
                fillFactor = np.hstack([fillFactor, float(row[9])])
        [_, c] = np.unique(strandToHalfTurn, return_index=True)
        [_, self.Magnet.Inputs.nT] = np.unique(strandToGroup[c], return_counts=True)
        self.Magnet.Inputs.nStrands_inGroup = np.gradient(c)[np.cumsum(self.Magnet.Inputs.nT)-1]

        nStrandsFieldMap = len(strandToGroup)
        if self.verbose: print('Total number of strands in the field-map from ROXIE = {}'.format(nStrandsFieldMap))

        # Calculate absolute magnetic field
        B = []
        for i in range(nStrandsFieldMap):
            B = np.hstack([B, (Bx[i] ** 2 + By[i] ** 2) ** .5])
        Bfield = MagnetField(B, Bx, By)
        if self.verbose: print('Peak magnetic field in the field-map from ROXIE = {} T'.format(np.max(B)))

        # Number of strands in each half-turn
        self.nStrands = len(strandToGroup)
        self.Magnet.Inputs.polarities_inGroup = np.sign(I[c])[np.cumsum(self.Magnet.Inputs.nT)-1]
        self.nGroups = int(np.max(strandToGroup))
        self.Magnet.Options.Iref = (sum(abs(I[c][np.cumsum(self.Magnet.Inputs.nT)-1]))/self.nGroups)*self.Magnet.Inputs.nStrands_inGroup[0]
        self.nHalfTurns = int(np.max(strandToHalfTurn))
        self.nTurns = int(self.nHalfTurns / 2)

        self.strandToGroup = np.int_(strandToGroup)
        self.strandToHalfTurn = np.int_(strandToHalfTurn)
        self.halfTurnToTurn = self.strandToHalfTurn
        #self.halfTurnToTurn = np.tile(np.arange(1, self.nTurns + 1), 2) - commented out as it is shorter than other

        # Average half-turn positions
        x_ave = []
        y_ave = []
        for ht in range(1, self.nHalfTurns + 1):
            x_ave = np.hstack([x_ave, np.mean(x[np.where(self.strandToHalfTurn == ht)])])
            y_ave = np.hstack([y_ave, np.mean(y[np.where(self.strandToHalfTurn == ht)])])

        # Average group positions
        x_ave_group = []
        y_ave_group = []
        for g in range(1, self.nGroups + 1):
            x_ave_group = np.hstack([x_ave_group, np.mean(x[np.where(self.strandToGroup == g)])])
            y_ave_group = np.hstack([y_ave_group, np.mean(y[np.where(self.strandToGroup == g)])])

        if self.verbose:
            print('Total number of strands = ' + str(self.nStrands))
            print('Total number of half-turns = ' + str(self.nHalfTurns))
            print('Total number of turns = ' + str(self.nTurns))
            print('Total number of groups = ' + str(self.nGroups))

        if self.typeMagnet == 'Cos-Theta':
            # Define the magnetic coil
            definedMagneticCoil = MagneticCoil.MagneticCoil()
            xPos, yPos, iPos, xBarePos, yBarePos, xS, yS, iS = \
                definedMagneticCoil.generateCoilGeometry(fileNameData, fileNameCadata, verbose = self.verbose)
            MagnetGeo = MagnetGeometry(xPos, yPos, iPos, xBarePos, yBarePos, xS, yS, iS, x, y, x_ave, y_ave, x_ave_group, y_ave_group)
        elif self.typeMagnet == 'solenoid':
            MagnetGeo = MagnetGeometry(0,0,0,0,0,0,0,0, x, y, x_ave, y_ave,x_ave_group, y_ave_group)

        print('X - Loading ROXIE was successful.')
        return [Bfield, MagnetGeo]

    def setAttribute(self, key, attribute):
        if key in self.Magnet.Inputs.__annotations__: key_class = 'Inputs'
        if key in self.Magnet.Options.__annotations__: key_class = 'Options'
        if key in self.Magnet.Plots.__annotations__: key_class = 'Plots'
        if key in self.Magnet.Variables.__annotations__: key_class = 'Variables'

        self.Magnet.setAttribute(key_class, key, attribute)

    def __translateDict(self, word):
        if word in self.supercon_dict.keys():
            return self.supercon_dict[word]
        if word in self.stabil_dict.keys():
            return self.stabil_dict[word]
        if word in self.insul_dict.keys():
            return self.insul_dict[word]

    def load_ConductorData(self, Conductor_L, Turns_L):
        if not isinstance(Conductor_L, list):
            Conductor_L = [Conductor_L]
        if not isinstance(Turns_L, np.ndarray):
            Turns_L = np.array(Turns_L)
        if len(Turns_L) != self.nGroups:
            print('The provided list has ', len(Turns_L),' but this magnet has ', self.nGroups,' groups. Abort.')
            return
        if np.max(np.array(Turns_L))!= len(Conductor_L):
            print('You are providing ', len(Conductor_L), '  conductor types, but only assign ',
                  np.max(np.array(Turns_L)), ' conductor. Please check!' )
            return

        for i in range(len(Conductor_L)):
            Conductor = Conductor_L[i]
            Group_Mask = np.where(Turns_L==i+1)[0]

            print('O - Loading Conductor data for Type: ', Conductor)
            if not Conductor in self.AvailableConductor:
                print('Conductor type: ',Conductor, ' not understood. Available conductor: ', self.AvailableConductor)
                return
            conductor_data = _read_yaml('conductor', Conductor)
            cable_data = conductor_data['cable']
            strand_data = conductor_data['strand']
            type = conductor_data['type']
            SC = list(strand_data['SC_type'].keys())[0]
            SC_data = strand_data['SC_type'][SC]

            Values = np.array([0.0]*self.nGroups)
            for key in cable_data.keys():
                if key in self.Magnet.Inputs.__annotations__:
                    try:
                        Values[Group_Mask] = float(cable_data[key])
                    except:
                        Values[Group_Mask] = self.__translateDict(cable_data[key])
                    self.Magnet.fillAttribute('Inputs', key, Values)
            for key in strand_data.keys():
                if key in self.Magnet.Inputs.__annotations__:
                    try:
                        Values[Group_Mask] = float(strand_data[key])
                    except:
                        Values[Group_Mask] = self.__translateDict(strand_data[key])
                    self.Magnet.fillAttribute('Inputs', key, Values)
            for key in SC_data.keys():
                if key in self.Magnet.Inputs.__annotations__:
                    try:
                        Values[Group_Mask] = float(SC_data[key])
                    except:
                        Values[Group_Mask] = self.__translateDict(SC_data[key])
                    self.Magnet.fillAttribute('Inputs', key, Values)
            Values = np.array([0.0] * self.nGroups)
            Values[Group_Mask] = self.__translateDict(SC)
            self.Magnet.fillAttribute('Inputs', 'SCtype_inGroup', Values)

            if type == 'rectangular':
                wire_area = (self.Magnet.Inputs.wBare_inGroup[Group_Mask] * self.Magnet.Inputs.hBare_inGroup[Group_Mask]) \
                            - ((4 - np.pi) * strand_data['scr_i'] ** 2)
                eq_diam = np.sqrt(wire_area * 4 / np.pi)  # equivalent diameter with correcting for the corner radius
            else:
                print('Conductor type: ', type, 'not supported.')
                eq_diam = np.zeros(len(Group_Mask))  # TODO other conductor types, like cables, round monolith wires
            Values = np.array([0.0] * self.nGroups)
            Values[Group_Mask] = eq_diam
            self.Magnet.fillAttribute('Inputs', 'ds_inGroup', Values)

            try:
                self.Magnet.Options.fScaling_Pex_AlongHeight = (2 * float(cable_data['insulationAroundCables'])) / (
                            2 * float(cable_data['insulationAroundCables']) + float(cable_data['insulationBetweenLayers']))
            except:
                self.Magnet.Options.fScaling_Pex_AlongHeight = 1
                pass
            try:
                if float(strand_data['T_Ref_RRR']) == 293:
                    self.Magnet.Inputs.RRR_Cu_inGroup[Group_Mask]  = self.Magnet.Inputs.RRR_Cu_inGroup[Group_Mask] / 1.086
            except:
                pass

            if len(self.Magnet.Inputs.Jc_Nb3Sn0_inGroup)==0:
                self.Magnet.fillAttribute('Inputs', 'Jc_Nb3Sn0_inGroup',np.array([0]* self.nGroups))
            if len(self.Magnet.Inputs.Bc2_Nb3Sn_inGroup)==0:
                self.Magnet.fillAttribute('Inputs', 'Bc2_Nb3Sn_inGroup',np.array([0]* self.nGroups))
            if len(self.Magnet.Inputs.Bc2_NbTi_ht_inGroup)==0:
                self.Magnet.fillAttribute('Inputs', 'Bc2_NbTi_ht_inGroup',np.array([0]* self.nGroups))
            if len(self.Magnet.Inputs.Tc0_Nb3Sn_inGroup)==0:
                self.Magnet.fillAttribute('Inputs', 'Tc0_Nb3Sn_inGroup',np.array([0]* self.nGroups))
            if len(self.Magnet.Inputs.c2_Ic_NbTi_inGroup)==0:
                self.Magnet.fillAttribute('Inputs', 'c2_Ic_NbTi_inGroup',np.array([0]* self.nGroups))
            if len(self.Magnet.Inputs.c1_Ic_NbTi_inGroup)==0:
                self.Magnet.fillAttribute('Inputs', 'c1_Ic_NbTi_inGroup',np.array([0]* self.nGroups))
            if len(self.Magnet.Inputs.Tc0_NbTi_ht_inGroup)==0:
                self.Magnet.fillAttribute('Inputs', 'Tc0_NbTi_ht_inGroup',np.array([0]* self.nGroups))

        if self.typeMagnet == 'solenoid':
            self.Magnet.Inputs.ds_inGroup = []
            self.Magnet.Inputs.nT = []
            self.Magnet.Inputs.l_mag_inGroup = []
            for block_name, block_dict in self.solenoid_data['blocks'].items():
                conductor_data = _read_yaml('conductor', block_dict['wire'])
                block_dict['wire'] = conductor_data
                sol = Solenoid(block_name, block_dict)
                n_groups_in_block = np.shape(sol.Rin)[0]
                wire_area = (conductor_data['strand']['wBare_inGroup'] * conductor_data['strand']['hBare_inGroup'])\
                            - ((4 - np.pi) * conductor_data['strand']['scr_i'] ** 2)
                eq_diam = np.sqrt(wire_area * 4 / np.pi)
                self.Magnet.Inputs.ds_inGroup = self.Magnet.Inputs.ds_inGroup + ((np.ones(n_groups_in_block) * eq_diam).tolist()) # equivalent diameter
                self.Magnet.Inputs.nT = self.Magnet.Inputs.nT + ((np.ones(n_groups_in_block, dtype=np.int32) * sol.n_turns_per_layer).tolist())  # Number of half-turns in each group
                self.Magnet.Inputs.l_mag_inGroup = self.Magnet.Inputs.l_mag_inGroup + ((2 * np.pi * (sol.Rin + sol.Rout) / 2).tolist())  # Length of turns of each layer
            self.Magnet.Inputs.nT = np.array(self.Magnet.Inputs.nT)
            self.Magnet.Inputs.ds_inGroup = np.array(self.Magnet.Inputs.ds_inGroup)
            self.Magnet.Inputs.l_mag_inGroup = np.array(self.Magnet.Inputs.l_mag_inGroup)

        self.ConductorTypes = Conductor_L
        self.ConductorGroups = Turns_L

        print('X - Loading Conductor data was successful.')
        if self.typeMagnet == 'Cos-Theta':
            print('O - Calculate Self-mutual inductance matrix.')
            self.__calculateSelfMutualInductance()
            print('X - Calculation was successful.')
        elif self.typeMagnet == 'solenoid':
            self.nGroups = len(self.Magnet.Inputs.ds_inGroup)
            self.Magnet.Inputs.GroupToCoilSection = self.nGroups * [1]
            self.nCoilSections = np.max(self.Magnet.Inputs.GroupToCoilSection)
            # Define to which inductive block each half-turn belongs
            self.Magnet.Inputs.HalfTurnToInductanceBlock = []
            for g in range(1, self.nGroups + 1):
                for j in range(self.Magnet.Inputs.nT[g - 1]):
                    self.Magnet.Inputs.HalfTurnToInductanceBlock.append(g)
        return

    def load_Options(self, *Type):
        if not Type:
            if self.typeMagnet == 'Cos-Theta': Type = 'cos_theta'
            elif self.typeMagnet == 'solenoid': Type = 'solenoid'
        else:
            Type = Type[0]
        print('O - Loading ', Type, 'options.')
        if not Type in self.AvailableOptions:
            print('Option type ', Type, ' currently not supported or not understood. '
                                        'Available options: ', self.AvailableOptions)
            return
        option_data = _read_yaml('options', Type)
        for key in option_data.keys():
            if key in self.Magnet.Options.__annotations__:
                Values = option_data[key]
                self.Magnet.setAttribute('Options', key, Values)
        print('X - Loading ', Type, 'options was successful.')

    def load_VariablesToStore(self, *Type):
        if not Type:
            Type = 'Default'
        else: Type = Type[0]
        print('O - Loading ', Type, ' storage options.')
        if not Type in self.AvailableVariables:
            print('Storage type ', Type, ' currently not supported or not understood '
                                        'Available options: ', self.AvailableVariables)
            return
        option_data = _read_yaml('store', Type)
        for key in option_data.keys():
            if key in self.Magnet.Variables.__annotations__:
                Values = option_data[key]
                self.Magnet.setAttribute('Variables', key, Values)
        print('X - Loading ', Type, 'variables to store was successful.')

    def load_PlotOptions(self, *Type):
        if not Type:
            Type = 'Default'
        else:
            Type = Type[0]
        print('O - Loading ', Type, ' plot options.')
        if not Type in self.AvailablePlotOptions:
            print('Plot-options type ', Type, ' currently not supported or not understood.'
                                         'Available plot-options: ', self.AvailablePlotOptions)
            return
        option_data = _read_yaml('plots', Type)
        for key in option_data.keys():
            if key in self.Magnet.Variables.__annotations__:
                Values = option_data[key]
                self.Magnet.setAttribute('Plots', key, Values)
        print('X - Loading ', Type, 'plot-options was successful.')

    def set_ElectricalOrder(self, elPairs_GroupTogether, elPairs_RevElOrder): #TODO  Solenoid does not use any of the inputs, so they can be anything as long as two inputs are given
        print('O - Attempting to set electrical order')
        # Start and end indices of each group
        indexTstop = np.cumsum(self.Magnet.Inputs.nT)
        indexTstop = indexTstop.tolist()
        indexTstart = [1]
        for i in range(len(self.Magnet.Inputs.nT) - 1):
            indexTstart.extend([indexTstart[i] + self.Magnet.Inputs.nT[i]])

        if self.verbose:
            print('The half-turns of these pairs of groups will be connected electrically:')
            print(elPairs_GroupTogether)

        if self.typeMagnet != 'solenoid':
            if len(elPairs_RevElOrder) != len(elPairs_GroupTogether):
                raise Exception('Length of the vector elPairs_RevElOrder ({}) must be equal to nElPairs={}.'.format(
                    len(elPairs_RevElOrder), len(elPairs_GroupTogether)))

        el_order_half_turns = []
        if self.typeMagnet != 'solenoid':
            for p in range(len(elPairs_GroupTogether)):
                if self.Magnet.Inputs.nT[elPairs_GroupTogether[p][0] - 1] != self.Magnet.Inputs.nT[elPairs_GroupTogether[p][1] - 1]:
                    raise Exception(
                        'Pair of groups defined by the variable elPairs_GroupTogether must have the same number of half-turns.')
                for k in range(self.Magnet.Inputs.nT[elPairs_GroupTogether[p][0] - 1]):
                    if elPairs_RevElOrder[p] == 0:
                        el_order_half_turns.append(indexTstart[elPairs_GroupTogether[p][0] - 1] + k)
                        el_order_half_turns.append(indexTstart[elPairs_GroupTogether[p][1] - 1] + k)
                    if elPairs_RevElOrder[p] == 1:
                        el_order_half_turns.append(indexTstop[elPairs_GroupTogether[p][0] - 1] - k)
                        el_order_half_turns.append(indexTstop[elPairs_GroupTogether[p][1] - 1] - k)
        else:
            self.nGroupsDefined = len(self.Magnet.Inputs.nT)
            winding_order_groups = (self.nGroupsDefined * [0, 1])[
                                   :self.nGroupsDefined]
            for p in range(self.nGroupsDefined, 0, -1):
                for k in range(self.Magnet.Inputs.nT[p - 1]):
                    if winding_order_groups[p - 1] == 0:
                        el_order_half_turns.append(indexTstart[p - 1] + k)
                    if winding_order_groups[p - 1] == 1:
                        el_order_half_turns.append(indexTstop[p - 1] - k)

        self.elPairs_GroupTogether = np.array(elPairs_GroupTogether)
        self.Magnet.Inputs.el_order_half_turns = np.array(el_order_half_turns)
        print('X - Setting electrical order was successful.')

    def set_ThermalConnections(self, max_distance):
        print('O - Attempting to set thermal connections')
        # Start and end indices of each group
        indexTstop = np.cumsum(self.Magnet.Inputs.nT)
        indexTstop = indexTstop.tolist()
        indexTstart = [1]
        for i in range(len(self.Magnet.Inputs.nT) - 1):
            indexTstart.extend([indexTstart[i] + self.Magnet.Inputs.nT[i]])

        iContactAlongWidth_From = []
        iContactAlongWidth_To = []

        for g in range(self.nGroups):
            iContactAlongWidth_From.extend(range(indexTstart[g], indexTstop[g]))
            iContactAlongWidth_To.extend(range(indexTstart[g] + 1, indexTstop[g] + 1))

        if len(iContactAlongWidth_From)<1:
            iContactAlongWidth_From.append(1)
            iContactAlongWidth_To.append(1)

        self.Magnet.Inputs.iContactAlongWidth_From = np.array(iContactAlongWidth_From)
        self.Magnet.Inputs.iContactAlongWidth_To = np.array(iContactAlongWidth_To)

        if self.verbose:
            print('Heat exchange along the cable wide side - Calculated indices:')
            print('iContactAlongWidth_From = ')
            print(iContactAlongWidth_From)
            print('iContactAlongWidth_To = ')
            print(iContactAlongWidth_To)

        # Prepare input for the function close_pairs_ckdtree
        X = np.column_stack((self.MagnetGeometry.x, self.MagnetGeometry.y))

        # find all pairs of strands closer than a distance of max_d
        pairs_close = close_pairs_ckdtree(X, max_distance)

        # find pairs that belong to half-turns located in different groups
        contact_pairs = set([])
        for p in pairs_close:
            if not self.strandToGroup[p[0]] == self.strandToGroup[p[1]]:
                contact_pairs.add((self.strandToHalfTurn[p[0]], self.strandToHalfTurn[p[1]]))

        # assign the pair values to two distinct vectors
        iContactAlongHeight_From = []
        iContactAlongHeight_To = []
        for p in contact_pairs:
            iContactAlongHeight_From.append(p[0])
            iContactAlongHeight_To.append(p[1])
        # Keep arrays Non-empty
        if len(iContactAlongHeight_From)<1:
            iContactAlongHeight_From.append(1)
            iContactAlongHeight_To.append(1)

        # find indices to order the vector iContactAlongHeight_From
        idxSort = [i for (v, i) in sorted((v, i) for (i, v) in enumerate(iContactAlongHeight_From))]

        # reorder both iContactAlongHeight_From and iContactAlongHeight_To using the indices
        self.Magnet.Inputs.iContactAlongHeight_From = np.array([iContactAlongHeight_From[i] for i in idxSort])
        self.Magnet.Inputs.iContactAlongHeight_To = np.array([iContactAlongHeight_To[i] for i in idxSort])

        if self.verbose:
            print('Heat exchange along the cable narrow side - Calculated indices:')
            print('iContactAlongHeight_From = ')
            print(self.Magnet.Inputs.iContactAlongHeight_From)
            print('iContactAlongWidth_To = ')
            print(self.Magnet.Inputs.iContactAlongHeight_To)
        print('X - Thermal connections are set.')

    def set_SimulationType(self, Scenario):
        print('O - Prepare simulation as:', Scenario)
        if Scenario == '2D+1D':
            self.Magnet.Inputs.iStartQuench = np.linspace(1,self.nHalfTurns, self.nHalfTurns)
            self.Magnet.Inputs.tStartQuench = np.ones((self.nHalfTurns,))*9999
            self.Magnet.Inputs.lengthHotSpot_iStartQuench = np.ones((self.nHalfTurns,))*0.01
            [_, self.MPZ, _, _, _, _] = self.Magnet.adjust_vQ(os.getcwd(), Return=1)
        elif Scenario == '2D':
            self.Magnet.Inputs.iStartQuench = np.array([1])
            self.Magnet.Inputs.tStartQuench = np.array([9999])
            self.Magnet.Inputs.lengthHotSpot_iStartQuench = np.array([0])
            self.Magnet.Inputs.vQ_iStartQuench = np.array([0])
        elif Scenario == '3D':
            print('To be implemented.')
        else:
            print('Scenario ', Scenario, ' currently not supported or not understood.'
                                         ' Available Simulation types: ', self.AvailableSimulations)
            return
        self.SimulationType = Scenario
        print('X - Scenario prepared.')

    def initiateQuench(self, Turn, TimeOfQuench, lengthHotspot = 0):
        print('O - Attempting to initiate quench.')
        if not isinstance(TimeOfQuench, list):
            TimeOfQuench = [TimeOfQuench]
        if not isinstance(Turn, list):
            Turn = [Turn]
        if lengthHotspot != 0 and not isinstance(lengthHotspot, list):
            lengthHotspot = [lengthHotspot]
        if len(TimeOfQuench) != len(Turn):
            print('You provided different number of times and turns. Abort')
            return
        if lengthHotspot != 0 and len(lengthHotspot) != len(Turn):
            print('You provided different number of turns and lengths. Abort')
            return

        if self.SimulationType == '2D+1D':
            for i in range(len(Turn)):
                self.Magnet.Inputs.tStartQuench[Turn[i]-1] = TimeOfQuench[i]
                if lengthHotspot != 0:
                    self.Magnet.Inputs.lengthHotSpot_iStartQuench[Turn[i]-1] = lengthHotspot[i]
                else:
                    self.Magnet.Inputs.lengthHotSpot_iStartQuench[Turn[i]-1] = self.MPZ[i]
        elif self.SimulationType == '2D':
            for i in range(len(Turn)):
                if i==0:
                    self.Magnet.Inputs.iStartQuench[i] = Turn[i]
                    self.Magnet.Inputs.tStartQuench[i] = TimeOfQuench[i]
                    self.Magnet.Inputs.lengthHotSpot_iStartQuench[i] = self.Magnet.Inputs.l_magnet
                    self.Magnet.Inputs.vQ_iStartQuench[i] = 0
                else:
                    self.Magnet.Inputs.tStartQuench = np.append(self.Magnet.Inputs.tStartQuench, TimeOfQuench[i])
                    self.Magnet.Inputs.iStartQuench = np.append(self.Magnet.Inputs.iStartQuench, Turn[i])
                    self.Magnet.Inputs.vQ_iStartQuench = np.append(self.Magnet.Inputs.vQ_iStartQuench, 0)
                    self.Magnet.Inputs.lengthHotSpot_iStartQuench = \
                        np.append(self.Magnet.Inputs.lengthHotSpot_iStartQuench, self.Magnet.Inputs.l_magnet)
            if lengthHotspot != 0:
                print('Simulation is set to 2D. Provided hot-spot length will be ignored.')
        elif self.SimulationType =='3D':
            print('To be implemented')
        else:
            print('Please first specify simulation type: set_SimulationType(Type)')
            return
        print('X - Quenches successfully initiated.')

    def setHeliumFraction(self, PercentVoids):
        print('O - Trying to set Helium fraction in conductor voids')
        if np.max(self.Magnet.Inputs.nStrands_inGroup)==1:
            print('You are about to set a helium-fraction for a single-stranded wire!')

        cs_bare = self.Magnet.Inputs.wBare_inGroup*self.Magnet.Inputs.hBare_inGroup
        cs_ins = (self.Magnet.Inputs.wBare_inGroup +2*self.Magnet.Inputs.wIns_inGroup)* \
                (self.Magnet.Inputs.hBare_inGroup +2*self.Magnet.Inputs.hIns_inGroup)
        cs_strand = self.Magnet.Inputs.nStrands_inGroup*np.pi*(self.Magnet.Inputs.ds_inGroup**2)/4
        strand_total = cs_strand/cs_ins
        ins_total = (cs_ins - cs_bare)/cs_ins
        VoidRatio = (cs_bare - cs_strand)/cs_ins
        extVoids = VoidRatio - (PercentVoids/100.0)
        if any(sV < 0 for sV in extVoids):
            print("Negative externalVoids calculated. Abort, please check.")
            return
        self.Magnet.Inputs.overwrite_f_externalVoids_inGroup = extVoids
        self.Magnet.Inputs.overwrite_f_internalVoids_inGroup = np.ones((self.nGroups,)).transpose()*(PercentVoids/100.0)
        print('X - Helium fraction successfully set.')

    def includeBusbar(self, BusbarLength, InductanceGuessPerLength = 0.5E-6):
        print('O - Including busbar inductance.')
        L_busbar = BusbarLength*InductanceGuessPerLength
        M_m = np.sum(np.sum(self.Magnet.Inputs.M_m))/(self.Magnet.Inputs.M_m.shape[0]*self.Magnet.Inputs.M_m.shape[1])
        idx_fL = np.argmin(abs(self.Magnet.Inputs.fL_I - self.Magnet.Inputs.I00))
        fL_L = self.Magnet.Inputs.fL_L[idx_fL]
        LEDET_lengthBusbar = L_busbar / (M_m *fL_L)
        self.Magnet.Inputs.l_magnet = self.Magnet.Inputs.l_magnet+LEDET_lengthBusbar
        self.flag_Busbar = 1
        print('X - ',BusbarLength,' m of busbar as additional inductance included.')

    def __calculateSelfMutualInductance(self):
        # Self-mutual inductance calculation, using SMIC (https://cernbox.cern.ch/index.php/s/37F87v3oeI2Gkp3)
        flag_strandCorrection = 0
        flag_sumTurnToTurn = 1
        flag_writeOutput = 0

        # Calculate group to which each half-turn belongs
        indexTstart = np.hstack([1, 1 + np.cumsum(self.Magnet.Inputs.nT[:-1])])
        indexTstop = np.cumsum(self.Magnet.Inputs.nT)
        HalfTurnToGroup = np.zeros((1, self.nHalfTurns), dtype=int)
        HalfTurnToGroup = HalfTurnToGroup[0]
        HalfTurnToCoilSection = np.zeros((1, self.nHalfTurns), dtype=int)
        HalfTurnToCoilSection = HalfTurnToCoilSection[0]
        for g in range(1, self.nGroups + 1):
            HalfTurnToGroup[indexTstart[g - 1] - 1:indexTstop[g - 1]] = g
            HalfTurnToCoilSection[indexTstart[g - 1] - 1:indexTstop[g - 1]] = self.Magnet.Inputs.GroupToCoilSection[g - 1]

        # Calculate group to which each strand belongs
        nS = np.repeat(self.Magnet.Inputs.nStrands_inGroup, self.Magnet.Inputs.nT)
        indexSstart = np.hstack([1, 1 + np.cumsum(nS[:-1])]).astype(int)
        indexSstop = np.cumsum(nS).astype(int)
        strandToGroup = np.zeros((1, self.nStrands), dtype=int)
        strandToGroup = strandToGroup[0]
        strandToCoilSection = np.zeros((1, self.nStrands), dtype=int)
        strandToCoilSection = strandToCoilSection[0]
        for ht in range(1, self.nHalfTurns + 1):
            strandToGroup[indexSstart[ht - 1] - 1:indexSstop[ht - 1]] = HalfTurnToGroup[ht - 1]
            strandToCoilSection[indexSstart[ht - 1] - 1:indexSstop[ht - 1]] = HalfTurnToCoilSection[ht - 1]

        polarities = np.repeat(self.Magnet.Inputs.polarities_inGroup, self.Magnet.Inputs.nT)
        polarities = np.repeat(polarities, nS.astype(int))
        for i in range(2):
            # Calculate diameter of each strand
            Ds = np.zeros((1, self.nStrands), dtype=float)
            Ds = Ds[0]
            for g in range(1, self.nGroups + 1):
                if i == 0: Ds[np.where(strandToGroup == g)] = self.Magnet.Inputs.ds_inGroup[g - 1]
                if i == 1: Ds[np.where(strandToGroup == g)] = self.Magnet.Inputs.hBare_inGroup[g - 1]

            # Define self-mutual inductance calculation object
            coil = SelfMutualInductanceCalculation(self.MagnetGeometry.x, self.MagnetGeometry.y, polarities,
                                                   nS, Ds, self.strandToHalfTurn, strandToCoilSection,
                                                   flag_strandCorrection, flag_sumTurnToTurn, flag_writeOutput,
                                                   self.nameMagnet)

            # Calculate self-mutual inductance between half-turns, turns, and coil-sections, per unit length [H/m]
            M_halfTurns_calculated, M_turns_calculated, M_coilSections_calculated, L_mag0_calculated = \
                coil.calculateInductance(self.MagnetGeometry.x, self.MagnetGeometry.y, polarities,
                                         nS, Ds, self.strandToHalfTurn, strandToCoilSection,
                                         flag_strandCorrection=0)

            L_turns = M_turns_calculated
            L_turns_diag = np.diagonal(L_turns)
            L_turns_diag_rep = np.tile(L_turns_diag, (len(L_turns),
                                                      1))  # this replicates the effect of L_xx[i][i]
            denom_turns = np.sqrt(L_turns_diag_rep.T * L_turns_diag_rep)
            k_turns = L_turns / denom_turns  # matrix alt to k_turns[i][j]=L_turns[i][j]/np.sqrt(L_turns[j][j]*L_turns[i][i])

            if len(k_turns[np.where(k_turns > 1)]) == 0:
                break
            else:
                assert max(self.Magnet.Inputs.nStrands_inGroup) == 1, 'Wires are not single stranded but k>1'
                print('Mutual inductance of some turns is k>1, re-calculate with hBare.')

        self.strandToCoilSection = strandToCoilSection
        self.HalfTurnToCoilSection = HalfTurnToCoilSection
        self.HalfTurnToGroup = HalfTurnToGroup

        # Self-mutual inductances between coil sections, per unit length [H/m]
        self.Magnet.Inputs.M_m = M_coilSections_calculated
        # Self-mutual inductances between turns, per unit length [H/m]
        self.Magnet.Inputs.M_InductanceBlock_m = M_turns_calculated
        # Total magnet self-mutual inductance, per unit length [H/m]
        L_mag0 = L_mag0_calculated

        # Defining to which inductive block each half-turn belongs
        self.Magnet.Inputs.HalfTurnToInductanceBlock = np.concatenate((np.linspace(1, int(self.nHalfTurns / 2 ), int(self.nHalfTurns/2)),
                                                       np.linspace(1, int(self.nHalfTurns / 2 ), int(self.nHalfTurns/2))))

        if self.verbose:
            print('')
            print('Total magnet self-inductance per unit length: ' + str(L_mag0) + ' H/m')

        # Check if Self-mutual inductance is too large
        if self.Magnet.Inputs.M_InductanceBlock_m.shape[0] >= 50:
            if self.verbose: print('Write Inductance matrix to csv')
            with open(self.nameMagnet + '_selfMutualInductanceMatrix.csv', 'w') as file:
                reader = csv.writer(file)
                reader.writerow(["Extended self mutual inductance matrix [H/m]"])
                for i in range(self.Magnet.Inputs.M_InductanceBlock_m.shape[0]):
                    reader.writerow(self.Magnet.Inputs.M_InductanceBlock_m[i])
            self.Magnet.Inputs.M_InductanceBlock_m = np.array([0])

    def set_QuenchHeater(self, nHalfQuadrants, iQH_toHalfTurn_From_oneHalfQuadrant, iQH_toHalfTurn_To_oneHalfQuadrant):
        idxHQ = int(self.nGroups/nHalfQuadrants)
        nHalfTurnsinHQ = sum(self.Magnet.Inputs.nT[:idxHQ])

        # Automatically extend to the other half-quadrants
        iQH_toHalfTurn_To = []
        iQH_toHalfTurn_From = []
        for i in range(0, nHalfQuadrants):
            iQH_tempVector_To = list(np.asarray(iQH_toHalfTurn_To_oneHalfQuadrant) + i * nHalfTurnsinHQ)
            iQH_toHalfTurn_To.extend(iQH_tempVector_To)

            iQH_tempVector_From = list(np.asarray(iQH_toHalfTurn_From_oneHalfQuadrant) + i)
            iQH_toHalfTurn_From.extend(iQH_tempVector_From)
        self.Magnet.Inputs.iQH_toHalfTurn_From = np.array(iQH_toHalfTurn_From)
        self.Magnet.Inputs.iQH_toHalfTurn_To = np.array(iQH_toHalfTurn_To)

        rhoSS = 5.00E-07 * 1.09  # in [Ohm m]
        R_cold_QH = rhoSS/(self.Magnet.Inputs.w_QH * self.Magnet.Inputs.h_QH) * self.Magnet.Inputs.l_QH * self.Magnet.Inputs.f_QH
        R_total_QH =  R_cold_QH + self.Magnet.Inputs.R_warm_QH
        I0_QH = self.Magnet.Inputs.U0_QH / R_total_QH
        tau_QH = R_total_QH * self.Magnet.Inputs.C_QH

        if self.verbose:
            print('I0_QH={}'.format(I0_QH))
            print('tau_QH={}'.format(tau_QH))

    def storeVariables(self, locals):
        print('O - Storing variables.')
        self.nCoilSections = np.max(self.Magnet.Inputs.GroupToCoilSection)
        if self.typeMagnet == 'solenoid':
            self.Magnet.Options.flag_typeWindings = 1
            self.Magnet.Inputs.l_magnet = 1
        else:
            self.Magnet.Inputs.l_mag_inGroup = np.ones((self.nGroups,)) * locals['l_magnet']
            if self.flag_Busbar:
                locals['l_magnet'] = self.Magnet.Inputs.l_magnet
        self.Magnet.localsParser(locals)

        if 'iQH_toHalfTurn_From_oneHalfQuadrant' in locals.keys():
            self.set_QuenchHeater(locals['nHalfQuadrants'], locals['iQH_toHalfTurn_From_oneHalfQuadrant'],
                                  locals['iQH_toHalfTurn_To_oneHalfQuadrant'])

        if len(self.Magnet.Inputs.initialQuenchTemp) < self.nCoilSections:
            self.Magnet.Inputs.initialQuenchTemp = np.repeat(self.Magnet.Inputs.initialQuenchTemp, self.nCoilSections)
        if len(self.Magnet.Inputs.tQuench) < self.nCoilSections:
            self.Magnet.Inputs.tQuench = np.repeat(self.Magnet.Inputs.tQuench, self.nCoilSections)

        ## Deduce Transient
        if locals['Transient'] == 'FPA':
            # LUT controlling power supply, Time [s]
            self.Magnet.Inputs.t_PC_LUT = [locals['tStart'], locals['t_PC'], locals['t_PC'] + 0.01]
            # LUT controlling power supply, Current [A]
            self.Magnet.Inputs.I_PC_LUT = [self.Magnet.Inputs.I00, self.Magnet.Inputs.I00, 0]
        else:
            print('Transient type ', locals['Transient'], ' currently not supported or not understood.')
        print('X - Variables successfully loaded.')

    def _solenoid_locals(self):
        scenario_data = _read_yaml('scenario', self.nameMagnet)
        circuit_data = _read_yaml('circuit', scenario_data['circuit'])
        protection_data = _read_yaml('protection', scenario_data['protection'])

        R_EE_triggered = (protection_data['U_EE'] - self.solenoid_data['I'] * (
                circuit_data['R_circuit'] + circuit_data['R_crowbar']) - circuit_data['Ud_crowbar']) / self.solenoid_data['I']  # Resistance of the energy-extraction system [Ohm]
        if R_EE_triggered < 0:
            R_EE_triggered = 0
        time_v_array = [item for sublist in [[rng['start'], rng['step'], rng['stop']] for rng in
                        scenario_data['simul_time']] for item in sublist]
        dict_block = {
        'R_EE_triggered': R_EE_triggered,
        'alphasDEG': self.nHalfTurns * [0],
        'rotation_block': self.nHalfTurns * [0],
        'mirror_block': self.nHalfTurns * [0],
        'mirrorY_block': self.nHalfTurns * [0],
        'initialQuenchTemp': 10,
        'tCLIQ': 99999,                  # Time when the CLIQ system is triggered [s]
        'directionCurrentCLIQ': [1],    # Direction of the introduced current change for the chosen CLIQ configuration
        'nCLIQ': 0,                     # Number of CLIQ units
        'U0': 0,                        # CLIQ charging voltage [V]
        'C': 0,                         # Capacitance of the CLIQ capacitor bank [F]
        'Rcapa': 0,                      # Resistance of the CLIQ leads [Ohm]
        'fL_I': [0, 1000],
        'fL_L': [1, 1],
        'tQuench': scenario_data['tStartQuench'],
        'tStart': time_v_array[0],
        'time_vector_params': time_v_array
        }
        return {**circuit_data, **protection_data, **dict_block}

    def writeLEDETFile(self, nameFileLEDET, locals):
        if self.typeMagnet == 'solenoid':
            locals = {**locals, **self._solenoid_locals()}
        self.storeVariables(locals)
        # Set flags depending on content:
        if len(self.ConductorTypes)>1 and self.Magnet.Options.flag_hotSpotTemperatureInEachGroup != 1:
            print('Multiple conductor types. Let me activate hot-spot temperatures in each group.')
            self.Magnet.Options.flag_hotSpotTemperatureInEachGroup = 1
        else:
            self.Magnet.Options.flag_hotSpotTemperatureInEachGroup = 0

        if np.max(self.Magnet.Inputs.nStrands_inGroup)==1 and self.Magnet.Options.flag_ISCL != 0:
            self.Magnet.Options.flag_ISCL = 0
            print('Single-stranded magnet. I set flag_ISCL to zero.')

        self.Magnet.writeFileLEDET(nameFileLEDET)

    ## Plotting part
    def plotter(self, data, titles, labels, types, texts, size=()):
        """
        Default plotter for most standard and simple cases
        """
        if not size:
            size = (len(data)*6,4)
        fig, axs = plt.subplots(nrows=1, ncols=len(data), figsize=size)
        if len(data) == 1:
            axs = [axs]
        for ax, ty, d, ti, l, te in zip(axs, types, data, titles, labels, texts):
            if ty == 'scatter':
                plot = ax.scatter(d['x'], d['y'], s=2, c=d['z'], cmap='jet')
                if len(te["t"]) != 0:
                    for x, y, z in zip(te["x"], te["y"], te["t"]):
                        ax.text(x, y, z)
            elif ty == 'plot':
                pass  # TODO make non scatter plots work. Some of non-scater plots are quite specific. Might be better off with a separate plotter
            ax.set_xlabel(l["x"], **self.selectedFont)
            ax.set_ylabel(l["y"], **self.selectedFont)
            ax.set_title(f'{ti}', **self.selectedFont)
            if ax.get_data_ratio()>1:
                ax.set_aspect(1. / ax.get_data_ratio())
            else:
                ax.set_aspect('equal')
            cbar = fig.colorbar(plot, ax=ax)
            if len(l["z"]) != 0:
                cbar.set_label(l["z"], **self.selectedFont)

        plt.tight_layout()
        plt.show()

    def plot_Conductors(self):
        """
        Plot conductor types for magnet
        """
        ConductorGroups = np.repeat(self.ConductorGroups, self.Magnet.Inputs.nT.astype(int))
        nStrands = np.repeat(self.Magnet.Inputs.nStrands_inGroup, self.Magnet.Inputs.nT.astype(int))
        ConductorGroups = np.repeat(ConductorGroups, nStrands.astype(int))
        data = [{'x': self.MagnetGeometry.x, 'y': self.MagnetGeometry.y, 'z': ConductorGroups}]
        titles = ['Conductor Type']
        labels = [{'x': "x (m)", 'y': "y (m)", 'z': ""}] * len(data)
        types = ['scatter'] * len(data)
        texts = [self.text] * len(data)
        self.plotter(data, titles, labels, types, texts)

    def plot_field(self):
        """
        Plot magnetic field components of a coil
        """
        I = np.repeat(self.Magnet.Inputs.polarities_inGroup, self.Magnet.Inputs.nT)
        nS = np.repeat(self.Magnet.Inputs.nStrands_inGroup, self.Magnet.Inputs.nT)
        I = np.repeat(I, nS.astype(int)) *self.Magnet.Inputs.I00

        data = [{'x': self.MagnetGeometry.x, 'y': self.MagnetGeometry.y, 'z': I},
                {'x': self.MagnetGeometry.x, 'y': self.MagnetGeometry.y, 'z': self.MagnetField.Bx},
                {'x': self.MagnetGeometry.x, 'y': self.MagnetGeometry.y, 'z': self.MagnetField.By},
                {'x': self.MagnetGeometry.x, 'y': self.MagnetGeometry.y, 'z': self.MagnetField.B}]
        titles = ['Current [A]', 'By [T]', 'Bz [T]', 'Bmod [T]']
        labels = [{'x': "x (m)", 'y': "y (m)", 'z': ""}] * len(data)
        types = ['scatter'] * len(data)
        texts = [self.text] * len(data)
        self.plotter(data, titles, labels, types, texts)

    def plot_strands_groups_layers(self):
        types = ['scatter'] * 4
        data = [{'x': self.MagnetGeometry.x, 'y': self.MagnetGeometry.y, 'z': self.strandToHalfTurn},
                {'x': self.MagnetGeometry.x, 'y': self.MagnetGeometry.y, 'z': self.strandToGroup},
                {'x': self.MagnetGeometry.x_ave, 'y': self.MagnetGeometry.y_ave, 'z': self.halfTurnToTurn},
                {'x': self.MagnetGeometry.x_ave, 'y': self.MagnetGeometry.y_ave, 'z': np.repeat(self.Magnet.Inputs.nStrands_inGroup, self.Magnet.Inputs.nT)}]
        titles = ['strandToHalfTurn', 'strandToGroup', 'halfTurnToTurn', 'Number of strands per half-turn']
        labels = [{'x': "r (m)", 'y': "z (m)", 'z': "Half-turn [-]"},
                  {'x': "r (m)", 'y': "z (m)", 'z': "Group [-]"},
                  {'x': "r (m)", 'y': "z (m)", 'z': "Turn [-]"},
                  {'x': "r (m)", 'y': "z (m)", 'z': "Number of  strands per cable [-]"}]
        t_ht = copy.deepcopy(self.text)
        for ht in range(self.nHalfTurns):
            t_ht['x'].append(self.MagnetGeometry.x_ave[ht])
            t_ht['y'].append(self.MagnetGeometry.y_ave[ht])
            t_ht['t'].append('{}'.format(ht + 1))
        t_ng = copy.deepcopy(self.text)
        for g in range(self.nGroups):
            t_ng['x'].append(self.MagnetGeometry.x_ave_group[g])
            t_ng['y'].append(self.MagnetGeometry.y_ave_group[g])
            t_ng['t'].append('{}'.format(g + 1))
        texts = [t_ht, t_ng, self.text, self.text]
        self.plotter(data, titles, labels, types, texts)

    def plot_polarities(self):
        polarities_inStrand = np.zeros((1, self.nStrands), dtype=int)
        polarities_inStrand = polarities_inStrand[0]
        for g in range(1, self.nGroups+ 1):
            polarities_inStrand[np.where(self.strandToGroup == g)] = self.Magnet.Inputs.polarities_inGroup[g - 1]
        data = [{'x': self.MagnetGeometry.x, 'y': self.MagnetGeometry.y, 'z': polarities_inStrand}]
        titles = ['Current polarities']
        labels = [{'x': "r (m)", 'y': "z (m)", 'z': "Polarity [-]"}]
        types = ['scatter'] * len(data)
        texts = [self.text] * len(data)
        self.plotter(data, titles, labels, types, texts)

    def plot_half_turns(self):
        data = [{'x': self.MagnetGeometry.x_ave, 'y': self.MagnetGeometry.y_ave, 'z': self.HalfTurnToGroup},
                {'x': self.MagnetGeometry.x_ave, 'y': self.MagnetGeometry.y_ave, 'z': self.HalfTurnToCoilSection},
                {'x': self.MagnetGeometry.x, 'y': self.MagnetGeometry.y, 'z': self.strandToGroup},
                {'x': self.MagnetGeometry.x, 'y': self.MagnetGeometry.y, 'z': self.strandToCoilSection}]
        titles = ['HalfTurnToGroup', 'HalfTurnToCoilSection', 'StrandToGroup', 'StrandToCoilSection']
        labels = [{'x': "r (m)", 'y': "z (m)", 'z': "Group [-]"},
                  {'x': "r (m)", 'y': "z (m)", 'z': "Coil section [-]"},
                  {'x': "r (m)", 'y': "z (m)", 'z': "Group [-]"},
                  {'x': "r (m)", 'y': "z (m)", 'z': "Coil Section [-]"}]
        types = ['scatter'] * len(data)
        texts = [self.text] * len(data)
        self.plotter(data, titles, labels, types, texts)

    def plot_nonlin_induct(self):
        f = plt.figure(figsize=(7.5, 5))
        plt.plot(self.Magnet.Inputs.fL_I, self.Magnet.Inputs.fL_L, 'ro-')
        plt.xlabel('Current [A]', **self.selectedFont)
        plt.ylabel('Factor scaling nominal inductance [-]', **self.selectedFont)
        plt.title('Differential inductance versus current', **self.selectedFont)
        plt.xlim([0, self.Magnet.Inputs.I00 * 2])
        plt.grid(True)
        plt.rcParams.update({'font.size': 12})
        plt.show()

    def plot_psu_and_trig(self):
        # Plot
        f = plt.figure(figsize=(7.5, 5))
        plt.plot([self.Magnet.Inputs.t_PC, self.Magnet.Inputs.t_PC], [0, 1], 'k--', linewidth=4.0, label='t_PC')
        plt.plot([self.Magnet.Inputs.tEE, self.Magnet.Inputs.tEE], [0, 1], 'r--', linewidth=4.0, label='t_EE')
        plt.plot([self.Magnet.Inputs.tCLIQ, self.Magnet.Inputs.tCLIQ], [0, 1], 'g--', linewidth=4.0, label='t_CLIQ')
        plt.plot([np.min(self.Magnet.Inputs.tQH), np.min(self.Magnet.Inputs.tQH)], [0, 1], 'b:', linewidth=2.0, label='t_QH')
        plt.xlabel('Time [s]', **self.selectedFont)
        plt.ylabel('Trigger [-]', **self.selectedFont)
        plt.xlim([1E-4, self.Magnet.Options.time_vector_params[-1]])
        plt.title('Power suppply and quench protection triggers', **self.selectedFont)
        plt.grid(True)
        plt.rcParams.update({'font.size': 12})
        plt.legend(loc='best')
        plt.tight_layout()
        plt.show()

    def plot_quench_prop_and_resist(self):
        if self.SimulationType=='2D+1D':
            # Calculate resistance of each turn at T=10 K
            rho_Cu_10K = 1.7E-10  # [Ohm*m] Approximate Cu resistivity at T=10 K, B=0, for RRR=100
            rho_Cu_10K_B = 4E-11  # [Ohm*m/T] Approximate Cu magneto-resistivity factor
            rho_ht_10K = []
            r_el_ht_10K = []
            tQuenchDetection = []
            mean_B_ht = []
            Iref = self.Magnet.Options.Iref
            nStrands_inGroup = self.Magnet.Inputs.nStrands_inGroup
            ds_inGroup = self.Magnet.Inputs.ds_inGroup
            f_SC_strand_inGroup = self.Magnet.Inputs.f_SC_strand_inGroup
            uQuenchDetectionThreshold = 0.1

            [vQ, l, th_con_h, delta_t_h, th_con_w, delta_t_w] = self.Magnet.adjust_vQ(os.getcwd(), Return =1)
            vQ_iStartQuench = vQ
            lengthHotSpot_iStartQuench = l

            r_el_m = np.zeros((self.nHalfTurns,))
            for ht in range(1, self.nHalfTurns + 1):
                current_group = self.HalfTurnToGroup[ht - 1]
                mean_B = np.mean(self.MagnetField.B[np.where(self.strandToHalfTurn == ht)]) / \
                         Iref * self.Magnet.Inputs.I00  # average magnetic field in the current half-turn
                rho_mean = rho_Cu_10K + rho_Cu_10K_B * mean_B  # average resistivity in the current half-turn
                cross_section = nStrands_inGroup[current_group - 1] * np.pi / 4 * ds_inGroup[current_group - 1] ** 2 * (
                                1 - f_SC_strand_inGroup[current_group - 1])

                # Electrical resistance per unit length
                r_el_m[ht - 1] = rho_mean / cross_section

                UQD_i = (self.Magnet.Inputs.I00 * r_el_m[ht - 1] * lengthHotSpot_iStartQuench[ht - 1])
                tQD = (uQuenchDetectionThreshold - UQD_i) / (vQ_iStartQuench[ht - 1] * r_el_m[ht - 1] * self.Magnet.Inputs.I00 + 1E-12)
                mean_B_ht = np.hstack([mean_B_ht, mean_B])
                rho_ht_10K = np.hstack([rho_ht_10K, np.array(rho_mean)])
                r_el_ht_10K = np.hstack([r_el_ht_10K, np.array(r_el_m[ht - 1])])
                tQuenchDetection = np.hstack([tQuenchDetection, np.array(tQD)])

                r_el_m = r_el_m.transpose()
                tQuenchDetection = []
                for ht in range(1, self.nHalfTurns + 1):
                    # Approximate time to reach the quench detection threshold
                    UQD_i = ( self.Magnet.Inputs.I00 * r_el_m[ht - 1] * lengthHotSpot_iStartQuench[ht - 1])
                    tQD = (uQuenchDetectionThreshold - UQD_i) / (vQ_iStartQuench[ht - 1] * r_el_m[ht - 1] * self.Magnet.Inputs.I00+ 1E-12)
                    delay = np.concatenate((np.array(delta_t_w[str(ht)]), np.array(delta_t_h[str(ht)])), axis=None)
                    th_con = np.concatenate((np.array(th_con_w[str(ht)]), np.array(th_con_h[str(ht)])), axis=None).astype(int)
                    tQD_i = tQD
                    t_i0 = 0
                    t_i1 = 0
                    idx_turns = np.array([ht - 1])
                    quenched_turns = [ht]
                    delay[delay > tQD_i] = 9999

                    while np.any(delay < 999):
                        idx = np.argmin(delay)
                        if th_con[idx] in quenched_turns:
                            delay[idx] = 9999
                            continue
                        else:
                            quenched_turns.append(int(th_con[idx]))
                        UQD_i = UQD_i + np.sum(self.Magnet.Inputs.I00 * r_el_m[idx_turns] * (t_i1 - t_i0) * vQ_iStartQuench[idx_turns])
                        idx_turns = np.append(idx_turns, int(th_con[idx] - 1))
                        t_i1 = delay[idx]
                        tQD_i = (uQuenchDetectionThreshold - UQD_i) / (
                            np.sum(vQ_iStartQuench[idx_turns] * r_el_m[idx_turns] * self.Magnet.Inputs.I00+ 1E-12))
                        t_i0 = t_i1
                        delay = np.concatenate((delay, np.array(delta_t_w[str(int(th_con[idx]))] + t_i1),
                                                np.array(delta_t_h[str(int(th_con[idx]))] + t_i1)), axis=None)
                        th_con = np.concatenate(
                            (th_con, np.array(th_con_w[str(int(th_con[idx]))]), np.array(th_con_h[str(int(th_con[idx]))])),
                            axis=None)
                        delay[delay > tQD_i] = 9999
                        delay[idx] = 9999
                    tQuenchDetection = np.hstack([tQuenchDetection, np.array(tQD_i)])

            f = plt.figure(figsize=(24, 6))
            plt.subplot(1, 4, 1)
            plt.scatter(self.MagnetGeometry.x_ave * 1000, self.MagnetGeometry.y_ave * 1000, s=2, c=self.Magnet.Inputs.vQ_iStartQuench)
            plt.xlabel('x [mm]', **self.selectedFont)
            plt.ylabel('y [mm]', **self.selectedFont)
            plt.title('2D cross-section Quench propagation velocity', **self.selectedFont)
            plt.set_cmap('jet')
            plt.grid('minor', alpha=0.5)
            cbar = plt.colorbar()
            cbar.set_label('Quench velocity [m/s]', **self.selectedFont)
            plt.rcParams.update({'font.size': 12})
            plt.axis('equal')

            plt.subplot(1, 4, 2)
            plt.scatter(self.MagnetGeometry.x_ave * 1000, self.MagnetGeometry.y_ave * 1000, s=2, c=rho_ht_10K)
            plt.xlabel('x [mm]', **self.selectedFont)
            plt.ylabel('y [mm]', **self.selectedFont)
            plt.title('Resistivity', **self.selectedFont)
            plt.set_cmap('jet')
            plt.grid('minor', alpha=0.5)
            cbar = plt.colorbar()
            cbar.set_label('Resistivity [$\Omega$*m]', **self.selectedFont)
            plt.rcParams.update({'font.size': 12})
            plt.axis('equal')

            plt.subplot(1, 4, 3)
            plt.scatter(self.MagnetGeometry.x_ave * 1000, self.MagnetGeometry.y_ave * 1000, s=2, c=r_el_ht_10K)
            plt.xlabel('x [mm]', **self.selectedFont)
            plt.ylabel('y [mm]', **self.selectedFont)
            plt.title('Resistance per unit length', **self.selectedFont)
            plt.set_cmap('jet')
            plt.grid('minor', alpha=0.5)
            cbar = plt.colorbar()
            cbar.set_label('Resistance per unit length [$\Omega$/m]', **self.selectedFont)
            plt.rcParams.update({'font.size': 12})
            plt.axis('equal')

            plt.subplot(1, 4, 4)
            plt.scatter(self.MagnetGeometry.x_ave * 1000, self.MagnetGeometry.y_ave * 1000, s=2, c=tQuenchDetection * 1e3)
            plt.xlabel('x [mm]', **self.selectedFont)
            plt.ylabel('y [mm]', **self.selectedFont)
            plt.title('Approximate quench detection time', **self.selectedFont)
            plt.set_cmap('jet')
            plt.grid('minor', alpha=0.5)
            cbar = plt.colorbar()
            cbar.set_label('Time [ms]', **self.selectedFont)
            plt.rcParams.update({'font.size': 12})
            plt.axis('equal')
            plt.tight_layout()
            plt.show()

    def plot_electrical_order(self):
        plt.figure(figsize=(24, 8))
        plt.subplot(1, 3, 1)
        plt.scatter(self.MagnetGeometry.x_ave, self.MagnetGeometry.y_ave, s=2, c=np.argsort(self.Magnet.Inputs.el_order_half_turns))
        plt.xlabel('x [m]', **self.selectedFont)
        plt.ylabel('y [m]', **self.selectedFont)
        plt.title('Electrical order of the half-turns', **self.selectedFont)
        plt.set_cmap('jet')
        cbar = plt.colorbar()
        cbar.set_label('Electrical order [-]', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        plt.axis('equal')
        # Plot
        plt.subplot(1, 3, 2)
        plt.plot(self.MagnetGeometry.x_ave[self.Magnet.Inputs.el_order_half_turns - 1],
                 self.MagnetGeometry.y_ave[self.Magnet.Inputs.el_order_half_turns - 1], 'k')
        plt.scatter(self.MagnetGeometry.x_ave, self.MagnetGeometry.y_ave, s=2, c=np.repeat(self.Magnet.Inputs.nStrands_inGroup, self.Magnet.Inputs.nT))
        plt.scatter(self.MagnetGeometry.x_ave[self.Magnet.Inputs.el_order_half_turns[0] - 1],
                    self.MagnetGeometry.y_ave[self.Magnet.Inputs.el_order_half_turns[0] - 1], s=50, c='r',
                    label='Positive lead')
        plt.scatter(self.MagnetGeometry.x_ave[self.Magnet.Inputs.el_order_half_turns[-1] - 1],
                    self.MagnetGeometry.y_ave[self.Magnet.Inputs.el_order_half_turns[-1] - 1], s=50, c='b',
                    label='Negative lead')
        plt.xlabel('x [m]', **self.selectedFont)
        plt.ylabel('y [m]', **self.selectedFont)
        plt.title('Electrical order of the half-turns', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        plt.axis('equal')
        plt.legend(loc='lower left')
        # Plot
        plt.subplot(1, 3, 3)
        plt.plot(self.MagnetGeometry.x_ave_group[self.elPairs_GroupTogether[:,0]-1],self.MagnetGeometry.y_ave_group[self.elPairs_GroupTogether[:,1]-1],'b') #TODO this does not work for solenoids and needs changing
        plt.scatter(self.MagnetGeometry.x, self.MagnetGeometry.y, s=2, c='k')
        plt.scatter(self.MagnetGeometry.x_ave_group, self.MagnetGeometry.y_ave_group, s=10, c='r')
        plt.xlabel('x [m]', **self.selectedFont)
        plt.ylabel('y [m]', **self.selectedFont)
        plt.title('Electrical order of the groups (only go-lines)', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        plt.axis('equal')
        plt.show()

    def plot_heat_exchange_order(self):
        plt.figure(figsize=(10, 10))
        # plot strand positions
        plt.scatter(self.MagnetGeometry.x, self.MagnetGeometry.y, s=2, c='b')
        # plot heat exchange links along the cable narrow side
        for i in range(len(self.Magnet.Inputs.iContactAlongHeight_From)):
            plt.plot([self.MagnetGeometry.x_ave[self.Magnet.Inputs.iContactAlongHeight_From[i] - 1],
                      self.MagnetGeometry.x_ave[self.Magnet.Inputs.iContactAlongHeight_To[i] - 1]],
                     [self.MagnetGeometry.y_ave[self.Magnet.Inputs.iContactAlongHeight_From[i] - 1],
                      self.MagnetGeometry.y_ave[self.Magnet.Inputs.iContactAlongHeight_To[i] - 1]], 'k')
        # plot heat exchange links along the cable wide side
        for i in range(len(self.Magnet.Inputs.iContactAlongWidth_From)):
            plt.plot([self.MagnetGeometry.x_ave[self.Magnet.Inputs.iContactAlongWidth_From[i] - 1],
                      self.MagnetGeometry.x_ave[self.Magnet.Inputs.iContactAlongWidth_To[i] - 1]],
                     [self.MagnetGeometry.y_ave[self.Magnet.Inputs.iContactAlongWidth_From[i] - 1],
                      self.MagnetGeometry.y_ave[self.Magnet.Inputs.iContactAlongWidth_To[i] - 1]], 'r')
        plt.xlabel('x [m]', **self.selectedFont)
        plt.ylabel('y [m]', **self.selectedFont)
        plt.title('Heat exchange order of the half-turns', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        plt.axis('equal')
        plt.show()

        [_, th_con_w, th_con_h] = self.Magnet._obtainThermalConnections()
        ThConnections = np.zeros((self.nHalfTurns))
        for i in range(1, self.nHalfTurns+1):
            count = 0
            if str(i) in th_con_w.keys(): count = count + len(th_con_w[str(i)])
            if str(i) in th_con_h.keys(): count = count + len(th_con_h[str(i)])
            ThConnections[i-1] = count

        data = [{'x': self.MagnetGeometry.x_ave, 'y': self.MagnetGeometry.y_ave, 'z': ThConnections}]
        titles = ['Number of Thermal connections']
        labels = [{'x': "x (m)", 'y': "y (m)", 'z': ""}] * len(data)
        types = ['scatter'] * len(data)
        texts = [self.text] * len(data)
        self.plotter(data, titles, labels, types, texts)

    def plot_power_supl_contr(self):
        plt.figure(figsize=(5, 5))
        plt.plot([self.Magnet.Inputs.t_PC, self.Magnet.Inputs.t_PC], [np.min(self.Magnet.Inputs.I_PC_LUT), np.max(self.Magnet.Inputs.I_PC_LUT)], 'k--', linewidth=4.0,
                 label='t_PC')
        plt.plot(self.Magnet.Inputs.t_PC_LUT, self.Magnet.Inputs.I_PC_LUT, 'ro-', label='LUT')
        plt.xlabel('Time [s]', **self.selectedFont)
        plt.ylabel('Current [A]', **self.selectedFont)
        plt.title('Look-up table controlling power supply', **self.selectedFont)
        plt.grid(True)
        plt.rcParams.update({'font.size': 12})
        plt.show()

    def plot_all(self):
        self.plot_field()
        self.plot_Conductors()
        #self.plot_polarities()
        self.plot_strands_groups_layers()
        self.plot_quench_prop_and_resist()
        self.plot_half_turns()
        #self.plot_electrical_order()
        self.plot_heat_exchange_order()
        self.plot_nonlin_induct()
        self.plot_psu_and_trig()
        self.plot_power_supl_contr()
