import os
import numpy as np
import yaml
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
        strand_ins_rad_size = self.conductor['strand']['hBare_inGroup'] + 2 * self.conductor['strand']['hIns_inGroup']
        strand_ins_ax_size = self.conductor['strand']['wBare_inGroup'] + 2 * self.conductor['strand']['wIns_inGroup']
        self.n_layers = int(np.rint((self.sol_dict['A2'] - self.sol_dict['A1']) / strand_ins_rad_size))
        self.n_turns_per_layer = int(np.rint((self.sol_dict['B2'] - self.sol_dict['B1']) / strand_ins_ax_size))
        self.tot_n_turns = self.n_turns_per_layer * self.n_layers

        f_layer_m_t_r = self.sol_dict['A1'] + strand_ins_rad_size / 2  # first layer middle turn radial position
        l_layer_m_t_r = f_layer_m_t_r + (self.n_layers - 1) * strand_ins_rad_size  # last layer middle turn radial position
        r_pos = np.linspace(f_layer_m_t_r, l_layer_m_t_r, self.n_layers,
                            endpoint=True)  # layers middle turns radial positions
        f_layer_m_t_z = self.sol_dict['B1'] + strand_ins_ax_size / 2  # first layer middle turn axial position
        l_layer_m_t_z = f_layer_m_t_z + (self.n_turns_per_layer - 1) * strand_ins_ax_size  # last layer middle turn axial position
        z_pos = np.linspace(f_layer_m_t_z, l_layer_m_t_z, self.n_turns_per_layer,
                            endpoint=True)  # layers middle turns axial positions
        self.rr_pos, self.zz_pos = np.meshgrid(r_pos, z_pos)

        self.rr_pos = self.rr_pos.T
        self.zz_pos = self.zz_pos.T

        self.Rin = np.linspace(self.sol_dict['A1'], self.sol_dict['A1'] + (self.n_layers - 1) * strand_ins_rad_size,
                               self.n_layers, endpoint=True)  # layers start turns radial positions
        self.Rout = self.Rin + strand_ins_rad_size  # layers end turns radial positions
        self.Zlow = np.ones_like(self.Rin) * self.sol_dict['B1']  # layers start axial positions
        self.Zhigh = np.ones_like(self.Rin) * self.sol_dict['B2']  # layers end axial positions
        self.Is = np.ones_like(self.Rin) * 0  # layers current
        self.Nturns = np.ones_like(self.Rin, dtype=np.int32) * self.n_turns_per_layer  # layers number of turns

class Solenoid_magnet:
    def __init__(self, magnet_name):
        self.magnet_data = _read_yaml('magnet', magnet_name)
        for block_name, block_dict in self.magnet_data['blocks'].items():
            self.magnet_data['blocks'][block_name]['wire'] = _read_yaml('conductor', block_dict['wire'])
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
        self.wires = [mag_dat['wire'] for  mag_dat in _read_yaml('magnet', magnet_name)['blocks'].values()]
        self.wire_groups = []
        for idx, n in enumerate(np.concatenate([sol.n_layers for sol in pysol_data], axis=None)):
            self.wire_groups = self.wire_groups + [idx+1] * n

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