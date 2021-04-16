from steam_nb_api.ledet.ParameterSweep import *
from steam_nb_api.ledet.ParametersLEDET import ParametersLEDET
from steam_nb_api.ledet.ParametersLEDET import *
from steam_nb_api.ledet.NotebookLEDET_V2 import *
import pandas as pd
from steam_nb_api.ledet.Simulation import RunSimulations
from steam_nb_api.ledet.SimulationEvaluation import EvaluateSimulations
from steam_nb_api.ledet.QuenchAnalysis import QuenchPlanAnalysis
from steam_nb_api.ledet.AutomaticSweep import AutomaticSweep
import time

from steam_nb_api.utils.MP3_simulations import *

testfile1 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MBRC\MBRC_0.xlsx"
testfile2 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MBRB\MBRB_0.xlsx"
testfile3 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MBRS\MBRS_0.xlsx"
testfile4 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MBX\MBX_0.xlsx"
testfile5 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MCD\MCD_0.xlsx"
testfile6 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MCO\MCO_0.xlsx"
testfile7 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MO_1AP\MO_1AP_8magBB_0.xlsx"
testfile8 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MCBXH\MCBXH_CopperWedges_ThCool_0.xlsx"
testfile9 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MCBXV\MCBXV_CopperWedges_ThCool_0.xlsx"
testfile10 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MCBXV\MCBXV_CopperWedges_0.xlsx"
testfile11 = "C:\cernbox\TEMP2\MCBY_1AP_CopperWedges_ThCool_29.xlsx"
testfile12 = "C:\cernbox\LEDET\LEDET\MCBY_1AP_CopperWedges_ThCool\Input\MCBY_1AP_CopperWedges_ThCool_35.xlsx"
testfile13 = "C:\cernbox\LEDET_MT\LEDET\MQXFS4b\Input\MQXFS4b_23.xlsx"
testfile14 = "C:\cernbox\MasterThesis\MQY studies\MQY_2in1_Ref.xlsx"

ledetFolder = 'C:\\cernbox\\LEDET_OS\\'
ledetExe = 'LEDET_v1_08_03.exe'

