from steam_nb_api.sing.ParametersCOSIM import ParametersCOSIM
from steam_nb_api.utils.misc import makeCopyFile
import datetime
import csv
import os
from pathlib import Path
import numpy as np
import yaml
import shutil
import json
from steam_nb_api.ledet.ParameterSweep import *

def _read_yaml(type_str, elem_name):
    """
    Reads yaml file and returns it as dictionary
    :param type_str: type of file, e.g.: quench, coil, wire
    :param elem_name: file name, e.g. ColSol.1
    :return: dictionary for file named: type.name.yam
    """
    fullfileName = os.path.join(os.getcwd(), f"{type_str}.{elem_name}.yaml")
    with open(fullfileName, 'r') as stream:
        data = yaml.safe_load(stream)
    return data

@dataclass
class Options:
    t_0: np.ndarray = np.array([0,1,2])
    t_end: np.ndarray = np.array([1,2,3])
    t_step_max: np.ndarray = np.array([[0.0005,0.001,0.001]]*2)
    relTolerance: np.ndarray = np.array([1e-4,None])
    absTolerance: np.ndarray = np.array([1,None])
    executionOrder: np.ndarray = np.array([1,2])
    executeCleanRun: np.ndarray = np.array([True, True])

class MP3_setup:
    def __checkOptions(self):
        for key in self.Options.__annotations__:
            if isinstance(self.Options.__getattribute__(key), list):
                tempv = np.array(self.Options.__getattribute__(key))
                self.Options.__setattr__(key, tempv)
            elif isinstance(self.Options.__getattribute__(key), np.ndarray):
                continue
            else:
                print(key + ' in Options, Data-type not understood. Abort.')

    def __autoConstructOptions(self, N_LEDET):
        if N_LEDET > 1:
            self.Options.t_step_max = np.vstack((self.Options.t_step_max, [self.Options.t_step_max.tolist()[-1]]*(N_LEDET-1)))
            self.Options.relTolerance = np.append(self.Options.relTolerance, [self.Options.relTolerance.tolist()[-1]]*(N_LEDET-1))
            self.Options.absTolerance = np.append(self.Options.absTolerance,
                                                  [self.Options.absTolerance.tolist()[-1]] * (N_LEDET-1))
            self.Options.executionOrder = np.append(self.Options.executionOrder,
                                                  [self.Options.executionOrder.tolist()[-1]] * (N_LEDET-1))
            self.Options.executeCleanRun = np.append(self.Options.executeCleanRun,
                                                    [self.Options.executeCleanRun.tolist()[-1]] * (N_LEDET-1))
        return

    def __init__(self, circuit, ParameterFile, Opts = [], enableQuench = 0):
        # Folder and Executables
        self.path_PSPICELib = ''
        self.path_NotebookLib = ''
        self.PspiceExecutable = ''
        self.LedetExecutable = ''
        self.CosimExecutable = ''
        self.ModelFolder = ''
        self.ResultFolder = ''
        self.EOS_stub_C = ''

        self.ParameterFile = ParameterFile

        self.circuit = circuit
        self.transient = ''

        if Opts:
            self.flag_Options = 0
            self.Options = Opts
            self.__checkOptions()
        else:
            self.Options = Options()
            self.flag_Options = 1
        self.enableQuench = enableQuench
        self.QuenchMagnet = 0
        self.ManualStimuli = []

        return

    def load_config(self, file):
        config_dict = _read_yaml('config', file)
        self.path_PSPICELib = config_dict['LibraryFolder']
        self.path_NotebookLib = config_dict['NotebookFolder']
        self.PspiceExecutable = config_dict['PSpiceExecutable']
        self.LedetExecutable = config_dict['LEDETExecutable']
        self.CosimExecutable = config_dict['COSIMExecutable']
        self.ModelFolder = config_dict['ModelFolder']
        self.ResultFolder = config_dict['ResultFolder']
        self.EOS_stub_C = config_dict['EOS_SynchronizationFolder']

        if os.getcwd().startswith('C'):
            self.ModelFolder_EOS = self.ModelFolder
        else:
            EOS_stub_EOS = os.environ['SWAN_HOME']
            self.ModelFolder_EOS = self.ModelFolder.replace(self.EOS_stub_C, EOS_stub_EOS)
            self.ModelFolder_EOS = self.ModelFolder_EOS.replace('\\','//')
            self.path_NotebookLib = self.path_NotebookLib.replace(self.EOS_stub_C, EOS_stub_EOS)
            self.path_NotebookLib = self.path_NotebookLib.replace('\\', '//')
        return

    def _loadParameterFile(self):
        with open(self.ParameterFile, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            row_parameter = []
            values = []
            parameter_dict = {}

            line_count = 0
            for row in csv_reader:
                if line_count == 0: row_parameter = row
                if row[0] == self.circuit: values = row
                line_count = line_count + 1
            for i in range(1,len(row_parameter)):
                try:
                    parameter_dict[row_parameter[i]] = float(values[i])
                except:
                    parameter_dict[row_parameter[i]] = values[i]

        return parameter_dict

    def SetUpSimulation(self, transient, Current, Append: bool = False, ManualCircuit: str = '', ManualStimuli: list = []):
        self.transient = transient
        parameter_dict = self._loadParameterFile()

        if ManualStimuli:
            self.ManualStimuli = ManualStimuli

        if not isinstance(Current, list):
            Current = [Current]

        Folder = []
        for i in range(len( Current)):
            I00 = Current[i]
            parameter_dict['I00'] = I00

            if parameter_dict['NumberOfMagnets']>1:
                try:
                    MagnetName = json.loads(parameter_dict['MagnetName'])
                    N_LEDET = len(MagnetName)
                except:
                    N_LEDET = 2
            else:
                N_LEDET = 1

            Sim_Flag = parameter_dict['flag_COSIM']
            if Sim_Flag:
                if self.flag_Options and i==0: self.__autoConstructOptions(N_LEDET)
                CoilSections = json.loads(parameter_dict['CoilSections'])
                if not ManualCircuit: circuit_file = self.__findCircuit(self.circuit)
                else: circuit_file = ManualCircuit
                COSIMfolder = self._setUp_COSIM(N_LEDET, CoilSections, circuit_file, parameter_dict)
            else:
                COSIMfolder = self._setUp_LEDETonly(parameter_dict)
            Folder.append(COSIMfolder)

        newModelCosim = ParametersCOSIM('1', '1', '1')
        if Sim_Flag:
            newModelCosim.writeCOSIMBatch(Folder, self.CosimExecutable,
                                          Destination=os.path.abspath(os.path.join(self.ModelFolder_EOS, os.pardir)), Append = Append)
        else:
            newModelCosim.writeCOSIMBatch(Folder, self.CosimExecutable,
                                          Destination=os.path.abspath(os.path.join(self.ModelFolder_EOS, os.pardir)),
                                          LEDET_exe=self.LedetExecutable, Append = Append)

    def __obtainCircuitParameters(self, circuit, new_circuit):
        parameter = {}
        f = open(circuit,'r')
        g = open(new_circuit, 'w')
        flag_On = 0
        for line in f:
            if line.startswith('.PARAM') or line.startswith(' .PARAM') and not 'S' in line:
                flag_On = 1
            elif flag_On and not line.startswith('+'):
                flag_On = 0
            if '+' in line[:10] and not line.startswith('*') and not 'PARAMS' in line and flag_On :
                para = line[line.index('+') + 1:line.index('=')].replace(' ', '')
                parameter[para] = 0
            else:
                g.write(line)
            if '_Quench' in line: self.QuenchMagnet = 1
        return parameter

    def __manipulateCircuit(self, circuit, parameter_dict, Stimuli):
         # 1. Write the params back into .cir
        f = open(circuit, 'r')
        new_lines = []
        flag_unbalancedFPA = 0
        if isinstance(Stimuli, list):
            flag_unbalancedFPA = 1
            StimuliCounter = 0
        for line in f:
            if line.startswith('I_PC') or line.startswith(' I_PC') and not self.ManualStimuli:
                idx = line.index('STIMULUS')
                if flag_unbalancedFPA:
                    ll = line[:idx] + " STIMULUS = " + Stimuli[StimuliCounter] + '\n'
                    StimuliCounter = StimuliCounter +1
                else:
                    ll = line[:idx]+" STIMULUS = "+ Stimuli+'\n'
                line = ll
                new_lines.append(line)
            elif line.startswith('.PARAM') or line.startswith(' .PARAM'):
                new_lines.append(line)
                for key in parameter_dict.keys():
                    if key == 'PowerConverter': continue
                    nl = '+ '+str(key)+'={'+str(parameter_dict[key])+'}\n'
                    new_lines.append(nl)
            elif line.startswith('.LIB') or line.startswith(' .LIB'):
                nel = line.replace("C:\\cernbox\\steam-pspice-library\\", self.path_PSPICELib)
                new_lines.append(nel)
            elif line.startswith('x_PC') or line.startswith(' x_PC'):
                try:
                    PC = parameter_dict['PowerConverter']
                    idx = line.index(')')
                    ll = line[:idx+2] + str(PC) + '\n'
                    line = ll
                    new_lines.append(line)
                except:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        # 2. Include new options
        ## TODO
        g = open(circuit, 'w')
        g.writelines(new_lines)
        return

    def __findCircuit(self, circuitName):
        idx = circuitName.index('.')
        fam = circuitName[:idx]
        sourcedir = os.listdir(os.path.join(self.path_NotebookLib,'steam-sing-input'))
        for f in sourcedir:
            if os.path.isfile(f): continue
            else:
                files = os.listdir(os.path.join(self.path_NotebookLib,'steam-sing-input',f))
                for k in files:
                    if k.startswith(fam) and k.endswith('Cosim.cir'):
                        return os.path.join(self.path_NotebookLib,'steam-sing-input',f,k)
        print('No circuit file found for' + circuitName + ' [' + fam + '] ')

    def __generateStimuliCOSIM(self, StimulusFile, transient, current_level, t_Start, t_PC):
        if transient == 'FPA' and not self.ManualStimuli:
            Stimuli =  "I_FPA_" + str(current_level)
            stlString = ".STIMULUS I_FPA_" + str(current_level) + " PWL" + "\n"
            stlString = stlString + "+ TIME_SCALE_FACTOR = 1 \n"
            stlString = stlString + "+ VALUE_SCALE_FACTOR = 1 \n"
            stlString = stlString + "+ ( " + str(t_Start)+"s,  " + str(current_level) + "A )\n"
            stlString = stlString + "+ ( " + str(t_PC)+"s,  " + str(current_level) + "A )\n"
            stlString = stlString + "+ ( " + str(t_PC+0.001)+"s,  0A )\n"
            stlString = stlString + "+ ( 70.00000s,  0A )\n"
            stlString = stlString + "\n"
            with open(StimulusFile, 'a') as file:
                file.write(stlString)
        elif transient == 'unbalancedFPA' and not self.ManualStimuli:
            Stimuli = []
            stlString = ''
            for i in range(len(current_level)):
                cl = current_level[i]
                Stimuli.append("I_FPA_" +str(cl))
                stlString = stlString + ".STIMULUS I_FPA_" + str(cl) + " PWL" + "\n"
                stlString = stlString + "+ TIME_SCALE_FACTOR = 1 \n"
                stlString = stlString + "+ VALUE_SCALE_FACTOR = 1 \n"
                stlString = stlString + "+ ( " + str(t_Start) + "s,  " + str(cl) + "A )\n"
                stlString = stlString + "+ ( " + str(t_PC) + "s,  " + str(cl) + "A )\n"
                stlString = stlString + "+ ( " + str(t_PC + 0.001) + "s,  0A )\n"
                stlString = stlString + "+ ( 70.00000s,  0A )\n"
                stlString = stlString + "\n"
            with open(StimulusFile, 'a') as file:
                file.write(stlString)
        elif self.ManualStimuli:
            Stimuli = []
            stlString = ''
            for i in range(len(self.ManualStimuli)):
                cl = current_level[i]
                stim = self.ManualStimuli[i]
                Stimuli.append(str(self.ManualStimuli[i]))
                stlString = stlString + ".STIMULUS " + str(self.ManualStimuli[i]) + " PWL" + "\n"
                stlString = stlString + "+ TIME_SCALE_FACTOR = 1 \n"
                stlString = stlString + "+ VALUE_SCALE_FACTOR = 1 \n"
                stlString = stlString + "+ ( " + str(t_Start) + "s,  " + str(cl) + "A )\n"
                stlString = stlString + "+ ( " + str(t_PC) + "s,  " + str(cl) + "A )\n"
                stlString = stlString + "+ ( " + str(t_PC + 0.001) + "s,  0A )\n"
                stlString = stlString + "+ ( 70.00000s,  0A )\n"
                stlString = stlString + "\n"
            with open(StimulusFile, 'a') as file:
                file.write(stlString)
        else:
            print('Transient is not supported yet. Abort!')
            return
        return Stimuli

    def _setUp_COSIM(self, N_LEDET, CoilSections, circuit, parameter_dict):
        current_level = parameter_dict['I00']
        try:
            MagnetName = json.loads(parameter_dict['MagnetName'])
            DistinctMagnets = len(MagnetName)
        except:
            MagnetName = parameter_dict['MagnetName']
            DistinctMagnets = 1

        if self.enableQuench:
            quenchTitle = '_Quench'
        else: quenchTitle = ''

        if isinstance(current_level, list):
            cl = ''
            for i in range(len(current_level)):
                cl = cl + str(current_level[i])+"A"
        else: cl = str(current_level)+"A"

        ModelFolder_EOS = os.path.join(self.ModelFolder_EOS, 'COSIM_model_' + self.circuit + "_" + self.transient + "_" +
                                            str(cl) +quenchTitle)
        ModelFolder_C = self.ModelFolder + 'COSIM_model_' + self.circuit + "_" + self.transient + "_" + str(cl) +quenchTitle
        ResultFolder_C = self.ResultFolder + self.circuit + "_" + self.transient + "_" + str(cl) +quenchTitle+'\\'
        COSIMfolder = ModelFolder_C

        if len(MagnetName)!= N_LEDET: Magnets = [MagnetName] * N_LEDET
        else: Magnets = MagnetName

        newModelCosim = ParametersCOSIM(ModelFolder_EOS, nameMagnet= Magnets , nameCircuit=self.circuit)
        newModelCosim.makeAllFolders(N_LEDET=N_LEDET)

        # 1. Obtain parameter to change
        new_circuit = os.path.join(ModelFolder_EOS, 'PSpice','Circuit.cir')
        parameter_cir = self.__obtainCircuitParameters(circuit, new_circuit)
        # 2. link parameter to parameter list
        cop_parameter_dict = deepcopy(parameter_dict)
        for key in parameter_dict.keys():
            if key not in parameter_cir.keys():
                del cop_parameter_dict[key]
            else:
                parameter_cir[key] = cop_parameter_dict[key]

        try:
            parameter_cir['PowerConverter'] = parameter_dict['PowerConverter']
        except:
            pass

        if isinstance(MagnetName,list):
            if len(MagnetName) == 2:
                if MagnetName[0] == MagnetName[1] and self.QuenchMagnet: DistinctMagnets = 1

        # 3. Generate Stimuli file
        StimulusFile =  os.path.join(ModelFolder_EOS, 'PSpice','ExternalStimulus.stl')
        t_Start = parameter_dict['t_Start']
        t_PC = parameter_dict['t_PC']
        Stimuli = self.__generateStimuliCOSIM(StimulusFile, self.transient, current_level, t_Start, t_PC)

        # 4. Change .cir file
        self.__manipulateCircuit(new_circuit, parameter_cir, Stimuli)

        # 5. Generate Input/Output etc.
        newModelCosim.copyConfigFiles(N_LEDET=N_LEDET)
        newModelCosim.makeGenericIOPortFiles(CoilSections, ModelFolder_C, ResultFolder_C,
                                             self.PspiceExecutable, self.LedetExecutable, t_0=self.Options.t_0.tolist(), t_end=self.Options.t_end.tolist(),
                                             t_step_max=self.Options.t_step_max.tolist(), relTolerance=self.Options.relTolerance.tolist(),
                                             absTolerance=self.Options.absTolerance.tolist(),
                                             executionOrder=self.Options.executionOrder.tolist(), executeCleanRun=self.Options.executeCleanRun.tolist(),
                                             N_LEDET=N_LEDET, QuenchMagnet=self.QuenchMagnet, DistinctMagnets=DistinctMagnets)

        LEDETfiles = newModelCosim.copyCOSIMfiles(new_circuit, StimulusFile, Magnets, N_LEDET=N_LEDET, ManuallyStimulusFile = StimulusFile)
        prepareLEDETFiles = newModelCosim.prepareLEDETFiles(LEDETfiles, N_PAR=N_LEDET)

        for file in prepareLEDETFiles:
            par_dict = deepcopy(parameter_dict)
            if self.transient == 'unbalancedFPA':
                del par_dict['I00']
            self._manipulateLEDETExcel(file, par_dict)
            if len(prepareLEDETFiles) > 1: self.enableQuench = 0
        currentDT = datetime.datetime.now()
        print('COSIM_model_' + self.circuit + "_" + self.transient + "_" +
                                            str(cl) + " generated.")
        print('Time stamp: ' + str(currentDT))
        print(' ')
        return COSIMfolder

    def __generateStimuliLEDET(self, parameter_dict):
        if self.transient == 'FPA':
            current_level = parameter_dict['I00']
            t_PC = parameter_dict['t_PC']
            t_Start = parameter_dict['t_Start']

            I_LUT = [current_level, current_level, 0]
            t_LUT = [t_Start, t_PC, t_PC+0.001]

            parameter_dict["I_PC_LUT"] = I_LUT
            parameter_dict["t_PC_LUT"] = t_LUT
        else:
            print(self.transient+' is not supported yet. Abort!')
        return parameter_dict

    def _setUp_LEDETonly(self, parameter_dict):
        current_level = parameter_dict['I00']
        MagnetName = parameter_dict['MagnetName']

        ModelFolder_EOS = os.path.join(self.ModelFolder_EOS, 'LEDET_model_' + self.circuit + "_" + self.transient + "_" +
                                            str(current_level) + "A")

        ModelFolder_C = self.ModelFolder + 'LEDET_model_' + self.circuit + "_" + self.transient + "_" + str(current_level) + "A"
        COSIMfolder = str(MagnetName) + '_L_' + ModelFolder_C
        newModelCosim = ParametersCOSIM(ModelFolder_EOS, nameMagnet=MagnetName, nameCircuit=self.circuit)
        newModelCosim.makeAllFolders(N_LEDET=1, LEDET_only=1)
        LEDETfiles = newModelCosim.copyCOSIMfiles('0', '0', MagnetName, N_LEDET=1, LEDET_only=1)
        nameFileLEDET = os.path.join(ModelFolder_EOS, "LEDET", "LEDET", MagnetName, "Input", MagnetName + "_0.xlsx")

        parameter_dict = self.__generateStimuliLEDET(parameter_dict)
        if not "flag_saveMatFile" in parameter_dict.keys():
            parameter_dict["flag_saveMatFile"] = 1
        if not "flag_generateReport" in parameter_dict.keys():
            parameter_dict["flag_generateReport"] = 1
        self._manipulateLEDETExcel(nameFileLEDET, parameter_dict)

        # Display time stamp and end run
        currentDT = datetime.datetime.now()
        print(' ')
        print('LEDET_model_' + self.circuit + "_" + self.transient + "_" +
                                            str(current_level) + "A generated.")
        print('Time stamp: ' + str(currentDT))
        return COSIMfolder

    def __generateImitate(self, PL, classvalue, value):
        if type(classvalue) == np.ndarray and len(classvalue) > 1 and len(PL.Inputs.nT)==len(classvalue):
            v = deepcopy(classvalue)
            v = np.where(PL.Inputs.polarities_inGroup != 0, value, v)
        elif type(classvalue) == np.ndarray and len(classvalue) > 1:
            v = np.array([value]*len(classvalue))
        elif type(classvalue) == np.ndarray:
            v = np.array([value])
        else:
            v = value
        return v

    def _manipulateLEDETExcel(self, file, parameter_dict):
        PL = ParametersLEDET()
        PL.readLEDETExcel(file, verbose = False)

        for key in parameter_dict.keys():
            if key in PL.Inputs.__annotations__:
                if not isinstance(parameter_dict[key], list):
                    values = self.__generateImitate(PL, PL.getAttribute(getattr(PL, 'Inputs'), key), parameter_dict[key])
                elif len(parameter_dict[key])==1:
                    values = self.__generateImitate(PL, PL.getAttribute(getattr(PL, 'Inputs'), key), parameter_dict[key])
                else: values = parameter_dict[key]
                PL.setAttribute('Inputs', key, values)
            if key in PL.Options.__annotations__:
                PL.setAttribute("Options", key, parameter_dict[key])

        if self.enableQuench:
            if parameter_dict['Quench']:
                i_qT = int(parameter_dict['i_qT'])
                t_Q = parameter_dict['t_Q']
                tStartQuench = [9999] * len(PL.Inputs.tStartQuench)
                tStartQuench[i_qT - 1] = t_Q
        else:
            tStartQuench = [9999] * len(PL.Inputs.tStartQuench)
        PL.setAttribute("Inputs", "tStartQuench", tStartQuench)

        PL.writeFileLEDET(file, verbose = False)
