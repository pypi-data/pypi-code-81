
import sys
import time

try: # Check for local build
    import MDI_Library as mdi
except: # Check for installed package
    import mdi

try:
    import numpy as np
    use_numpy = True
except ImportError:
    use_numpy = False

# Check for a -nompi argument
# This argument prevents the code from importing MPI
nompi_flag = False
for arg in sys.argv:
    if arg == "-nompi":
        nompi_flag = True

use_mpi4py = False
if not nompi_flag:
    try:
        from mpi4py import MPI
        use_mpi4py = True
    except ImportError:
        pass

# get the MPI communicator
if use_mpi4py:
    mpi_world = MPI.COMM_WORLD
else:
    mpi_world = None

# Initialize the MDI Library
mdi.MDI_Init(sys.argv[2],mpi_world)
if use_mpi4py:
    mpi_world = mdi.MDI_MPI_get_world_comm()
    world_rank = mpi_world.Get_rank()
else:
    world_rank = 0

# Confirm that this code is being used as a driver
role = mdi.MDI_Get_Role()
if not role == mdi.MDI_DRIVER:
    raise Exception("Must run driver_py.py as a DRIVER")

# Connect to the engine
comm = mdi.MDI_Accept_Communicator()



# Few lines to test density, requests densities. 
# Driver