def CompleteRun():
    start = time.time()
    a = ParametersLEDET()
    a.readLEDETExcel(testfile13)
    Sw = MinMaxSweep(a, 6)
    MagnetName = 'MQXFS4b'

    # ##MQXF, 6 base points
    Sw.addParameterToSweep('tau_increaseRis', 0.001, 0.2)
    Sw.addParameterToSweep('Rcapa', 0.00001, 0.1)
    Sw.addParameterToSweep('tau_increaseRif', 0.001, 0.2)


    ##13mag
    # Sw.addParameterToSweep('l_magnet', 4.16, 5.2)
    # Sw.addParameterToSweep('f_ro_eff_inGroup', 1, 3)
    # Sw.addParameterToSweep('RRR_Cu_inGroup', 100, 300)

    # ##MBX/ MRBC/ MBRS/ MBRB
    # Sw.addParameterToSweep('f_ro_eff_inGroup', 1, 3, basePoints = 3)
    # Sw.addParameterToSweep('R_c_inGroup', -6, -3, type='logarithmic', basePoints= 3)
    # Sw.addHeliumCrossSection(0, 6, basePoints= 4)
    # Sw.addParameterToSweep('RRR_Cu_inGroup', 35, 200, basePoints=6)

    ##8mag
    # Sw.addParameterToSweep('l_magnet', 0.056, 0.14)
    # Sw.addParameterToSweep('f_ro_eff_inGroup', 1, 3)
    # Sw.addParameterToSweep('RRR_Cu_inGroup', 100, 300)
    # Sw.addHeliumCrossSection(3, 6, basePoints=4)

    ## MCBXH_CopperWedges -1
    # Sw.addParameterToSweep('f_ro_eff_inGroup', 0.1, 3)
    # Sw.addParameterToSweep('RRR_Cu_inGroup', 100, 300)
    # Sw.addParameterToSweep('l_magnet', 0.056, 0.14)
    # Sw.addQuenchSweep("tStartQuench",[1,1,1,1,1,1],[-0.2, -0.21, -0.22, -0.23, -0.24, -0.25])
    # Sw.addQuenchSweep("tStartQuench", [[1, 730],[321,1050],[1, 730],[321,1050],[1, 730],[321,1050],[1, 730],[321,1050]],
    #                   [[-0.2, -0.182],[-0.2, -0.182],[-0.15, -0.132],[-0.15, -0.132],[-0.1, -0.082],[-0.2, -0.082],[-0.05, -0.032],[-0.05, -0.032]])

    ##MCBY
    # Sw.addParameterToSweep('f_ro_eff_inGroup', 1, 3)
    # Sw.addParameterToSweep('RRR_Cu_inGroup', 100, 300)

    ## Current Sweep
    # Sw.addCurrentSweep(6650, 30)

    Sw.generatePermutations()
    end = time.time()
    print("Time:", end-start)
    start = time.time()
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\\LEDET_MT\\LEDET\\MQXFS4b\\Input\\",OffsetNumber=100)
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\LEDET\\LEDET\\MBRC\\Input\\")
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\LEDET\\LEDET\\MCD\\Input\\")
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\LEDET\\LEDET\\MCO\\Input\\")
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\LEDET\\LEDET\\MO_1AP\\Input\\")
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\LEDET\\LEDET\\MCBXH_CopperWedges_ThCool\\Input\\")
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\LEDET\\LEDET\\MCBXV_CopperWedges_ThCool\\Input\\")
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\\TEMP2\\", OffsetNumber= 42, ROXIE_File='C:\\cernbox\\SWAN_projects\\steam-notebooks\\steam-ledet-input\\MCBXV\\MCBXV_CopperWedges_All_WithIron_WithSelfField.map2d')
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\\TEMP2\\", OffsetNumber=17, ROXIE_File='C:\\cernbox\\SWAN_projects\\steam-notebooks\\steam-ledet-input\\MCBY_1AP\\MCBY_1AP_CopperWedges_ThCool_All_WithIron_WithSelfField.map2d')
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\\TEMP\\", OffsetNumber=50)
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\\TEMP\\")


    end = time.time()
    print("Time:", end - start)
    print("Preparation done")

    # SimNumbers = np.linspace(50,265, 216).astype(int)

    # RunSimulations(ledetFolder, ledetExe, MagnetName, Simulations = SimNumbers, RunSimulations=False)
    # EvaluateSimulations("C:\\cernbox\\LEDET\\LEDET\\MCO\\Output\\Txt Files", 'MCO',
    #                     'C:\\cernbox\\Validation_MCDO\\Exp Data\\RCO.A56B1_2018-03-16_PM_I_A_AutoAlign.csv',
    #                     Sw, Mat=False, SkipAlign=True)
    # EvaluateSimulations("C:\\cernbox\\LEDET\\LEDET\\MCD\\Output\\Txt Files", 'MCD',
    #                     'C:\\cernbox\\Validation_MCDO\\Exp Data\\RCD.A56B1_2018-03-16_PM_I_A_AutoAlign.csv',
    #                     Sw, Mat=False, SkipAlign=True)
    # EvaluateSimulations('C:\cernbox\LEDET\LEDET_SimulationFiles_Quench\LEDET\MBRS\Output\Txt Files', 'MBRS',
    #                      'C:\cernbox\Validation_IPD\Validation MBRS\Exp Data\RD3.R4_20181203_135959_IA - Cut.csv',
    #                     Sw, Mat=False, SkipAlign=True)
    # EvaluateSimulations('C:\cernbox\LEDET\LEDET\MBRC\Output\Txt Files', 'MBRC',
    #                      'C:\cernbox\Validation_IPD\Validation MBRC\Exp Data\RD2.L8_20181203_131307_IA - Cut.csv',
    #                     Sw, Mat=False)
    # EvaluateSimulations('C:\\cernbox\\Validation_MO\\Validation\\LEDET\\FullB2', 'MO_1AP', 'C:\\cernbox\\LHC-SM-API\\ROD_ROF\\ROD.A12B2_PM_I_A.csv',
    #                     Sw, Mat=False)
    # EvaluateSimulations('C:\\cernbox\\Validation_MO\\Validation\\LEDET\\FullB1', 'MO_1AP',
    #                     'C:\\cernbox\\LHC-SM-API\\ROD_ROF\\ROD.A12B1_PM_I_A.csv',
    #                      Sw, Mat=False)
    # EvaluateSimulations('C:\\cernbox\\Validation_MCBX_HV\\LEDET Validation\\1st Sweep-RRR_fro_tQ\\Output\\Txt Files', 'MCBXH_CopperWedges',
    #                     'C:\\cernbox\\Validation_MCBX_HV\\Exp Data\\RCBXH1.R1_2018-03-11_PM_I_ARAW.csv',
    #                      Sw, Mat=False)
    # EvaluateSimulations('C:\\cernbox\\Validation_MCBX_HV\\LEDET Validation\\2nd Sweep-RRR_fro_tQ_THCOOL\\Output\\Txt Files',
    #                     'MCBXH_CopperWedges_ThCool', 'C:\\cernbox\\Validation_MCBX_HV\\Exp Data\\RCBXH1.R1_2018-03-11_PM_I_ARAW.csv',
    #                      Sw, Mat=False, showBestFit = 20)
    # EvaluateSimulations("C:\\cernbox\\TEMP\\",
    #                     'MCBXV_CopperWedges_ThCool', 'C:\\cernbox\\Validation_MCBX_HV\\Exp Data\\RCBXV2.R1_2017-04-20_PM_I_ARAW.csv',
    #                      Sw, Mat=False)
    # EvaluateSimulations("C:\\cernbox\\TEMP2\\",
    #                     'MCBXH_CopperWedges_ThCool',
    #                     'C:\\cernbox\\Validation_MCBX_HV\\Exp Data\\RCBXH1.R1_2018-03-11_PM_I_ARAW.csv',
    #                     Sw, Mat=False)
    EvaluateSimulations("C:\\cernbox\\LEDET_OS\\LEDET\\MQXFS4b\\Output\\Txt Files",
                        MagnetName,
                        'C:\\cernbox\\MasterThesis\\Test23_ParSweepMeas.csv',
                        Sw, Mat=False)

