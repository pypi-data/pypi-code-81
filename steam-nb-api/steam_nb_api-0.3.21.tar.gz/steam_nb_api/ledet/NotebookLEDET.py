import os
import copy
import numpy as np
import yaml
import subprocess
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

from steam_nb_api.ledet.ParametersLEDET import ParametersLEDET
from steam_nb_api.ledet.Simulation import RunSimulations
from steam_nb_api.roxie_parser.geometricFunctions import close_pairs_ckdtree, close_pairs_pdist
import pysoleno as pysol
from steam_nb_api.resources.ResourceReader import ResourceReader


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

class Solenoid:
    def __init__(self, sol_name, sol_dict):
        self.sol_name = sol_name
        self.sol_dict = sol_dict
        self.conductor = sol_dict['wire']
        self.n_layers = int(np.rint((self.sol_dict['A2'] - self.sol_dict['A1']) / self.conductor['strand']['sh_i']))
        self.n_turns_per_layer = int(np.rint((self.sol_dict['B2'] - self.sol_dict['B1']) / self.conductor['strand']['sw_i']))
        self.tot_n_turns = self.n_turns_per_layer * self.n_layers

        f_layer_m_t_r = self.sol_dict['A1'] + self.conductor['strand']['sh_i'] / 2  # first layer middle turn radial position
        l_layer_m_t_r = f_layer_m_t_r + (self.n_layers - 1) * self.conductor['strand'][
            'sh_i']  # last layer middle turn radial position
        r_pos = np.linspace(f_layer_m_t_r, l_layer_m_t_r, self.n_layers,
                            endpoint=True)  # layers middle turns radial positions
        f_layer_m_t_z = self.sol_dict['B1'] + self.conductor['strand']['sw_i'] / 2  # first layer middle turn axial position
        l_layer_m_t_z = f_layer_m_t_z + (self.n_turns_per_layer - 1) * self.conductor['strand'][
            'sw_i']  # last layer middle turn axial position
        z_pos = np.linspace(f_layer_m_t_z, l_layer_m_t_z, self.n_turns_per_layer,
                            endpoint=True)  # layers middle turns axial positions
        self.rr_pos, self.zz_pos = np.meshgrid(r_pos, z_pos)

        self.rr_pos = self.rr_pos.T
        self.zz_pos = self.zz_pos.T

        self.Rin = np.linspace(self.sol_dict['A1'], self.sol_dict['A1'] + (self.n_layers - 1) * self.conductor['strand']['sh_i'],
                               self.n_layers, endpoint=True)  # layers start turns radial positions
        self.Rout = self.Rin + self.conductor['strand']['sh_i']  # layers end turns radial positions
        self.Zlow = np.ones_like(self.Rin) * self.sol_dict['B1']  # layers start axial positions
        self.Zhigh = np.ones_like(self.Rin) * self.sol_dict['B2']  # layers end axial positions
        self.Is = np.ones_like(self.Rin) * 0  # layers current
        self.Nturns = np.ones_like(self.Rin, dtype=np.int32) * self.n_turns_per_layer  # layers number of turns


class Solenoid_magnet:
    def __init__(self, magnet_name):
        self.magnet_data = _read_yaml('magnet', magnet_name)
        for block_name, block_dict in self.magnet_data['blocks'].items():
            self.magnet_data['blocks'][block_name]['wire'] = _read_yaml('wire', block_dict['wire'])

        Nloop = 6  # number of loops - higher means higher accuracy
        pysol_data = [Solenoid(sol_name, sol_dict) for sol_name, sol_dict in self.magnet_data['blocks'].items()]
        Rins = np.concatenate([sol.Rin for sol in pysol_data], axis=None)
        Routs = np.concatenate([sol.Rout for sol in pysol_data], axis=None)
        Zlows = np.concatenate([sol.Zlow for sol in pysol_data], axis=None)
        Zhighs = np.concatenate([sol.Zhigh for sol in pysol_data], axis=None)
        Is = np.concatenate([np.ones_like(sol.Rin) * self.magnet_data['I'] for sol in pysol_data], axis=None)
        Nts = np.concatenate([sol.Nturns for sol in pysol_data], axis=None)
        NLs = np.concatenate([np.ones_like(sol.Rin, dtype=np.int32) * Nloop for sol in pysol_data], axis=None)
        self.group_sets = Rins, Routs, Zlows, Zhighs, Is, Nts, NLs

        blocks = []
        conductors = []
        numbers = []
        currents = []
        block_nr = 1
        cond_nr = 1
        for block in pysol_data:
            blocks.append(
                np.repeat(np.arange(block_nr, block.n_layers + block_nr, dtype=np.int32), block.n_turns_per_layer))
            conductors.append(np.arange(cond_nr, block.tot_n_turns + cond_nr, dtype=np.int32))
            numbers.append(np.arange(cond_nr, block.tot_n_turns + cond_nr, dtype=np.int32))
            currents.append(np.ones(block.tot_n_turns) * self.magnet_data['I'])
            block_nr = block_nr + block.n_layers
            cond_nr = cond_nr + block.tot_n_turns
        self.block = np.concatenate(blocks, axis=None)
        self.conductor = np.concatenate(conductors, axis=None)
        self.number = np.concatenate(numbers, axis=None)
        self.current = np.concatenate(currents, axis=None)
        self.area = np.zeros_like(self.number)
        self.fill_fac = np.zeros_like(self.number)

        self.rr_pos = np.concatenate([sol.rr_pos for sol in pysol_data], axis=None)
        self.zz_pos = np.concatenate([sol.zz_pos for sol in pysol_data], axis=None)

    def calc_L_M(self):
        return pysol.PySoleno().calcM(*self.group_sets)

    def calc_L_tot(self):
        return np.sum(self.calc_L_M())

    def calc_Br_Bz(self):
        Br, Bz = pysol.PySoleno().calcB(self.rr_pos, self.zz_pos, *self.group_sets)
        return self.rr_pos, self.zz_pos, Br, Bz

    def save_L_M(self, Ind_matrix_file):
        with open(Ind_matrix_file, 'w') as fp:
            fp.write("Extended self mutual inductance matrix [H/m]\n")
            np.savetxt(fp, self.calc_L_M(), '%6.16e', ',')

    def save_B_map(self, field_map_file):
        rr_pos, zz_pos, Br, Bz = self.calc_Br_Bz()
        output = np.array(
            [self.block, self.conductor, self.number, rr_pos.flatten('F') * 1000, zz_pos.flatten('F') * 1000,
             Br.flatten('F'), Bz.flatten('F'), self.area, self.current, self.fill_fac]).T
        with open(field_map_file, 'w') as fp:
            fp.write("BL. COND. NO. R-POS/MM Z-POS/MM BR/T BZ/T AREA/MM**2 CURRENT FILL FAC.  \n\n")
            np.savetxt(fp, output, '%d %d %d %6.5f %6.5f %6.5f %6.5f %6.5f %6.5f %6.5f', ',')

    def print_summary(self):
        print(f"Turns = {np.max(self.number)}")
        L = self.calc_L_tot()
        E = 0.5 * L * self.magnet_data['I'] ** 2
        print(f"L = {L:.3f} H")
        print(f"E = {1e-3 * E:.3f} kJ")


