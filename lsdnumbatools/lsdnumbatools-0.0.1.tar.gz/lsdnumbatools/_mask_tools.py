"""
This set of functions are designed to define masks on topographic data
For example select a watershed based on different conditions
"""

import numba as nb
import numpy as np
import math


@nb.jit(nopython = True)
def mask_upstream_from_node_ID_SF(node, stack, receivers, acc,argSstack,imask):
  """
    Label all nodes draining into a single one, Steepest descent version
  """
  omask = np.zeros_like(stack, dtype = np.int8)
  st = argSstack[node]
  print("WILL ADD::")
  print(acc[node])
  for i in range(acc[node]):
    if(imask[stack[st+i]] == 1):
      omask[stack[st+i]] = 1
  return omask


@nb.jit(nopython = True)
def recursive_add_to_mask_upstream_from_node_ID_MF(i,omask,ndondone,MFnDonors,MFDonors,isinqueue):
  # print(i, end = '|')
  for j in range(MFnDonors[i]):
    nodej = MFDonors[i,j]
    if(omask[nodej] == 1 and ndondone[nodej] == MFnDonors[nodej]):
      continue

    if(ndondone[nodej] > MFnDonors[nodej]):
      print("Arg!!!")

    if(omask[nodej] == 0):
      omask[nodej] = 1
      ndondone[i] += 1

    if(ndondone[nodej] != MFnDonors[nodej] and isinqueue[nodej] == 0):
      isinqueue[nodej] = 1
      recursive_add_to_mask_upstream_from_node_ID_MF(nodej,omask,ndondone,MFnDonors,MFDonors,isinqueue)


@nb.jit(nopython = True)
def mask_upstream_from_node_ID_MF(node, Sstack, Sreceivers, MFreceivers, MFDonors, MFnDonors, MFnrecs, accSF,argSstack,imask):
  """
    Label all nodes draining into a single one, multiple flow version
  """
  # First getting the mask for SF donors
  omask = mask_upstream_from_node_ID_SF(node, Sstack, Sreceivers, accSF,argSstack,imask)
  ndondone = np.zeros_like(Sstack)
  isinqueue = np.zeros_like(Sstack, dtype = nb.int8)
  for i in range(omask.shape[0]):
    if(omask[i] == 0):
      continue;
    for j in range(MFnrecs[i]):
      nodej = MFreceivers[i,j]
      ndondone[nodej] += 1

  for i in range(omask.shape[0]):
    # print("2:%s/%s       "%(i+1,omask.shape[0] ), end = '\r')
    if(omask[i] == 0):
      continue
    if(ndondone[i] == MFnDonors[i]):
      continue
    for j in range(MFnDonors[i]):
      nodej = MFDonors[i,j]
      # print(nodej, end = '|')
      if(omask[nodej] == 1 and ndondone[nodej] == MFnDonors[nodej]):
        continue
      if(omask[nodej] == 0):
        omask[nodej] = 1
        ndondone[i] += 1
    if(ndondone[nodej] != MFnDonors[nodej]):
      isinqueue[nodej] = 1        
      recursive_add_to_mask_upstream_from_node_ID_MF(nodej,omask,ndondone,MFnDonors,MFDonors, isinqueue)

  # Correcting to the global mask
  omask[imask == 0] = 0

  return omask










































# End of fucking file FFS I DONT WANT TO ONLY WORK ON THE ABSOLUTE BOTTOM OF MY SCREEN