def AutomaticRun():
    LEDETFolder = 'C:\\cernbox\LEDET\\LEDET_SimulationFiles_Quench'
    LEDETExe = 'LEDET_v1_07_01_6February2020.exe'
    MagnetName = 'MO_1AP'
    MeasFile = 'C:\cernbox\LHC-SM-API\ROD_ROF\ROD.A12B2_PM_I_A.csv'
    SetUpFile = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MO_1AP\MO_1AP_8magBB_0.xlsx"

    ASw = AutomaticSweep(8, SetUpFile, LEDETFolder, LEDETExe, MagnetName, MeasFile)
    ASw.addParameterToSweep('l_magnet', 2.56, 4.8)
    ASw.addParameterToSweep('f_ro_eff_inGroup', 1, 3)
    ASw.addParameterToSweep('RRR_Cu_inGroup', 100, 300)
    #ASw.AutomaticRun(101)

    ASw.LearnAndTrainAll()
    return ASw

def testConsistencyChecks():
    a = ParametersLEDET()
    a.readLEDETExcel(testfile10)
    x = a._consistencyCheckLEDET()
    print(x)

def testvQ():
    nameFileLEDET = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MQXA\MQXA_0.xlsx"
    # nameFileLEDET = 'C:\cernbox\LEDET_MT\LEDET\MQXFBP2\Input\MQXFBP2_10.xlsx'
    RoxieFile = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MQXA\MQXA_All_WithIron_WithSelfField.map2d"
    # RoxieFile = "C:\cernbox\LEDET_MT\Field Maps\MQXFBP2\MQXFBP2_All_WithIron_WithSelfField.map2d"
    # RoxieFile = "C:\\cernbox\\LEDET_MT\\Field Maps\\MQXFBP2\\"
    a = ParametersLEDET()
    a.readLEDETExcel(nameFileLEDET)
    [vQ, l, th_con_h, delta_t_h, th_con_w, delta_t_w] = a.adjust_vQ(RoxieFile)
    return a

