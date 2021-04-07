#%% Load modules...
import clr, sys, os

foldername = os.path.join(os.path.dirname(os.path.abspath(__file__)),'Resources')
sys.path.append(foldername)
simba_dll_filepath = os.path.join(foldername,'Simba.Data.dll')
clr.AddReference(simba_dll_filepath)

from Simba.Data.Repository import ProjectRepository
from Simba.Data import License, Design, Circuit, DesignExamples
import Simba.Data
Simba.Data.FunctionsAssemblyResolver.RedirectAssembly()
Simba.Data.DoubleArrayPythonEncoder.Register()
Simba.Data.Double2DArrayPythonEncoder.Register()
Simba.Data.StatusPythonEncoder.Register()
Simba.Data.ParameterToPythonEncoder.Register()

Simba.Data.PythonToParameterDecoder.Register()
Simba.Data.PythonToStatusDecoder.Register()


if os.environ.get('SIMBA_DEPLOYMENT_KEY') is not None:
    License.Activate(os.environ.get('SIMBA_DEPLOYMENT_KEY'))