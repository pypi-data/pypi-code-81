import numba as nb
import numpy as np
import math as m
import lsdnumbatools as lsdnb

@nb.jit(nopython = True, cache = True)
def compute_DA_Srec(DA,Srec,Sstack,dx,dy):
  """
  Compute the drainage area using the single flow stack
  """
  # Initialising to 0
  # DA = np.zeros_like(Sstack,dtype = nb.float32)
  # itarating through the reverse stack
  for i in range(Srec.shape[0]):
    # reversing the thingy
    ri = Srec.shape[0] - 1 - i
    # node index
    inode = Sstack[ri]
    # Adding current DA
    DA[inode] += dx*dy
    # Getting receiver
    irec = Srec[inode]
    # Stopping if base level
    if(irec == inode):
      continue
    # Propagating DA
    DA[irec] += DA[inode]

@nb.jit(nopython = True, cache = True)
def compute_dist_from_outlet(donors, ndonors, Sstack, dist2outlet, dist2rec, Srec, dx,dy):
  for inode in Sstack:
    if(inode == Srec[inode]):
      dist2outlet[inode] = 0
      continue

    for d in range(ndonors[inode]):
      idon = donors[inode,d]
      dist = dist2rec[idon]
      dist2outlet[idon] = dist2outlet[inode] + dist






@nb.jit(nopython = True, cache = True)
def compute_chi_Srec(chi, QDA, Sstack, Srec, Slength2rec, A0, theta):
  """
  Calculating Chi for a whole stack/rec. This can be the original stack/rec or a subset of it (make sure you convert the ID)
  """
  # Initialising chi to 0 everywhere
  # chi = np.zeros_like(Sstack, dtype = nb.float32)

  # Integrating from base-level to top
  for inode in Sstack:
    irec = Srec[inode]
    if(inode == irec):
      continue
    # Trapezoidal approxiamation of the integration
    chi[inode] = chi[irec] + (m.pow(A0/QDA[irec],theta) + m.pow(A0/QDA[inode],theta) ) / 2 * Slength2rec[inode]

@nb.jit(nopython = True, cache = True)
def compute_SPL_chi_Srec(chi, QDA, UE, K, Sstack, Srec, Slength2rec, A0, UE0, K0, mexp,nexp):
  """
  Calculating Chi for a whole stack/rec. This can be the original stack/rec or a subset of it (make sure you convert the ID)
  """
  # Initialising chi to 0 everywhere
  # chi = np.zeros_like(Sstack, dtype = nb.float32)

  # Integrating from base-level to top
  for inode in Sstack:
    irec = Srec[inode]
    if(inode == irec):
      continue
    # Trapezoidal approxiamation of the integration
    chi[inode] = chi[irec] + (m.pow(A0 * UE[irec]/(QDA[irec]**mexp  * K[irec]),1/nexp) + m.pow(A0 * UE[inode]/(QDA[inode]**mexp * K[inode]),1/nexp) ) / 2 * Slength2rec[inode]

@nb.jit(nopython = True, cache = True)
def compute_curvachi_basic(chi,elevation,Srec,curv):

  intermediate = np.zeros_like(curv)
  for inode in range(Srec.shape[0]):
    irec = Srec[inode]
    if(inode ==irec ):
      continue
    intermediate[inode] = (elevation[inode] - elevation[irec])/(chi[inode] - chi[irec])

  for inode in range(Srec.shape[0]):
    irec = Srec[inode]
    if(inode ==irec ):
      continue
    curv[inode] = (intermediate[inode] - intermediate[irec])/(chi[inode] - chi[irec])

    
        
@nb.jit(nopython = True, cache = True)
def compute_curvachi_central(chi,elevation,Srec,Sdons, Sndons,curv, slope_smooth_deg):

    intermediate = np.zeros_like(curv)
    for inode in range(Srec.shape[0]):
        irec = Srec[inode]
        if(inode ==irec ):
            continue
        intermediate[inode] = (elevation[inode] - elevation[irec])/(chi[inode] - chi[irec])
    
    for dkjfhl in range(slope_smooth_deg):
        intermediate2 = average_amongst_donors_and_recs(intermediate, Srec, Sdons, Sndons)
    
    for inode in range(Srec.shape[0]):
        irec = Srec[inode]
        if(inode ==irec ):
            continue
        curv[inode] = (intermediate2[inode] - intermediate2[irec])/(chi[inode] - chi[irec])


























    # end of file (sublime text automatically removes the unused line and stick the code in the bottom of the screen. that triggers my OCD)