def testQuenchPlanAnalysis(FileName_TDMS, FileName_Sim, verbose = True):
    Coil108 = {'C108_I1_I2':[],
               'C108_I2_I3':np.concatenate((np.linspace(29, 45, 17), np.linspace(229, 245, 17))),
               'C108_I3_I4':np.concatenate((np.linspace(46, 49, 4), np.linspace(246, 249, 4))),
               'C108_I4_I5':[],
               'C108_I5_I6':np.array([50]),
               'C108_I6_I7':[],
               'C108_I7_I8':np.array([250]),
               'C108_I8_O1':[],
               'C108_O1_O2':[],
               'C108_O2_O3':np.array([28]),
               'C108_O3_O4':[],
               'C108_O4_O5':np.array([228]),
               'C108_O5_O6':np.concatenate((np.linspace(17, 27, 11), np.linspace(217, 227, 11))),
               'C108_O6_O7':np.concatenate((np.linspace(1, 16, 16), np.linspace(201, 216, 16))),
               'C108_O7_O8':[]}
    Coil109 = {'C109_I1_I2':[],
               'C109_I2_I3':np.concatenate((np.linspace(329, 345, 17), np.linspace(129, 145, 17))),
               'C109_I3_I4':np.concatenate((np.linspace(146, 149, 4), np.linspace(346, 349, 4))),
               'C109_I4_I5':[],
               'C109_I5_I6':np.array([150]),
               'C109_I6_I7':[],
               'C109_I7_I8':np.array([350]),
               'C109_I8_O1':[],
               'C109_O1_O2':[],
               'C109_O2_O3':np.array([128]),
               'C109_O3_O4':[],
               'C109_O4_O5':np.array([328]),
               'C109_O5_O6':np.concatenate((np.linspace(117, 127, 11), np.linspace(317, 327, 11))),
               'C109_O6_O7':np.concatenate((np.linspace(101, 116, 16), np.linspace(301, 316, 16))),
               'C109_O7_O8':[]}
    Coil110 = {'C110_I1_I2':[],
               'C110_I2_I3':np.concatenate((np.linspace(79, 95, 17), np.linspace(279, 295, 17))),
               'C110_I3_I4':np.concatenate((np.linspace(96, 99, 4), np.linspace(296, 299, 4))),
               'C110_I4_I5':[],
               'C110_I5_I6':np.array([100]),
               'C110_I6_I7':[],
               'C110_I7_I8':np.array([300]),
               'C110_I8_O1':[],
               'C110_O1_O2':[],
               'C110_O2_O3':np.array([78]),
               'C110_O3_O4':[],
               'C110_O4_O5':np.array([278]),
               'C110_O5_O6':np.concatenate((np.linspace(267, 277, 11), np.linspace(67, 77, 11))),
               'C110_O6_O7':np.concatenate((np.linspace(51, 66, 16), np.linspace(251, 266, 16))),
               'C110_O7_O8':[]}
    Coil111 = {'C111_I1_I2':[],
               'C111_I2_I3':np.concatenate((np.linspace(179, 195, 17), np.linspace(379, 395, 17))),
               'C111_I3_I4':np.concatenate((np.linspace(196, 199, 4), np.linspace(396, 399, 4))),
               'C111_I4_I5':[],
               'C111_I5_I6':np.array([200]),
               'C111_I6_I7':[],
               'C111_I7_I8':np.array([400]),
               'C111_I8_O1':[],
               'C111_O1_O2':[],
               'C111_O2_O3':np.array([178]),
               'C111_O3_O4':[],
               'C111_O4_O5':np.array([378]),
               'C111_O5_O6':np.concatenate((np.linspace(367, 377, 11), np.linspace(167, 177, 11))),
               'C111_O6_O7':np.concatenate((np.linspace(151, 166, 16), np.linspace(351, 366, 16))),
               'C111_O7_O8':[]}
    a = QuenchPlanAnalysis(FileName_TDMS, FileName_Sim, verbose = verbose)
    # a = QuenchPlanAnalysis(0, FileName_Sim)
    # a.ProvideTurnsToCoilStructure(Coil = [Coil109,Coil110,Coil111,Coil108])
    # a.ProvideTurnsToCoilStructure(CoilCsv = 'C:\cernbox\MasterThesis\CoilStructure_MQXFPB2.csv')
    a.ProvideTurnsToCoilStructure(CoilCsv='C:\cernbox\MasterThesis\CoilStructure_MQXFS4b.csv')
    # a.QuenchPlanAnalysis(Plot = 1)
    # a.FindQuenchTDMS(0.1, 0.007, Plot=1)
    # a.PlotVoltageTap(Coil = 110)
    # a.PlotVoltageTap(TapName = 'C109_I2_I3')
    # a.calculateAllQuenchIntegrals()
    # a.calculateAllQuenchIntegrals(TDMS = 0)
    # a.calculateAllQuenchIntegrals(SIM = 0)
    return a

def PrepareSimulations():
    # PlanFile = "C:\cernbox\MasterThesis\MQFBP2 Test\MQXFBP2_QuenchPlan_Masterfile.xlsx"
    # RefFile = "C:\cernbox\MasterThesis\MQFBP2 Test\MQXFBP2_Ref_0.xlsx"
    PlanFile = "C:\cernbox\MasterThesis\MQY studies\QuenchPlan_MQY.xlsx"
    RefFile = "C:\cernbox\MasterThesis\MQY studies\MQY_2in1_Ref.xlsx"
    OutputDirectory = "C:\cernbox\TEMP"

    a = QuenchPlanAnalysis(0, 0)
    a.PrepareSimulations(PlanFile, RefFile, OutputDirectory,
                         QHpairs=[], nQHseries = 4)