class NB_LEDET:
    def __init__(self, scenario_name, model_no, output_folder="", recalc_field=True):
        self.scenario_name = scenario_name
        self.model_no = model_no

        self.scenario_data = _read_yaml('scenario', scenario_name)
        self.circuit_data = _read_yaml('circuit', self.scenario_data['circuit'])
        self.protection_data = _read_yaml('protection', self.scenario_data['protection'])

        self.magnet_name = self.scenario_data['magnet']
        self.magnet_data = _read_yaml('magnet', self.magnet_name)

        if output_folder == "":
            self.base_folder = os.getcwd()
            self.magnet_folder = self.base_folder
            self.field_maps_folder = self.base_folder
        else:
            self.base_folder = output_folder
            self.magnet_folder = os.path.join(os.path.join(os.path.join(self.base_folder, 'LEDET'), self.magnet_name),
                                          'Input')
            self.field_maps_folder = os.path.join(os.path.join(self.base_folder, 'Field maps'), self.magnet_name)

        if not os.path.exists(self.magnet_folder):
            os.makedirs(self.magnet_folder)
        if not os.path.exists(self.field_maps_folder):
            os.makedirs(self.field_maps_folder)
        self.field_map_file = os.path.join(self.field_maps_folder, f"{self.magnet_name}_All_NoIron_NoSelfField.map2d")
        self.Ind_matrix_file = os.path.join(self.magnet_folder, f"{self.magnet_name}_selfMutualInductanceMatrix.csv")

        self.flagIron = self.magnet_data['flagIron']
        self.flagSelfField = self.magnet_data['flagSelfField']

        if self.magnet_data['type'] == 'solenoid':
            self.consistency_checks = True
            self.flag_typeWindings = 1
            self.m = Solenoid_magnet(self.magnet_name)
            if recalc_field:
                if self.flagIron == 1 or self.flagSelfField == 1:
                    raise Exception(
                        'Can not calculate magnetic field using soleno and account for self field or iron effect')
                else:
                    self.m.save_B_map(self.field_map_file)
                    self.m.save_L_M(self.Ind_matrix_file)
        else:
            self.consistency_checks = False
            pass  # TODO add other magnet types, dipole etc.

        self.selectedFont = {'fontname': 'DejaVu Sans', 'size': 14}  # Define style for plots
        self.verbose = False  # If this variable is set to True, many comments will be displayed

        self.I00 = self.magnet_data['I']
        self.T00 = self.magnet_data['T']  # [K]
        self.Iref = self.I00
        self.fL_I = [0, 1000]
        self.fL_L = [1.0, 1.0]
        self.M_m = np.sum(np.loadtxt(self.Ind_matrix_file, delimiter=',', skiprows=1))
        self.l_magnet = 1  # [m] THIS MUST REMAIN =1 for solenoid
        self.l_mag_inGroup = []
        self.max_distance = 1.5E-3  # Prepare input for the function close_pairs_ckdtree
        self._ttdf = 99999  # time to deactivate feature

        self.nT = []
        self.ds_inGroup = []
        self.f_SC_strand_inGroup = []
        self.f_ro_eff_inGroup = []
        self.Lp_f_inGroup = []
        self.RRR_Cu_inGroup = []
        self.SCtype_inGroup = []
        self.STtype_inGroup = []
        self.insulationType_inGroup = []
        self.internalVoidsType_inGroup = []
        self.externalVoidsType_inGroup = []
        self.wBare_inGroup = []
        self.hBare_inGroup = []
        self.wIns_inGroup = []
        self.hIns_inGroup = []
        self.Lp_s_inGroup = []
        self.R_c_inGroup = []
        self.Tc0_NbTi_ht_inGroup = []
        self.Bc2_NbTi_ht_inGroup = []
        self.c1_Ic_NbTi_inGroup = []
        self.c2_Ic_NbTi_inGroup = []
        self.Tc0_Nb3Sn_inGroup = []
        self.Bc2_Nb3Sn_inGroup = []
        self.Jc_Nb3Sn0_inGroup = []

        supercon_dict = {'Nb-Ti': 1, "Nb3Sn(Summer's fit)": 2, "BSCCO2212": 3, "Nb3Sn(Bordini's fit)": 4}
        stabil_dict = {'Cu': 1, 'Ag': 2}
        insul_type_dict = {'G10': 1, 'kapton': 2}
        filler_strand_dict = {"G10": 1, "kapton": 2, "helium": 3, "void": 4}
        filler_insul_dict = {"G10": 1, "kapton": 2, "helium": 3, "void": 4}
        for block_name, block_dict in self.m.magnet_data['blocks'].items():
            conductor = block_dict['wire']
            strand = conductor['strand']
            SC_type = list(strand['SC_type'])[0]
            cable = conductor['cable']
            if conductor['type'] == 'rectangular':
                wire_area = ((strand['sw_i'] - 2 * strand['si_w']) * (
                        strand['sh_i'] - 2 * strand['si_h'])) - ((4 - np.pi) * strand['scr_i'] ** 2)
                eq_diam = np.sqrt(wire_area * 4 / np.pi)  # equivalent diameter with correcting for the corner radius
            else:
                eq_diam = 0  # TODO other conductor types, like cables, round monolith wires

            if self.m.magnet_data['type'] == 'solenoid':
                sol = Solenoid(block_name, block_dict)
                self.n_groups_in_block = np.shape(sol.Rin)[0]
                self.ds_inGroup.append(np.ones(self.n_groups_in_block) * eq_diam)  # equivalent diameter
                self.nT.append(
                    np.ones(self.n_groups_in_block,
                            dtype=np.int32) * sol.n_turns_per_layer)  # Number of half-turns in each group
                self.l_mag_inGroup.append(2 * np.pi * (sol.Rin + sol.Rout) / 2)  # Length of turns of each layer
            else:
                pass  # TODO add other magnet types, like dipole

            self.f_SC_strand_inGroup.append(
                np.ones(self.n_groups_in_block) * (
                        1 / (1 + strand['Cu_SC'])))  # fraction of superconductor in the strands
            self.f_ro_eff_inGroup.append(
                np.ones(self.n_groups_in_block) * strand['Ro_eff'])  # Effective transverse resistivity parameter
            self.Lp_f_inGroup.append(
                np.ones(self.n_groups_in_block) * strand['stp'])  # Filament twist-pitch [m]# guess value
            self.RRR_Cu_inGroup.append(np.ones(self.n_groups_in_block) * strand[
                'RRR'] / 1.086)  # RRR of the conductor in each group of cables# 1.086 factor applied to RRR to correct for the fact that the NIST fit considers RRR measured between 273 K (not room temperature) and cryogenic temperature
            self.SCtype_inGroup.append(np.ones(self.n_groups_in_block) * supercon_dict[SC_type])
            self.STtype_inGroup.append(np.ones(self.n_groups_in_block) * stabil_dict[strand['stabilizer']])
            self.insulationType_inGroup.append(
                np.ones(self.n_groups_in_block) * insul_type_dict[strand['insulation_type']])
            self.internalVoidsType_inGroup.append(
                np.ones(self.n_groups_in_block) * filler_strand_dict[cable['fil_adj_str']])
            self.externalVoidsType_inGroup.append(
                np.ones(self.n_groups_in_block) * filler_insul_dict[cable['fil_btw_str_ins_l']])
            self.wBare_inGroup.append(np.ones(self.n_groups_in_block) * (strand['sh_i'] - strand[
                'si_h']))  # they need to be swapped - bare cable width [m] RADIAL direction
            self.hBare_inGroup.append(np.ones(self.n_groups_in_block) * (strand['sw_i'] - strand[
                'si_w']))  # they need to be swapped -bare average cable height [m] AXIAL direction
            self.wIns_inGroup.append(np.ones(self.n_groups_in_block) * strand[
                'si_h'])  # they need to be swapped - insulation thickness in the radial direction [m]
            self.hIns_inGroup.append(np.ones(self.n_groups_in_block) * strand[
                'si_w'])  # they need to be swapped - insulation thickness in the axial direction [m]
            self.Lp_s_inGroup.append(np.ones(self.n_groups_in_block) * cable['Lp_s'])  # Strand twist-pitch [m] THIS WILL BE IGNORED
            self.R_c_inGroup.append(
                np.ones(self.n_groups_in_block) * cable['R_c'])  # Cross-contact resistance [Ohm] THIS WILL BE IGNORED
            if SC_type == 'Nb-Ti':
                self.Tc0_NbTi_ht_inGroup.append(
                    np.ones(self.n_groups_in_block) * strand['SC_type'][SC_type]['Tc0'])  # Tc0_NbTi_ht_inGroup [K]
                self.Bc2_NbTi_ht_inGroup.append(
                    np.ones(self.n_groups_in_block) * strand['SC_type'][SC_type]['Bc2'])  # Bc2_NbTi_ht_inGroup [T]
                self.c1_Ic_NbTi_inGroup.append(
                    np.ones(self.n_groups_in_block) * strand['SC_type'][SC_type]['c1_Ic'])  # c1_Ic_NbTi_inGroup [A]
                self.c2_Ic_NbTi_inGroup.append(
                    np.ones(self.n_groups_in_block) * strand['SC_type'][SC_type]['c2_Ic'])  # c2_Ic_NbTi_inGroup [A/T]
                self.Tc0_Nb3Sn_inGroup.append(np.ones(self.n_groups_in_block) * 0)  # Tc0_Nb3Sn [K]  THIS WILL BE IGNORED
                self.Bc2_Nb3Sn_inGroup.append(np.ones(self.n_groups_in_block) * 0)  # Bc2_Nb3Sn [T]  THIS WILL BE IGNORED
                self.Jc_Nb3Sn0_inGroup.append(np.ones(
                    self.n_groups_in_block) * 0)  # Jc_Nb3Sn0 [A*T^0.5/m^2] Based on short-sample measurement THIS WILL BE IGNORED
            elif SC_type == 'Nb3Sn':
                self.Tc0_NbTi_ht_inGroup.append(
                    np.ones(self.n_groups_in_block) * 0)  # Tc0_NbTi_ht_inGroup [K]
                self.Bc2_NbTi_ht_inGroup.append(
                    np.ones(self.n_groups_in_block) * 0)  # Bc2_NbTi_ht_inGroup [T]
                self.c1_Ic_NbTi_inGroup.append(
                    np.ones(self.n_groups_in_block) * 0)  # c1_Ic_NbTi_inGroup [A]
                self.c2_Ic_NbTi_inGroup.append(
                    np.ones(self.n_groups_in_block) * 0)  # c2_Ic_NbTi_inGroup [A/T]
                self.Tc0_Nb3Sn_inGroup.append(np.ones(self.n_groups_in_block) * strand['SC_type'][SC_type]['Tc0'])  # Tc0_Nb3Sn [K]  THIS WILL BE IGNORED
                self.Bc2_Nb3Sn_inGroup.append(np.ones(self.n_groups_in_block) * strand['SC_type'][SC_type]['Bc2'])  # Bc2_Nb3Sn [T]  THIS WILL BE IGNORED
                self.Jc_Nb3Sn0_inGroup.append(np.ones(self.n_groups_in_block) * strand['SC_type'][SC_type]['Jc'])  # Jc_Nb3Sn0 [A*T^0.5/m^2] Based on short-sample measurement THIS WILL BE IGNORED

        self.ds_inGroup = np.concatenate(self.ds_inGroup, axis=None)
        self.nT = np.concatenate(self.nT, axis=None)
        self.l_mag_inGroup = np.concatenate(self.l_mag_inGroup, axis=None)
        self.f_SC_strand_inGroup = np.concatenate(self.f_SC_strand_inGroup, axis=None)
        self.f_ro_eff_inGroup = np.concatenate(self.f_ro_eff_inGroup, axis=None)
        self.Lp_f_inGroup = np.concatenate(self.Lp_f_inGroup, axis=None)
        self.RRR_Cu_inGroup = np.concatenate(self.RRR_Cu_inGroup, axis=None)
        self.SCtype_inGroup = np.concatenate(self.SCtype_inGroup, axis=None)
        self.STtype_inGroup = np.concatenate(self.STtype_inGroup, axis=None)
        self.insulationType_inGroup = np.concatenate(self.insulationType_inGroup, axis=None)
        self.internalVoidsType_inGroup = np.concatenate(self.internalVoidsType_inGroup, axis=None)
        self.externalVoidsType_inGroup = np.concatenate(self.externalVoidsType_inGroup, axis=None)
        self.wBare_inGroup = np.concatenate(self.wBare_inGroup, axis=None)
        self.hBare_inGroup = np.concatenate(self.hBare_inGroup, axis=None)
        self.wIns_inGroup = np.concatenate(self.wIns_inGroup, axis=None)
        self.hIns_inGroup = np.concatenate(self.hIns_inGroup, axis=None)
        self.Tc0_NbTi_ht_inGroup = np.concatenate(self.Tc0_NbTi_ht_inGroup, axis=None)
        self.Bc2_NbTi_ht_inGroup = np.concatenate(self.Bc2_NbTi_ht_inGroup, axis=None)
        self.c1_Ic_NbTi_inGroup = np.concatenate(self.c1_Ic_NbTi_inGroup, axis=None)
        self.c2_Ic_NbTi_inGroup = np.concatenate(self.c2_Ic_NbTi_inGroup, axis=None)
        self.Lp_s_inGroup = np.concatenate(self.Lp_s_inGroup, axis=None)
        self.R_c_inGroup = np.concatenate(self.R_c_inGroup, axis=None)
        self.Tc0_Nb3Sn_inGroup = np.concatenate(self.Tc0_Nb3Sn_inGroup, axis=None)
        self.Bc2_Nb3Sn_inGroup = np.concatenate(self.Bc2_Nb3Sn_inGroup, axis=None)
        self.Jc_Nb3Sn0_inGroup = np.concatenate(self.Jc_Nb3Sn0_inGroup, axis=None)

        self.nGroupsDefined = len(self.ds_inGroup)
        self.nHalfTurnsDefined = np.sum(self.nT)

        #  Scale up or down the contribution of heat exchange through the short side of the conductors (useful to change the insulation between coil layers)
        insulationBetweenLayers = 0E-6  # !!!!  TODO Does it make sense to specify this for each group on conductor level
        insulationAroundCables = 0E-6  # !!!!   TODO Does it make sense to specify this for each group on conductor level
        # self.fScaling_Pex_AlongHeight_Defined = (2 * insulationAroundCables) / (2 * insulationAroundCables + insulationBetweenLayers)
        self.fScaling_Pex_AlongHeight_Defined = 1

        # # # Circuit warm resistance and power-supply crowbar
        self.R_circuit = self.circuit_data['R_circuit_warm']  # Resistance of the warm parts of the circuit [Ohm]
        self.R_crowbar = self.circuit_data['R_crowbar']  # Resistance of crowbar of the power supply [Ohm]
        self.Ud_crowbar = self.circuit_data[
            'Ud_crowbar']  # Forward voltage drop of a diode or thyristor in the crowbar of the power supply [V]

        # # # Power supply control
        self.t_PC = self.protection_data[
            't_PC']  # Time when the power supply is switched off and the crowbar is switched on [s]


        earliest_time_in_simul_time = np.min([start['start'] for start in self.scenario_data['simul_time']])
        self.PSU_ramp_down_duration = 0.01
        self.t_PC_LUT = [earliest_time_in_simul_time, self.t_PC,
                         self.t_PC + self.PSU_ramp_down_duration]  # LUT controlling power supply, Time [s] #TODO WHY does it matter how PC is switched off
        self.I_PC_LUT = [self.I00, self.I00, 0]  # LUT controlling power supply, Current [A]

        # # # Energy-extraction system
        self.tEE = self.protection_data['t_EE']  # Time when the energy-extraction system is triggered [s]
        self.R_EE_triggered = (self.protection_data['U_EE'] - self.I00 * (
                self.R_circuit + self.R_crowbar) - self.Ud_crowbar) / self.I00  # Resistance of the energy-extraction system [Ohm]
        if self.R_EE_triggered < 0:
            self.R_EE_triggered = 0

        self.time_vector_params = [item for sublist in [[rng['start'], rng['step'], rng['stop']] for rng in
                                                        self.scenario_data['simul_time']] for item in
                                   sublist]  # start, step, end

        if self._ttdf < self.time_vector_params[
            len(self.time_vector_params) - 1]:  # check if time to deactivate feature is shorter than simulation time
            raise Exception(
                'Simulation time is so long that it exceeds time to deactivate feature. Increase ._ttdf to bo longer than simulation time')

        self.headerLines = 1
        self.strandToGroup = np.array([])
        self.strandToHalfTurn = np.array([])
        idx = []
        self.x = []
        self.y = []
        self.Bx = []
        self.By = []
        Area = []
        self.I = []
        fillFactor = []

        file = open(self.field_map_file, "r")  # Read file
        fileContent = file.read()
        fileContentByRow = fileContent.split("\n")  # Separate rows

        for index in range(len(fileContentByRow) - 1):
            if index > self.headerLines:
                fc = fileContentByRow[index]
                row = fc.split()
                self.strandToGroup = np.hstack([self.strandToGroup, int(row[0])])
                self.strandToHalfTurn = np.hstack([self.strandToHalfTurn, int(row[1])])
                idx = np.hstack([idx, float(row[2])])
                self.x = np.hstack([self.x, float(row[3]) / 1000])  # in [m]
                self.y = np.hstack([self.y, float(row[4]) / 1000])  # in [m]
                self.Bx = np.hstack([self.Bx, float(row[5])])
                self.By = np.hstack([self.By, float(row[6])])
                Area = np.hstack([Area, float(row[7])])
                self.I = np.hstack([self.I, float(row[8])])
                fillFactor = np.hstack([fillFactor, float(row[9])])

        self.nStrandsFieldMap = len(self.x)
        # Calculate absolute magnetic field
        self.B = []
        for i in range(self.nStrandsFieldMap):
            self.B = np.hstack([self.B, (self.Bx[i] ** 2 + self.By[i] ** 2) ** .5])
        self.nStrands = len(self.strandToGroup)
        # polarities = np.sign(self.I)
        self.nHalfTurns = int(np.max(self.strandToHalfTurn))
        self.nTurns = self.nHalfTurns  # this is specific for solenoids
        self.nGroups = int(np.max(self.strandToGroup))
        self.nS = []
        for ht in range(1, self.nHalfTurns + 1):
            # nS =sum(strandToHalfTurn==ht);
            self.nS = np.hstack(
                [self.nS, np.size(np.where(self.strandToHalfTurn == ht))])  # Number of strands in each half-turn
        self.nS = np.int_(self.nS)
        self.strandToGroup = np.int_(self.strandToGroup)
        self.strandToHalfTurn = np.int_(self.strandToHalfTurn)
        self.halfTurnToTurn = self.strandToHalfTurn

        # Average half-turn positions
        self.x_ave = []
        self.y_ave = []
        for ht in range(1, self.nHalfTurns + 1):
            self.x_ave = np.hstack([self.x_ave, np.mean(self.x[np.where(self.strandToHalfTurn == ht)])])
            self.y_ave = np.hstack([self.y_ave, np.mean(self.y[np.where(self.strandToHalfTurn == ht)])])

        # Average group positions
        self.x_ave_group = []
        self.y_ave_group = []
        for g in range(1, self.nGroups + 1):
            self.x_ave_group = np.hstack([self.x_ave_group, np.mean(self.x[np.where(self.strandToGroup == g)])])
            self.y_ave_group = np.hstack([self.y_ave_group, np.mean(self.y[np.where(self.strandToGroup == g)])])

        # # Definition of groups of conductors
        self.GroupToCoilSection = self.nGroups * [1]
        self.polarities_inGroup = self.nGroups * [+1]

        # Count number of groups defined
        self.nCoilSectionsDefined = np.max(self.GroupToCoilSection)
        self.nGroupsDefined = len(self.GroupToCoilSection)

        # Number of strands in each cable belonging to a particular group
        nStrands_inGroup = self.nGroupsDefined * [1]
        self.nStrands_inGroup = nStrands_inGroup
        # length of each half turn [m] (default=l_magnet)

        # # # Electrical order of the turns
        # Start and end indices of each group
        indexTstop = np.cumsum(self.nT)
        indexTstop = indexTstop.tolist()
        indexTstart = [1]
        for i in range(len(self.nT) - 1):
            indexTstart.extend([indexTstart[i] + self.nT[i]])

        # Calculation of the electrical order of the half-turns
        self.el_order_groups = range(self.nGroupsDefined, 0, -1)  # Electrical order of the groups
        winding_order_groups = (self.nGroupsDefined * [0, 1])[
                               :self.nGroupsDefined]  # Winding direction of the turns: following LEDET order (-->0), or its inverse (-->1)

        if len(self.el_order_groups) != self.nGroupsDefined:
            raise Exception(
                'Length of the vector el_order_groups ({}) must be equal to nGroupsDefined={}.'.format(
                    len(self.el_order_groups),
                    self.nGroupsDefined))
        self.el_order_half_turns = []
        for p in self.el_order_groups:
            for k in range(self.nT[p - 1]):
                if winding_order_groups[p - 1] == 0:
                    self.el_order_half_turns.append(indexTstart[p - 1] + k)
                if winding_order_groups[p - 1] == 1:
                    self.el_order_half_turns.append(indexTstop[p - 1] - k)

        self.el_order_half_turns_Array = np.int_(self.el_order_half_turns)  # this is just used for plotting
        # Inclination of cables with respect to X axis (including transformations for mirror and rotation)
        self.alphasDEG = self.nHalfTurnsDefined * [0]
        # Rotate cable by a certain angle [deg]
        self.rotation_block = self.nHalfTurnsDefined * [0]
        # Mirror cable along the bisector of its quadrant (0=no, 1=yes)
        self.mirror_block = self.nHalfTurnsDefined * [0]
        # Mirror cable along the Y axis (0=no, 1=yes)
        self.mirrorY_block = self.nHalfTurnsDefined * [0]

        # # # Heat exchange between half-turns along the cable wide side
        # Pairs of half-turns exchanging heat along the cable wide side
        self.iContactAlongWidth_From = []
        self.iContactAlongWidth_To = []
        for g in range(self.nGroupsDefined):
            self.iContactAlongWidth_From.extend(range(indexTstart[g], indexTstop[g]))
            self.iContactAlongWidth_To.extend(range(indexTstart[g] + 1, indexTstop[g] + 1))
        pairs_close = close_pairs_ckdtree(np.column_stack((self.x, self.y)),
                                          self.max_distance)  # find all pairs of strands closer than a distance of max_d

        contact_pairs = set([])  # find pairs that belong to half-turns located in different groups
        for cp in pairs_close:
            if not self.strandToGroup[cp[0]] == self.strandToGroup[cp[1]]:
                contact_pairs.add(
                    (self.strandToHalfTurn[cp[0]], self.strandToHalfTurn[cp[1]]))

        self.iContactAlongHeight_From = []
        self.iContactAlongHeight_To = []
        for cp in contact_pairs:  # assign the pair values to two distinct vectors
            self.iContactAlongHeight_From.append(cp[0])
            self.iContactAlongHeight_To.append(cp[1])

        idxSort = [i for (v, i) in sorted((v, i) for (i, v) in enumerate(
            self.iContactAlongHeight_From))]  # find indices to order the vector iContactAlongHeight_From

        # reorder both iContactAlongHeight_From and iContactAlongHeight_To using the indices
        self.iContactAlongHeight_From = np.array([self.iContactAlongHeight_From[i] for i in idxSort])
        self.iContactAlongHeight_To = np.array([self.iContactAlongHeight_To[i] for i in idxSort])
        self.iContactAlongHeight_From_Array = np.int_(self.iContactAlongHeight_From)
        self.iContactAlongHeight_To_Array = np.int_(self.iContactAlongHeight_To)
        self.iContactAlongWidth_From_Array = np.int_(self.iContactAlongWidth_From)
        self.iContactAlongWidth_To_Array = np.int_(self.iContactAlongWidth_To)
        self.iContactAlongWidth_From = np.array([self.iContactAlongWidth_From[i] for i in idxSort])
        self.iContactAlongWidth_To = np.array([self.iContactAlongWidth_To[i] for i in idxSort])

        # # # CLIQ system
        self.tCLIQ = self._ttdf  # Time when the CLIQ system is triggered [s]
        self.directionCurrentCLIQ = [1]  # Direction of the introduced current change for the chosen CLIQ configuration
        self.nCLIQ = 1  # Number of CLIQ units
        self.U0 = 1000  # CLIQ charging voltage [V]
        self.C = 0.04  # Capacitance of the CLIQ capacitor bank [F]
        self.Rcapa = 0.05  # Resistance of the CLIQ leads [Ohm]

        # # # Quench heater parameters - DUMMY VALUES: THERE ARE NO QUENCH HEATERS
        nHeaterStrips = 1  # Number of quench heater strips to write in the file

        self.tQH = [
            self._ttdf]  # Time at which the power supply connected to the QH strip is triggered (Low-field QHs set to a very large value to avoid triggering).
        self.U0_QH = nHeaterStrips * [450]  # Charging voltage of the capacitor connected to the QH strip.
        self.C_QH = nHeaterStrips * [14.1E-3]  # Capacitance of the capacitor connected to the QH strip.
        self.R_warm_QH = nHeaterStrips * [0.50]  # Resistance of the warm leads of the QH strip discharge circuit.
        self.w_QH = nHeaterStrips * [15E-3]  # Width of the non-Cu-plated part of the the QH strip
        self.h_QH = nHeaterStrips * [25E-6]  # Height of the non-Cu-plated part of the QH strip.
        self.s_ins_QH = nHeaterStrips * [
            75E-6]  # Thickness of the insulation layer between QH strip and coil insulation layer.
        self.type_ins_QH = nHeaterStrips * [
            2]  # Type of material of the insulation layer between QH strip and coil insulation layer (1=G10; 2=kapton)
        # Thickness of the insulation layer between QH strip and the helium bath (or the collars); on this side, the QH strip is thermally connected to an infinite thermal sink at constant temperature.
        self.s_ins_QH_He = nHeaterStrips * [150E-6]
        self.type_ins_QH_He = nHeaterStrips * [
            2]  # Type of material of the insulation layer between QH strip and helium bath (1=G10; 2=kapton)
        self.l_QH = nHeaterStrips * [14.3]  # Length of the QH strip.
        self.f_QH = nHeaterStrips * [
            .12 / (.12 + .4)]  # Fraction of QH strip covered by heating stations (not-Cu-plated).

        # # # Heat exchange between quench heater strips and half-turns - DUMMY VALUES: THERE ARE NO QUENCH HEATERS
        self.iQH_toHalfTurn_To = [1]  # Thermal connections between heater strips and half-turns
        self.iQH_toHalfTurn_From = [1]

        # # # Adiabatic hot-spot temperature calculation
        # Time from which the adiabatic hot-spot temperature calculation starts. For each coil section, calculate the adiabatic hot-spot temperature in the highest-field strand/cable [s]
        self.tQuench = self.nCoilSectionsDefined * [0]
        self.initialQuenchTemp = self.nCoilSectionsDefined * [10]  # Initial quench temperature in the hot-spot temperature calculation [K]

        # # # Self-mutual inductance matrix between half-turns, and between coil sections
        # Set M_InductanceBlock_m to 0 to force LEDET to import the self-mutual inductances from the .csv file
        self.M_InductanceBlock_m = 0

        # Define to which inductive block each half-turn belongs
        self.HalfTurnToInductanceBlock = []
        for g in range(1, self.nGroupsDefined + 1):
            for j in range(self.nT[g - 1]):
                self.HalfTurnToInductanceBlock.append(g)

        # Calculate group to which each half-turn belongs
        indexTstart = np.hstack([1, 1 + np.cumsum(self.nT[:-1])])
        indexTstop = np.cumsum(self.nT)
        self.HalfTurnToGroup = np.zeros((1, self.nHalfTurnsDefined), dtype=int)
        self.HalfTurnToGroup = self.HalfTurnToGroup[0]
        self.HalfTurnToCoilSection = np.zeros((1, self.nHalfTurnsDefined), dtype=int)
        self.HalfTurnToCoilSection = self.HalfTurnToCoilSection[0]
        for g in range(1, self.nGroupsDefined + 1):
            self.HalfTurnToGroup[indexTstart[g - 1] - 1:indexTstop[g - 1]] = g
            self.HalfTurnToCoilSection[indexTstart[g - 1] - 1:indexTstop[g - 1]] = self.GroupToCoilSection[g - 1]

        # Calculate group to which each strand belongs
        indexSstart = np.hstack([1, 1 + np.cumsum(self.nS[:-1])])
        indexSstop = np.cumsum(self.nS)
        self.strandToGroup = np.zeros((1, self.nStrands), dtype=int)
        self.strandToGroup = self.strandToGroup[0]
        self.strandToCoilSection = np.zeros((1, self.nStrands), dtype=int)
        self.strandToCoilSection = self.strandToCoilSection[0]
        for ht in range(1, self.nHalfTurnsDefined + 1):
            self.strandToGroup[indexSstart[ht - 1] - 1:indexSstop[ht - 1]] = self.HalfTurnToGroup[ht - 1]
            self.strandToCoilSection[indexSstart[ht - 1] - 1:indexSstop[ht - 1]] = self.HalfTurnToCoilSection[ht - 1]

        self.columnsXY = [4, 5]
        self.columnsBxBy = [6, 7]
        self.flagPlotMTF = 0

        # Input Generation Options
        self.flag_calculateInductanceMatrix = 0
        self.flag_useExternalInitialization = 0
        self.flag_initializeVar = 0

        # Simulation Run Options
        self.flag_fastMode = 1
        self.flag_controlCurrent = 0
        self.flag_automaticRefinedTimeStepping = 1

        # Simulation Physics Options
        self.flag_IronSaturation = 0  # this was originally set to 1
        self.flag_InvertCurrentsAndFields = 0
        self.flag_ScaleDownSuperposedMagneticField = 1
        self.flag_HeCooling = 0  # was 2 TODO
        self.fScaling_Pex = 1
        self.fScaling_Pex_AlongHeight = self.fScaling_Pex_AlongHeight_Defined
        self.fScaling_MR = 1
        self.flag_scaleCoilResistance_StrandTwistPitch = 0
        self.flag_separateInsulationHeatCapacity = 0
        self.flag_ISCL = 0
        self.fScaling_Mif = 1
        self.fScaling_Mis = 0
        self.flag_StopIFCCsAfterQuench = 0
        self.flag_StopISCCsAfterQuench = 0
        self.tau_increaseRif = 0.005
        self.tau_increaseRis = 0.01
        self.fScaling_RhoSS = 1.09
        self.maxVoltagePC = 10
        self.flag_symmetricGroundingEE = 0
        self.flag_removeUc = 0
        self.BtX_background = 0
        self.BtY_background = 0

        # Post-Processing Options
        self.flag_showFigures = 0
        self.flag_saveFigures = 1
        self.flag_saveMatFile = 1
        self.flag_saveTxtFiles = 0
        self.flag_generateReport = 1
        self.flag_hotSpotTemperatureInEachGroup = 0
        self.MinMaxXY_MTF = [75, 125, -120, 120]

        self.suffixPlot = ["'_Temperature2D_'"]
        self.typePlot = [4]
        self.outputPlotSubfolderPlot = ["Temperature"]
        self.variableToPlotPlot = ["T"]
        self.selectedStrandsPlot = ["1:nStrands"]
        self.selectedTimesPlot = ["1:n_time"]
        self.labelColorBarPlot = ["'Temperature [K]'"]
        self.minColorBarPlot = ["min(min(variableToPlot))"]
        self.maxColorBarPlot = ["max(max(variableToPlot))"]
        self.MinMaxXYPlot = []
        self.flagSavePlot = [1]
        self.flagColorPlot = [1]
        self.flagInvisiblePlot = [1]

        # # # Define the values of all Variables variables - Change something only if you know what you're doing
        self.variableToSaveTxt = ['time_vector', 'Ia', 'Ib', 'T_ht', 'dT_dt_ht', 'flagQ_ht', 'IifX', 'IifY', 'Iis',
                                  'dIifXDt',
                                  'dIifYDt', 'dIisDt', 'Uc', 'U_QH', 'T_QH', 'time_vector', 'R_CoilSections',
                                  'U_inductive_dynamic_CoilSections']
        self.typeVariableToSaveTxt = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1]
        self.variableToInitialize = ['Ia', 'Ib', 'T_ht', 'dT_dt_ht', 'flagQ_ht', 'IifX', 'IifY', 'Iis', 'dIifXDt',
                                     'dIifYDt',
                                     'dIisDt', 'Uc', 'U_QH', 'T_QH']



        if self.verbose:
            print('Total number of strands in the field-map from ROXIE = {}'.format(self.nStrandsFieldMap))
            print('Peak magnetic field in the field-map from ROXIE = {} T'.format(np.max(self.B)))
            print('Total number of strands = ' + str(self.nStrands))
            print('Total number of half-turns = ' + str(self.nHalfTurns))
            print('Total number of turns = ' + str(self.nTurns))
            print('Total number of groups = ' + str(self.nGroups))
            print(str(self.nCoilSectionsDefined) + ' coil sections defined.')
            print(str(self.nGroupsDefined) + ' groups defined.')
            print(str(self.nHalfTurnsDefined) + ' half-turns defined.')

            print('fScaling_Pex_AlongHeight_Defined = ')
            print(self.fScaling_Pex_AlongHeight_Defined)

            print('The groups will be connected electrically in this order:')
            print(self.el_order_groups)

            print('Calculated electrical order of the half-turns:')
            print('el_order_half_turns = ' + str(self.el_order_half_turns))
            print('Heat exchange along the cable wide side - Calculated indices:')
            print('iContactAlongWidth_From = ')
            print(self.iContactAlongWidth_From)
            print('iContactAlongWidth_To = ')
            print(self.iContactAlongWidth_To)

            print('Heat exchange along the cable narrow side - Calculated indices:')
            print('iContactAlongHeight_From = ')
            print(self.iContactAlongHeight_From)
            print('iContactAlongWidth_To = ')
            print(self.iContactAlongHeight_To)

            print('iQH_toHalfTurn_From = {}'.format(self.iQH_toHalfTurn_From))
            print('iQH_toHalfTurn_To = {}'.format(self.iQH_toHalfTurn_To))
            print('Total magnet self-inductance: ' + str(self.M_m) + ' H')
            print(self.HalfTurnToInductanceBlock)
            # Visualize variable descriptions, names, and values
            print('### "Inputs" variables ###')
            self.paramLEDET.printVariableDescNameValue(self.paramLEDET.variableGroupInputs,
                                                       self.paramLEDET.variablesInputs)

            # Visualize variable descriptions, names, and values
            print('')
            print('### "Options" variables ###')
            self.paramLEDET.printVariableDescNameValue(self.paramLEDET.variableGroupOptions,
                                                       self.paramLEDET.variablesOptions)

            # Visualize variable descriptions, names, and values
            print('')
            print('### "Plots" variables ###')
            self.paramLEDET.printVariableDescNameValue(self.paramLEDET.variableGroupPlots,
                                                       self.paramLEDET.variablesPlots)

            # Visualize variable descriptions, names, and values
            print('')
            print('### "Variables" variables ###')
            self.paramLEDET.printVariableDescNameValue(self.paramLEDET.variableGroupVariables,
                                                       self.paramLEDET.variablesVariables)

        # # # Calculate approximate quench detection time in case the quench occurs in any half-turn

        self.paramLEDET = ParametersLEDET()  # Load default LEDET variable descriptions
        self.uQuenchDetectionThreshold = 0.1  # [V]# Define quench detection threshold
        self.iStartQuench = list(
            range(1, self.nHalfTurnsDefined + 1))  # Indices of the half-turns that are set to quench at a given time
        self.tStartQuench = [self._ttdf] * self.nHalfTurnsDefined  # Time at which each selected half-turn quenches [s]
        for i_SQ, t_SQ in zip(self.scenario_data['iStartQuench'], self.scenario_data['tStartQuench']):
            self.tStartQuench[i_SQ - 1] = t_SQ
        self.lengthHotSpot_iStartQuench = [10E-3] * self.nHalfTurnsDefined  # Length of the initial hot-spot [m] (it can be set to a large value to implement a full 2D model)
        self.vQ_iStartQuench = []

        # Add all Inputs variables to a list - DO NOT CHANGE
        self.paramLEDET.addVariablesInputs(
            self.T00, self.l_magnet, self.I00, self.M_m,
            self.fL_I, self.fL_L,
            self.GroupToCoilSection, self.polarities_inGroup, self.nT,
            self.nStrands_inGroup, self.l_mag_inGroup, self.ds_inGroup,
            self.f_SC_strand_inGroup, self.f_ro_eff_inGroup, self.Lp_f_inGroup,
            self.RRR_Cu_inGroup,
            self.SCtype_inGroup, self.STtype_inGroup, self.insulationType_inGroup,
            self.internalVoidsType_inGroup,
            self.externalVoidsType_inGroup,
            self.wBare_inGroup, self.hBare_inGroup, self.wIns_inGroup, self.hIns_inGroup,
            self.Lp_s_inGroup, self.R_c_inGroup,
            self.Tc0_NbTi_ht_inGroup, self.Bc2_NbTi_ht_inGroup,
            self.c1_Ic_NbTi_inGroup, self.c2_Ic_NbTi_inGroup,
            self.Tc0_Nb3Sn_inGroup, self.Bc2_Nb3Sn_inGroup, self.Jc_Nb3Sn0_inGroup,
            self.el_order_half_turns,
            self.alphasDEG, self.rotation_block, self.mirror_block, self.mirrorY_block,
            self.iContactAlongWidth_From, self.iContactAlongWidth_To,
            self.iContactAlongHeight_From,
            self.iContactAlongHeight_To,
            self.iStartQuench, self.tStartQuench, self.lengthHotSpot_iStartQuench,
            self.vQ_iStartQuench,
            self.R_circuit, self.R_crowbar, self.Ud_crowbar, self.t_PC, self.t_PC_LUT, self.I_PC_LUT,
            self.tEE, self.R_EE_triggered,
            self.tCLIQ, self.directionCurrentCLIQ, self.nCLIQ, self.U0, self.C, self.Rcapa,
            self.tQH, self.U0_QH, self.C_QH, self.R_warm_QH, self.w_QH, self.h_QH, self.s_ins_QH, self.type_ins_QH,
            self.s_ins_QH_He, self.type_ins_QH_He, self.l_QH, self.f_QH,
            self.iQH_toHalfTurn_From, self.iQH_toHalfTurn_To,
            self.tQuench, self.initialQuenchTemp,
            self.HalfTurnToInductanceBlock, self.M_InductanceBlock_m
        )

        # Add all Options variables to a list - DO NOT CHANGE
        self.paramLEDET.addVariablesOptions(
            self.time_vector_params,
            self.Iref, self.flagIron, self.flagSelfField, self.headerLines, self.columnsXY, self.columnsBxBy,
            self.flagPlotMTF,
            self.flag_calculateInductanceMatrix, self.flag_useExternalInitialization, self.flag_initializeVar,
            self.flag_fastMode, self.flag_controlCurrent, self.flag_automaticRefinedTimeStepping,
            self.flag_IronSaturation,
            self.flag_InvertCurrentsAndFields, self.flag_ScaleDownSuperposedMagneticField, self.flag_HeCooling,
            self.fScaling_Pex,
            self.fScaling_Pex_AlongHeight,
            self.fScaling_MR, self.flag_scaleCoilResistance_StrandTwistPitch, self.flag_separateInsulationHeatCapacity,
            self.flag_ISCL, self.fScaling_Mif, self.fScaling_Mis, self.flag_StopIFCCsAfterQuench,
            self.flag_StopISCCsAfterQuench, self.tau_increaseRif,
            self.tau_increaseRis,
            self.fScaling_RhoSS, self.maxVoltagePC, self.flag_symmetricGroundingEE, self.flag_removeUc,
            self.BtX_background, self.BtY_background,
            self.flag_showFigures, self.flag_saveFigures, self.flag_saveMatFile, self.flag_saveTxtFiles,
            self.flag_generateReport,
            self.flag_hotSpotTemperatureInEachGroup, self.flag_typeWindings, self.MinMaxXY_MTF
        )

        # Define the values of all Plots variables - DO NOT CHANGE
        self.paramLEDET.addVariablesPlots(
            self.suffixPlot, self.typePlot, self.outputPlotSubfolderPlot, self.variableToPlotPlot,
            self.selectedStrandsPlot, self.selectedTimesPlot,
            self.labelColorBarPlot, self.minColorBarPlot, self.maxColorBarPlot, self.MinMaxXYPlot, self.flagSavePlot,
            self.flagColorPlot, self.flagInvisiblePlot
        )

        # Define the values of all Variables variables - DO NOT CHANGE
        self.paramLEDET.addVariablesVariables(
            self.variableToSaveTxt, self.typeVariableToSaveTxt, self.variableToInitialize
        )
        self.text = {'x': [], 'y': [], 't': []}

        self.paramLEDET.adjust_vQ(self.field_map_file)
        self.vQ_iStartQuench = list(self.paramLEDET.getAttribute("Inputs",
                                                                 "vQ_iStartQuench"))  # Quench propagation velocity [m/s] (you can write 2x higher velocity if the quench propagates in two directions)

        # Set the location and time of the quench
        # halfTurn_start_quench = 1
        # time_start_quench = -0.05
        # tStartQuench[halfTurn_start_quench-1] = time_start_quench

        # Calculate resistance of each turn at T=10 K
        rho_Cu_10K = 1.7E-10  # [Ohm*m] Approximate Cu resistivity at T=10 K, B=0, for RRR=100
        rho_Cu_10K_B = 4E-11  # [Ohm*m/T] Approximate Cu magneto-resistivity factor
        self.rho_ht_10K = []
        self.r_el_ht_10K = []
        self.mean_B_ht = []
        self.tQuenchDetection = []
        for ht in range(1, self.nHalfTurns + 1):
            current_group = self.HalfTurnToGroup[ht - 1]
            mean_B = np.mean(
                self.B[np.where(
                    self.strandToHalfTurn == ht)]) / self.Iref * self.I00  # average magnetic field in the current half-turn
            rho_mean = rho_Cu_10K + rho_Cu_10K_B * mean_B  # average resistivity in the current half-turn
            cross_section = self.nStrands_inGroup[current_group - 1] * np.pi / 4 * self.ds_inGroup[
                current_group - 1] ** 2 * (1 - self.f_SC_strand_inGroup[current_group - 1])
            r_el_m = rho_mean / cross_section  # Electrical resistance per unit length
            tQD = self.uQuenchDetectionThreshold / (self.vQ_iStartQuench[
                                                        ht - 1] * r_el_m * self.I00)  # Approximate time to reach the quench detection threshold
            self.mean_B_ht = np.hstack([self.mean_B_ht, mean_B])
            self.rho_ht_10K = np.hstack([self.rho_ht_10K, rho_mean])
            self.r_el_ht_10K = np.hstack([self.r_el_ht_10K, r_el_m])
            self.tQuenchDetection = np.hstack([self.tQuenchDetection, tQD])


    def write_ledet_input(self):
        """
        Writes LEDET input excel file to disk
        """
        excel_file_path = os.path.join(self.magnet_folder, f"{self.magnet_name}_{int(self.model_no)}.xlsx")
        self.paramLEDET.writeFileLEDET(excel_file_path, SkipConsistencyCheck=self.consistency_checks)  # Write the LEDET input file
        print(f"LEDET inputs written to {excel_file_path}")

    def write_quench_v(self):
        np.savetxt(os.path.join(self.m.magnet_folder, f"{self.magnet_name}vQ_I00.csv"), self.vQ_iStartQuench,
                   delimiter=",")
        if self.verbose:
            print(f'Minimum quench detection time = {min(self.tQuenchDetection * 1e3)} ms')
            print(f'Maximum quench detection time = {max(self.tQuenchDetection * 1e3)} ms')
            print(f"File {self.magnet_name}vQ_I00.csv with calculated quench propagation velocities was written")

    def plotter(self, data, titles, labels, types, texts, size):
        """
        Default plotter for most standard and simple cases
        """
        fig, axs = plt.subplots(nrows=1, ncols=len(data), figsize=size)
        if len(data) == 1:
            axs = [axs]
        for ax, ty, d, ti, l, te in zip(axs, types, data, titles, labels, texts):
            if ty == 'scatter':
                plot = ax.scatter(d['x'], d['y'], s=2, c=d['z'], cmap='jet')  # =cm.get_cmap('jet'))
                if len(te["t"]) != 0:
                    for x, y, z in zip(te["x"], te["y"], te["t"]):
                        ax.text(x, y, z)
            elif ty == 'plot':
                pass  # TODO make non scatter plots work. Some of non-scater plots are quite specific. Might be better off with a separate plotter
            ax.set_xlabel(l["x"], **self.selectedFont)
            ax.set_ylabel(l["y"], **self.selectedFont)
            ax.set_title(f'{ti}', **self.selectedFont)
            # ax.set_aspect('equal')
            # ax.figure.autofmt_xdate()
            cax = make_axes_locatable(ax).append_axes('right', size='5%', pad=0.05)
            cbar = fig.colorbar(plot, cax=cax, orientation='vertical')
            if len(l["z"]) != 0:
                cbar.set_label(l["z"], **self.selectedFont)
        plt.tight_layout()
        plt.show()

    def plot_field(self):
        """
        Plot magnetic field components of a coil
        """
        data = [{'x': self.x, 'y': self.y, 'z': self.I},
                {'x': self.x, 'y': self.y, 'z': self.Bx},
                {'x': self.x, 'y': self.y, 'z': self.By},
                {'x': self.x, 'y': self.y, 'z': self.B}]
        titles = ['Current [A]', 'Br [T]', 'Bz [T]', 'Bmod [T]']
        labels = [{'x': "r (m)", 'y': "z (m)", 'z': ""}] * len(data)
        types = ['scatter'] * len(data)
        texts = [self.text] * len(data)
        self.plotter(data, titles, labels, types, texts, (15, 5))

    def plot_strands_groups_layers(self):
        types = ['scatter'] * 4
        data = [{'x': self.x, 'y': self.y, 'z': self.strandToHalfTurn},
                {'x': self.x, 'y': self.y, 'z': self.strandToGroup},
                {'x': self.x, 'y': self.y, 'z': self.halfTurnToTurn},
                {'x': self.x, 'y': self.y, 'z': self.nS}]
        titles = ['strandToHalfTurn', 'strandToGroup', 'halfTurnToTurn', 'Number of strands per half-turn']
        labels = [{'x': "r (m)", 'y': "z (m)", 'z': "Half-turn [-]"},
                  {'x': "r (m)", 'y': "z (m)", 'z': "Group [-]"},
                  {'x': "r (m)", 'y': "z (m)", 'z': "Turn [-]"},
                  {'x': "r (m)", 'y': "z (m)", 'z': "Number of  strands per cable [-]"}]
        t_ht = copy.deepcopy(self.text)
        for ht in range(self.nHalfTurns):
            t_ht['x'].append(self.x_ave[ht])
            t_ht['y'].append(self.y_ave[ht])
            t_ht['t'].append('{}'.format(ht + 1))
        t_ng = copy.deepcopy(self.text)
        for g in range(self.nGroups):
            t_ng['x'].append(self.x_ave_group[g])
            t_ng['y'].append(self.y_ave_group[g])
            t_ng['t'].append('{}'.format(g + 1))
        texts = [t_ht, t_ng, self.text, self.text]
        self.plotter(data, titles, labels, types, texts, (15, 5))

    def plot_polarities(self):
        polarities_inStrand = np.zeros((1, self.nStrands), dtype=int)
        polarities_inStrand = polarities_inStrand[0]
        for g in range(1, self.nGroupsDefined + 1):
            polarities_inStrand[np.where(self.strandToGroup == g)] = self.polarities_inGroup[g - 1]
        data = [{'x': self.x, 'y': self.y, 'z': polarities_inStrand}]
        titles = ['Current polarities']
        labels = [{'x': "r (m)", 'y': "z (m)", 'z': "Polarity [-]"}]
        types = ['scatter'] * len(data)
        texts = [self.text] * len(data)
        self.plotter(data, titles, labels, types, texts, (5, 5))

    def plot_half_turns(self):
        data = [{'x': self.x_ave, 'y': self.y_ave, 'z': self.HalfTurnToGroup},
                {'x': self.x_ave, 'y': self.y_ave, 'z': self.HalfTurnToCoilSection},
                {'x': self.x, 'y': self.y, 'z': self.strandToGroup},
                {'x': self.x, 'y': self.y, 'z': self.strandToCoilSection}]
        titles = ['HalfTurnToGroup', 'HalfTurnToCoilSection', 'StrandToGroup', 'StrandToCoilSection']
        labels = [{'x': "r (m)", 'y': "z (m)", 'z': "Group [-]"},
                  {'x': "r (m)", 'y': "z (m)", 'z': "Coil section [-]"},
                  {'x': "r (m)", 'y': "z (m)", 'z': "Group [-]"},
                  {'x': "r (m)", 'y': "z (m)", 'z': "Coil Section [-]"}]
        types = ['scatter'] * len(data)
        texts = [self.text] * len(data)
        self.plotter(data, titles, labels, types, texts, (15, 5))

    def plot_nonlin_induct(self):
        f = plt.figure(figsize=(7.5, 5))
        plt.plot(self.fL_I, self.fL_L, 'ro-')
        plt.xlabel('Current [A]', **self.selectedFont)
        plt.ylabel('Factor scaling nominal inductance [-]', **self.selectedFont)
        plt.title('Differential inductance versus current', **self.selectedFont)
        plt.xlim([0, self.I00 * 2])
        plt.grid(True)
        plt.rcParams.update({'font.size': 12})
        plt.show()

    def plot_psu_and_trig(self):
        # Plot
        f = plt.figure(figsize=(7.5, 5))
        plt.plot([self.t_PC, self.t_PC], [0, 1], 'k--', linewidth=4.0, label='t_PC')
        plt.plot([self.tEE, self.tEE], [0, 1], 'r--', linewidth=4.0, label='t_EE')
        plt.plot([self.tCLIQ, self.tCLIQ], [0, 1], 'g--', linewidth=4.0, label='t_CLIQ')
        plt.plot([np.min(self.tQH), np.min(self.tQH)], [0, 1], 'b:', linewidth=2.0, label='t_QH')
        plt.xlabel('Time [s]', **self.selectedFont)
        plt.ylabel('Trigger [-]', **self.selectedFont)
        plt.xlim([1E-4, self.time_vector_params[-1]])
        plt.title('Power suppply and quench protection triggers', **self.selectedFont)
        plt.grid(True)
        plt.rcParams.update({'font.size': 12})
        plt.legend(loc='best')
        plt.tight_layout()
        plt.show()

    def plot_quench_prop_and_resist(self):
        f = plt.figure(figsize=(16, 6))
        plt.subplot(1, 4, 1)
        # fig, ax = plt.subplots()
        plt.scatter(self.x_ave * 1000, self.y_ave * 1000, s=2, c=self.vQ_iStartQuench)
        plt.xlabel('x [mm]', **self.selectedFont)
        plt.ylabel('y [mm]', **self.selectedFont)
        plt.title('2D cross-section Quench propagation velocity', **self.selectedFont)
        plt.set_cmap('jet')
        plt.grid('minor', alpha=0.5)
        cbar = plt.colorbar()
        cbar.set_label('Quench velocity [m/s]', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        # plt.axis('equal')

        plt.subplot(1, 4, 2)
        plt.scatter(self.x_ave * 1000, self.y_ave * 1000, s=2, c=self.rho_ht_10K)
        plt.xlabel('x [mm]', **self.selectedFont)
        plt.ylabel('y [mm]', **self.selectedFont)
        plt.title('Resistivity', **self.selectedFont)
        plt.set_cmap('jet')
        plt.grid('minor', alpha=0.5)
        cbar = plt.colorbar()
        cbar.set_label('Resistivity [$\Omega$*m]', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        # plt.axis('equal')

        plt.subplot(1, 4, 3)
        plt.scatter(self.x_ave * 1000, self.y_ave * 1000, s=2, c=self.r_el_ht_10K)
        plt.xlabel('x [mm]', **self.selectedFont)
        plt.ylabel('y [mm]', **self.selectedFont)
        plt.title('Resistance per unit length', **self.selectedFont)
        plt.set_cmap('jet')
        plt.grid('minor', alpha=0.5)
        cbar = plt.colorbar()
        cbar.set_label('Resistance per unit length [$\Omega$/m]', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        # plt.axis('equal')

        plt.subplot(1, 4, 4)
        plt.scatter(self.x_ave * 1000, self.y_ave * 1000, s=2, c=self.tQuenchDetection * 1e3)
        plt.xlabel('x [mm]', **self.selectedFont)
        plt.ylabel('y [mm]', **self.selectedFont)
        plt.title('Approximate quench detection time', **self.selectedFont)
        plt.set_cmap('jet')
        plt.grid('minor', alpha=0.5)
        cbar = plt.colorbar()
        cbar.set_label('Time [ms]', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        # plt.axis('equal')
        plt.show()

    def plot_q_prop_v(self):
        f = plt.figure(figsize=(16, 6))
        plt.subplot(1, 2, 1)
        plt.plot(self.mean_B_ht, self.vQ_iStartQuench, 'ko')
        plt.xlabel('Average magnetic field in the half-turn [T]', **self.selectedFont)
        plt.ylabel('Quench propagation velocity [m/s]', **self.selectedFont)
        plt.title('Quench propagation velocity', **self.selectedFont)
        plt.set_cmap('jet')
        plt.grid('minor', alpha=0.5)
        plt.rcParams.update({'font.size': 12})
        plt.subplot(1, 2, 2)
        plt.plot(self.mean_B_ht, self.tQuenchDetection * 1e3, 'ko')
        plt.xlabel('Average magnetic field in the half-turn [T]', **self.selectedFont)
        plt.ylabel('Approximate quench detection time [ms]', **self.selectedFont)
        plt.title('Approximate quench detection time', **self.selectedFont)
        plt.set_cmap('jet')
        plt.grid('minor', alpha=0.5)
        plt.rcParams.update({'font.size': 12})
        plt.show()

    def plot_electrical_order(self):
        plt.figure(figsize=(16, 8))
        plt.subplot(1, 3, 1)
        plt.scatter(self.x_ave, self.y_ave, s=2, c=np.argsort(self.el_order_half_turns_Array))
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
        plt.plot(self.x_ave[self.el_order_half_turns_Array - 1], self.y_ave[self.el_order_half_turns_Array - 1], 'k')
        plt.scatter(self.x_ave, self.y_ave, s=2, c=self.nS)
        plt.scatter(self.x_ave[self.el_order_half_turns_Array[0] - 1],
                    self.y_ave[self.el_order_half_turns_Array[0] - 1], s=50, c='r',
                    label='Positive lead')
        plt.scatter(self.x_ave[self.el_order_half_turns_Array[-1] - 1],
                    self.y_ave[self.el_order_half_turns_Array[-1] - 1], s=50, c='b',
                    label='Negative lead')
        plt.xlabel('x [m]', **self.selectedFont)
        plt.ylabel('y [m]', **self.selectedFont)
        plt.title('Electrical order of the half-turns', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        plt.axis('equal')
        plt.legend(loc='lower left')
        # Plot
        plt.subplot(1, 3, 3)
        # plt.plot(x_ave_group[elPairs_GroupTogether_Array[:,0]-1],y_ave_group[elPairs_GroupTogether_Array[:,1]-1],'b')
        plt.scatter(self.x, self.y, s=2, c='k')
        plt.scatter(self.x_ave_group, self.y_ave_group, s=10, c='r')
        plt.xlabel('x [m]', **self.selectedFont)
        plt.ylabel('y [m]', **self.selectedFont)
        plt.title('Electrical order of the groups (only go-lines)', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        plt.axis('equal')
        plt.show()

    def plot_heat_exchange_order(self):
        plt.figure(figsize=(10, 10))
        # plot strand positions
        plt.scatter(self.x, self.y, s=2, c='b')
        # plot conductors
        # for c, (cXPos, cYPos) in enumerate(zip(xPos, yPos)):
        #     pt1, pt2, pt3, pt4 = (cXPos[0], cYPos[0]), (cXPos[1], cYPos[1]), (cXPos[2], cYPos[2]), (cXPos[3], cYPos[3])
        #     line = plt.Polygon([pt1, pt2, pt3, pt4], closed=True, fill=True, facecolor='r', edgecolor='k', alpha=.25)
        #     plt.gca().add_line(line)
        # plot average conductor positions
        # plt.scatter(x_ave, y_ave, s=10, c='r')
        # plot heat exchange links along the cable narrow side
        for i in range(len(self.iContactAlongHeight_From)):
            plt.plot([self.x_ave[self.iContactAlongHeight_From_Array[i] - 1],
                      self.x_ave[self.iContactAlongHeight_To_Array[i] - 1]],
                     [self.y_ave[self.iContactAlongHeight_From_Array[i] - 1],
                      self.y_ave[self.iContactAlongHeight_To_Array[i] - 1]], 'k')
        # plot heat exchange links along the cable wide side
        for i in range(len(self.iContactAlongWidth_From)):
            plt.plot([self.x_ave[self.iContactAlongWidth_From_Array[i] - 1],
                      self.x_ave[self.iContactAlongWidth_To_Array[i] - 1]],
                     [self.y_ave[self.iContactAlongWidth_From_Array[i] - 1],
                      self.y_ave[self.iContactAlongWidth_To_Array[i] - 1]], 'r')
        # plot strands belonging to different conductor groups and clo ser to each other than max_distance
        # for p in pairs_close:
        #     if not strandToGroup[p[0]] == strandToGroup[p[1]]:
        #         plt.plot([X[p[0], 0], X[p[1], 0]], [X[p[0], 1], X[p[1], 1]], c='g')
        plt.xlabel('x [m]', **self.selectedFont)
        plt.ylabel('y [m]', **self.selectedFont)
        plt.title('Heat exchange order of the half-turns', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        plt.axis('equal')
        plt.show()

    def plot_power_supl_contr(self):
        plt.figure(figsize=(5, 5))
        plt.plot([self.t_PC, self.t_PC], [np.min(self.I_PC_LUT), np.max(self.I_PC_LUT)], 'k--', linewidth=4.0,
                 label='t_PC')
        plt.plot(self.t_PC_LUT, self.I_PC_LUT, 'ro-', label='LUT')
        plt.xlabel('Time [s]', **self.selectedFont)
        plt.ylabel('Current [A]', **self.selectedFont)
        plt.title('Look-up table controlling power supply', **self.selectedFont)
        plt.grid(True)
        plt.rcParams.update({'font.size': 12})
        plt.show()

    def plot_all(self):
        self.plot_field()
        self.plot_polarities()
        self.plot_strands_groups_layers()
        self.plot_electrical_order()
        self.plot_q_prop_v()
        self.plot_quench_prop_and_resist()
        self.plot_psu_and_trig()
        self.plot_half_turns()
        self.plot_heat_exchange_order()
        self.plot_nonlin_induct()
        self.plot_power_supl_contr()

    def run_LEDET(self, LEDET_exe_full_path):
        RunSimulations(self.base_folder, LEDET_exe_full_path, self.nameCircuit, Simulations=self.model_no,
                       RunSimulations=False)
        LEDET_exe_path = os.path.join(self.base_folder, LEDET_exe_full_path)
        os.chdir(self.base_folder)
        subprocess.call([LEDET_exe_path])


if __name__ == "__main__":
    n = NB_LEDET("Dummy", 2, output_folder=r"E:\LEDET\LEDET_v2_01_10", recalc_field=True)

    n.write_ledet_input()
    # n.plot_field()
    # n.plot_polarities()
    # n.plot_strands_groups_layers()
    # n.plot_electrical_order()
    # n.plot_q_prop_v()
    # n.plot_quench_prop_and_resist()
    # n.plot_psu_and_trig()
    # n.plot_half_turns()
    # n.plot_heat_exchange_order()
    # n.plot_nonlin_induct()
    # n.plot_power_supl_contr()
    #n.plot_all()