def testLEDETnotebook():
    new_notebook = Notebook_LEDET('MBRB')


    T00 = 4.5
    l_magnet = 9.45
    I00 = 5800  # Current to be simulated
    new_notebook.setAttribute('GroupToCoilSection', new_notebook.nGroups * [1])
    new_notebook.setAttribute('I00', I00)

    new_notebook.load_ConductorData(['Type2','Type2'],[1,2]*int(new_notebook.nGroups/2))
    elPairs_GroupTogether = [[1, 17], [2, 18], [3, 19], [4, 20], [5, 21], [6, 22], [7, 23], [8, 24], [9, 25], [10, 26],
                             [11, 27], [12, 28], [13, 29], [14, 30], [15, 31], [16, 32]]
    elPairs_RevElOrder = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    new_notebook.set_ElectricalOrder(elPairs_GroupTogether, elPairs_RevElOrder)

    max_distance = 0.5E-3
    new_notebook.set_ThermalConnections(max_distance)

    new_notebook.load_Options('Default')

    # Resistance of the warm parts of the circuit [Ohm]
    R_circuit = 7.76E-4
    # Resistance of crowbar of the power supply [Ohm]
    R_crowbar = 5.6E-5
    # Forward voltage drop of a diode or thyristor in the crowbar of the power supply [V]
    Ud_crowbar = 0.34

    t_PC = 0
    tStart = -0.02
    Transient = 'FPA'


    # R_EE_triggered = 0.066
    # tEE = 99999

    # # Time when the CLIQ system is triggered [s]
    # tCLIQ = 99999
    # # Direction of the introduced current change for the chosen CLIQ configuration
    # directionCurrentCLIQ = [1]
    # # Number of CLIQ units
    # nCLIQ = 1
    # # CLIQ charging voltage [V]
    # U0 = 1000
    # # Capacitance of the CLIQ capacitor bank [F]
    # C = 0.04
    # # Resistance of the CLIQ leads [Ohm]
    # Rcapa = 0.05

    # Number of quench heater strips to write in the file
    nHeaterStrips = 8
    # Number of QH circuits
    nQHcircuits = 2
    # Time at which the power supply connected to the QH strip is triggered (Low-field QHs set to a very large value to avoid triggering).
    tQH = nHeaterStrips * [.002]
    # Charging voltage of the capacitor connected to the QH strip.
    U0_QH = nHeaterStrips * [900 / nQHcircuits]
    # Capacitance of the capacitor connected to the QH strip.
    C_QH = nHeaterStrips * [7.05E-3 * nQHcircuits]
    # Resistance of the warm leads of the QH strip discharge circuit.
    R_warm_QH = nHeaterStrips * [
        0.2 * nQHcircuits]  # 0.25-->0.28 Ohm partially compensates the fact that the real strip is 9.646 m long instead of l_magnet=9.450 m long
    # Width of the non-Cu-plated part of the the QH strip.
    w_QH = nHeaterStrips * [15E-3]
    # Height of the non-Cu-plated part of the QH strip.
    h_QH = nHeaterStrips * [0.025E-3]
    # Thickness of the insulation layer between QH strip and coil insulation layer.
    s_ins_QH = nHeaterStrips * [75E-6]
    # Type of materialof the insulation layer between QH strip and coil insulation layer (1=G10; 2=kapton)
    type_ins_QH = nHeaterStrips * [2]
    # Thickness of the insulation layer between QH strip and the helium bath (or the collars); on this side, the QH strip is thermally connected to an infinite thermal sink at constant temperature.
    s_ins_QH_He = nHeaterStrips * [500E-6]
    # Type of material of the insulation layer between QH strip and helium bath (1=G10; 2=kapton)
    type_ins_QH_He = nHeaterStrips * [2]
    # Length of the QH strip.
    l_QH = nHeaterStrips * [l_magnet]
    # Fraction of QH strip covered by heating stations (not-Cu-plated).
    f_QH = nHeaterStrips * [.127 / (.127 + .633)]

    # Heat exchange between quench heater strips and half-turns
    iQH_toHalfTurn_From_oneHalfQuadrant = [1, 1, 1, 1, 1, 1, 1, 1]
    iQH_toHalfTurn_To_oneHalfQuadrant = [1, 2, 3, 4, 5, 6, 7, 8]

    nHalfTurnsDefined = new_notebook.nHalfTurns
    nHalfQuadrants = 8
    # Inclination of cables with respect to X axis (including transformations for mirror and rotation)
    alphasDEG = nHalfQuadrants * [0, 1.2404, 2.4808, 3.7212, 4.9616, 6.202, 7.4424, 8.6828, 9.9232, 0, 1.2404, 2.4808,
                                  3.7212, 4.9616, 6.202, 7.4424, 8.6828, 9.9232, 11.1636, 12.404, 0, 1.2404, 2.4808,
                                  3.7212, 4.9616, 6.202, 7.4424, 8.6828, 0, 1.2404, 2.4808, 3.7212]
    # Rotate cable by a certain angle [deg]
    rotation_block = int(nHalfTurnsDefined / 8) * [0] + int(nHalfTurnsDefined / 8) * [180] + int(
        nHalfTurnsDefined / 8) * [0] + int(nHalfTurnsDefined / 8) * [180] + int(nHalfTurnsDefined / 8) * [90] + int(
        nHalfTurnsDefined / 8) * [270] + int(nHalfTurnsDefined / 8) * [90] + int(nHalfTurnsDefined / 8) * [270]
    # Mirror cable along the bisector of its quadrant (0=no, 1=yes)
    mirror_block = int(nHalfTurnsDefined / 2) * [0] + int(nHalfTurnsDefined / 2) * [1]
    # Mirror cable along the Y axis (0=no, 1=yes)
    mirrorY_block = nHalfTurnsDefined * [0]

    # Copy/paste the values after calculation using ROXIE or COMSOL or another software
    fL_I = [0, 60.5, 511.225, 961.95, 1412.675, 1863.4, 2314.125, 2764.85, 3215.575, 3666.3, 4117.025, 4567.75,
            5018.475, 5469.2, 5919.925, 6370.65, 6821.375, 7272.1, 7722.825, 8173.55, 8624.275, 9075]
    fL_L = [1.50847185630795, 1.50847185630795, 1.50847185630795, 1.50846737882912, 1.50841522306793, 1.50830395909222,
            1.50822527083526, 1.50806904802754, 1.50787422001269, 1.50745689700945, 1.50645441147256, 1.50388608565927,
            1.49507688502376, 1.47034904670854, 1.4380027616657, 1.40295544163306, 1.35977890716088, 1.30439619675877,
            1.23307412316907, 1.17633437683201, 1.14099904228627, 1.11820344760328]

    # Time Vector Definition. Parameters used to generate the time vector.
    # Each triplet of numbers defines a time window: first element is the start time, second element is the time step in that window, third element is the end time. It must contain a number of elements multiple of 3. Any time point above t=1000 s will be ignored.
    time_vector_params = [tStart, 5E-4, 0, 5E-4, 5E-4, 0.5, 0.501, 0.001, 1]

    # Time from which the adiabatic hot-spot temperature calculation starts. For each coil section, calculate the adiabatic hot-spot temperature in the highest-field strand/cable [s]
    tQuench = tStart
    # Initial quench temperature in the hot-spot temperature calculation [K]
    initialQuenchTemp = 10

    # Further stuff
    new_notebook.set_SimulationType('2D+1D')
    new_notebook.load_VariablesToStore('Default')
    new_notebook.load_PlotOptions('Default')
    new_notebook.storeVariables(locals())

    new_notebook.initiateQuench([1,5,10],[0.1,0.2,3], lengthHotspot=[2,3,4])
    new_notebook.setHeliumFraction(2)
    new_notebook.includeBusbar(5000)

    # Finish up
    nameMagnet = 'MBRB'
    nameFileLEDET = nameMagnet + '_TEST_0' + '.xlsx'
    new_notebook.writeLEDETFile(nameFileLEDET, locals())

    new_notebook.plot_all()

    return new_notebook

def test_persCurrents():
    a = ParametersLEDET()
    a.readLEDETExcel( "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MQXF_V2\MQXF_V2_0.xlsx")
    a.Inputs.fitParameters_inGroup = np.ones((3, 32))
    a.Inputs.df_inGroup = np.ones((32,)).transpose()
    a.Inputs.selectedFit_inGroup = np.ones((32,)).transpose()
    # a.Options.flag_persistentCurrents = 1
    a.writeFileLEDET('A.xlsx')
    return a

def test_persCurrents2():
    a = ParametersLEDET()
    a.readLEDETExcel( "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MQXF_V2\MQXF_V2_0.xlsx")
    dIdt = 6.8
    timeStep = 0.5

    nameFileLEDET_PS = 'abc_200' + '.xlsx'
    PS_paramLEDET = deepcopy(a)
    PS_paramLEDET.localsParser(locals())
    I00 = a.Inputs.I00
    I_PC_LUT = [0, 0, I00, I00, -I00, -I00, I00, I00, -I00, -I00, 0, 0]
    PS_paramLEDET.preparePersistentCurrents(I_PC_LUT, dIdt, timeStep)
    PS_paramLEDET.writeFileLEDET(nameFileLEDET_PS)
    return a

def testOldLEDETnotebook():
    from steam_nb_api.ledet.NotebookLEDET import NB_LEDET as nl
    nameMagnet = "MainSolenoid"  # coil name in imput folder
    model_n = 0  # this is model number and gets added as _model_n in LEDET input file name
    n = nl(nameMagnet, model_n)  # create notebook object called n
    n.write_ledet_input()
    return n

def testSolenoids():
    new_notebook = Notebook_LEDET('MainSolenoid_New', typeMagnet = 'solenoid')

    nGroups = new_notebook.nGroups
    new_notebook.load_ConductorData(['W1'], [1] * int(new_notebook.nGroups))

    elPairs_GroupTogether = []
    for i in range(0,nGroups,2):
        elPairs_GroupTogether.append([nGroups-i, nGroups-i-1])
    elPairs_RevElOrder = [0, 1, 0]
    new_notebook.set_ElectricalOrder(elPairs_GroupTogether, elPairs_RevElOrder)

    max_distance = 0.5E-3
    new_notebook.set_ThermalConnections(max_distance)

    R_circuit = 7.76E-4
    R_crowbar = 5.6E-5
    Ud_crowbar = 0.34

    t_PC = 0
    tStart = -0.02
    Transient = 'FPA'

    nHalfTurnsDefined = new_notebook.nHalfTurns
    alphasDEG = nHalfTurnsDefined * [0]
    rotation_block = nHalfTurnsDefined * [0]
    mirror_block = nHalfTurnsDefined * [0]
    mirrorY_block = nHalfTurnsDefined * [0]

    fL_I = [0, 1000]
    fL_L = [1, 1]

    time_vector_params = [tStart, 5E-4, 0, 5E-4, 5E-4, 0.5, 0.501, 0.001, 1]
    tQuench = tStart
    initialQuenchTemp = 10

    # Further stuff
    new_notebook.load_Options('Default')
    new_notebook.set_SimulationType('2D')
    new_notebook.load_VariablesToStore('Default')
    new_notebook.load_PlotOptions('Default')
    new_notebook.storeVariables(locals())


    # Finish up
    nameMagnet = 'MainSolenoid_New'
    nameFileLEDET = nameMagnet + '_TEST_0' + '.xlsx'
    new_notebook.writeLEDETFile(nameFileLEDET, locals())

    # new_notebook.plot_all()

    return new_notebook

def testMP3():
    Opts = Options()
    Opts.t_0 = [0, 1.5, 2]
    Opts.t_end = [1.5, 2, 3]
    Opts.t_step_max = [[0.0005, 0.0005, 0.001]] + [[0.0005, 0.0005, 0.001]] * 2
    Opts.relTolerance = [1e-4] + [None] * 2
    Opts.absTolerance = [1] + [None] * 2
    Opts.executionOrder = [1] + [2] * 2
    Opts.executeCleanRun = [True] * (2 + 1)

    # ParameterFile = "600A_Circuit_Param_Table.csv"
    # MP3 = MP3_setup('RSS.A81B1', ParameterFile, Opts = Opts, enableQuench=0)
    # MP3.load_config('MarvinJ')
    # MP3.SetUpSimulation('FPA', 250)
    ParameterFile = "IPQ_Circuit_Param_Table.csv"
    MP3 = MP3_setup("RQ4.L2", ParameterFile)
    MP3.load_config('MarvinJ')
    MP3.SetUpSimulation('unbalancedFPA', [[250, 500]],
                        ManualCircuit="C:\\cernbox\\SWAN_projects\\steam-notebooks\\steam-sing-input\\IPQ\\IPQ_MagnetEQ4.cir")
    return MP3

# a = test_persCurrents2()

# nb = testOldLEDETnotebook()

# nb = testSolenoids()

# nb = testMP3()

# nb= testLEDETnotebook()

# CompareLEDETParameters("C:\cernbox\steam-notebook-api\steam_nb_api\ledet\MBRB_TEST_0.xlsx","C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MBRB\MBRB_0.xlsx")

# testConsistencyChecks()


CompareLEDETParameters("C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MQ_1AP\MQ_1AP_0.xlsx",
                       "S:\LHC\RQD_RQF\ElMaTh\LEDET\LEDET\MQ\Input\MQ_1.xlsx")
# CompareLEDETParameters("C:\cernbox\MB_1.xlsx","C:\cernbox\MB_65.xlsx")
# CompareLEDETParameters("C:\cernbox\MQXA_200.xlsx","C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MQXA\MQXA_200.xlsx")

# CompareLEDETParameters("C:\cernbox\COSIM\Models\COSIM_model_RQ9.L1_unbalancedFPA_5225A5225A\LEDET_2\LEDET\MQMC_2in1\Input\MQMC_2in1_0.xlsx",
#                        "S:\LHC\IPQ\ElMaTh\PSPICE_LEDET\Output\Test_31\\3_LEDET\Model\LEDET\MQMC_2in1\Input\MQMC_2in1_0.xlsx")
# CompareLEDETParameters("C:\cernbox\LEDET_MT\LEDET\MQXFS4b\Input\MQXFS4b_0.xlsx", "C:\cernbox\MasterThesis\QuenchPlans\MQXF_V2_2924.xlsx")
# CompareLEDETParameters("C:\\cernbox\\steam-notebook-api\\test\\ledet\\resources\\TestFile_1.xlsx", "C:\\cernbox\\steam-notebook-api\\test\\ledet\\TestFile1.xlsx")
# CompareLEDETParameters("C:\cernbox\MasterThesis\QuenchPlans\MQXF_V2_5400.xlsx", "C:\cernbox\LEDET_MT\LEDET\MQXFS4b\Input\MQXFS4b_14.xlsx")
# CompareLEDETParameters("C:\cernbox\LEDET_MT\LEDET\MQXFS4b\Input\MQXFS4b_18.xlsx", "C:\cernbox\LEDET_MT\LEDET\MQXFS4b\Input\MQXFS4b_15.xlsx")
# CompareLEDETParameters("C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MCBXV\MCBXV_CopperWedges_ThCool_0.xlsx", "C:\cernbox\TEMP2\MCBXH_CopperWedges_ThCool_100.xlsx")
# CompareLEDETParameters("C:\cernbox\COSIM\\600A\RCS.A45B2\Output_3\\3_LEDET\Model\LEDET\MCS\Input\MCS_0_.xlsx","C:\cernbox\SWAN_projects\steam-notebooks\steam-sing-input\\600A_Rpar\cosim_model_RCS.A45B2\LEDET_2\LEDET\MCS\Input\MCS_0.xlsx")
# CompareLEDETParameters("C:\cernbox\LEDET_MT\LEDET\MQXFS4b\Input\MQXFS4b_23.xlsx", "C:\cernbox\MQXF_V2_2924.xlsx")

# CompareLEDETParameters("C:\cernbox\MB_92.xlsx", "C:\cernbox\MB_98.xlsx")

# CompleteRun()

# PrepareSimulations()

# a  = testvQ()

# td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFPB01\\HCLMQXFBT01-CR000001__A202007140955_a001(0).tdms"

# td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFS4b\\HCMQXSM001-CR000042__H1810151854_a026(0).tdms"
# td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFS4b\\HCMQXSM001-CR000042__H1810111418_a003(0).tdms"
# td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFS4b\\HCMQXSM001-CR000042__H1810111846_a008(0).tdms"
# td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFS4b\\HCMQXSM001-CR000042__H1810101854_tb017(0).tdms"
# td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFS4b\\HCMQXSM001-CR000042__H1810101725_tb016(0).tdms"
# td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFS4b\\HCMQXSM001-CR000042__H1810171217_a041(0).tdms"
# td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFS4b\\HCMQXSM001-CR000042__H1810121049_a012(0).tdms"
# td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFS4b\\HCMQXSM001-CR000042__H1810120908_a009(0).tdms"
# td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFS4b\\HCMQXSM001-CR000042__H1810111541_a006(0).tdms"
# td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFS4b\\HCMQXSM001-CR000042__H1810171446_a042(0).tdms"
# td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFS4b\\HCMQXSM001-CR000042__H1810171007_a036(0).tdms"
# td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFS4b\\HCMQXSM001-CR000042__H1810171144_a039(0).tdms"
# td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFS4b\\HCMQXSM001-CR000042__H1810161600_a033(0).tdms"

# sim_data = "C:\\cernbox\\LEDET_MT\\LEDET\\MQXFBP2\\Output\\Mat Files\\SimulationResults_LEDET_10.mat"
# sim_data = "C:\\cernbox\\LEDET_MT\\LEDET\\MQXFS4b\\Output\\Mat Files\\SimulationResults_LEDET_12.mat"
# sim_data = "C:\\cernbox\\LEDET_MT\\LEDET\\MQXFS4b\\Output\\Mat Files\\SimulationResults_LEDET_10.mat"
# sim_data = "C:\\cernbox\\LEDET_MT\\LEDET\\MQXFS4b\\Output\\Mat Files\\SimulationResults_LEDET_27.mat"
# sim_data = "C:\\cernbox\\LEDET_MT\\LEDET\\MQXFS4b\\Output\\Mat Files\\SimulationResults_LEDET_15.mat"
# sim_data = "C:\\cernbox\\LEDET_MT\\LEDET\\MQXFS4b\\Output\\Mat Files\\SimulationResults_LEDET_23.mat"
# sim_data = "C:\\cernbox\\LEDET_MT\\LEDET\\MQXFS4b\\Output\\Mat Files\\SimulationResults_LEDET_18.mat"
# sim_data = "C:\\cernbox\\LEDET_MT\\LEDET\\MQXFS4b\\Output\\Mat Files\\SimulationResults_LEDET_3.mat"
# sim_data = "C:\\cernbox\\LEDET_MT\\LEDET\\MQXFS4b\\Output\\Mat Files\\SimulationResults_LEDET_12.mat"
# sim_data = "C:\\cernbox\\LEDET_MT\\LEDET\\MQXFS4b\\Output\\Mat Files\\SimulationResults_LEDET_26.mat"

# a = testQuenchPlanAnalysis(td_data, sim_data)
# a.ExtractFeatures()
# a = testQuenchPlanAnalysis(0, sim_data)
# a = testQuenchPlanAnalysis(td_data, 0)


# a = ParametersLEDET()
# a.readLEDETExcel(testfile7)
# Sw = MinMaxSweep(a, 3)
# MagnetName = 'MCBXH_CopperWedges'
# Sw.addParameterToSweep('l_magnet', 4.16, 5.2)
# Sw.addParameterToSweep('f_ro_eff_inGroup', 1, 3)
# Sw.addParameterToSweep('RRR_Cu_inGroup', 100, 300)
# Sw.addQuenchSweep("tStartQuench",[0,2],[-3,5])
# Sw.addQuenchSweep("tStartQuench",[[1,4],[2,5]],[[-3,5],[1,2]])
# Sw.addHeliumCrossSection(3, 6, basePoints=4)
# Sw.generatePermutations()
# Sw.prepareSimulation(MagnetName, "C:\\cernbox\\TEST-DELTE\\")

# x = AutomaticRun()

# a = ParametersLEDET()
# a.readLEDETExcel(testfile13)
# a.writeFileLEDET('Test_todelete.xlsx')