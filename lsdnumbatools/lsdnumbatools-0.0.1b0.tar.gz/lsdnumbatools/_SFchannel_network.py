import numba as nb
import numpy as np



@nb.njit()
def restack_from_source_ID_S8S(SStack, SStackID, D8Srec, D8Sndons, D8Sdons, D8Sdist2rec, D8Sdist2don, sources):
  """
    Restacking operation generating a river stack from the main dem stack with the corresponding array conversions
    Basically creating a local referential for the river. It allows its decoupling from the main dem while retaining global informations if necessary
    At some point I will create another inverse function to readapt a river stack to a different DEM
    Might be WIP
    B.G
  """
  # Initialising all the arrays
  ## River node to dem node conversion
  riverID2nodeID = np.full_like(SStack, -1)
  ## DEM node ID to river node ID
  nodeID2riverID = np.full_like(SStack, -1)
  ## river ID to its rec ID (river ref)
  river_rec = np.full_like(SStack, -1)
  ## river_ID to its donors (in river)
  river_dons = np.full_like(D8Sndons, -1)
  ## river_id/ndonors to distance to donors
  river_dist2dons = np.full_like(D8Sndons, -1)
  ## river ID to distance to receivers
  river_dist2rec = np.full_like(SStack, -1)
  ## river stack sensu Braun and Willett
  river_stack = np.full_like(SStack, -1)
  ## Temp ID of dem stack to sort the stack at the end
  river_stack_ID = np.full_like(SStack, -1)

  # explicit enough by its name I believe
  n_river_nodes = 0

  # bool mask on the main dem to wether a node is river or not
  mask_mother_river = np.full_like(SStack, -1, dtype = np.bool)

  # Id in the stack inserter
  stack_insert = 0
  # iterating through the list of sources node ID
  for source in sources:
    # starting with the source
    tnode = source
    #which receiver is
    recnode = D8Srec[tnode]
    # I am gathering nodes in me river while the receiver is not in the river
    # note: It will stop at base level first, because a base level is its own receiver
    while(mask_mother_river[recnode] == False):
      ## Inserting the current node
      river_stack[stack_insert] = stack_insert
      ## Getting the stack ID
      river_stack_ID[stack_insert] = SStackID[tnode]
      ## conversion between node ID to the stack ID
      nodeID2riverID[tnode] = stack_insert
      ## river ID to its dem node ID
      riverID2nodeID[stack_insert] = tnode
      ## this node is a river now
      mask_mother_river[tnode] = True
      ## Incrementing 
      stack_insert += 1
      n_river_nodes += 1
      ## NExt nodes
      tnode = recnode
      recnode = D8Srec[tnode]
      # End of the while

  # Now I have me stack, I can resize it and compute the other metrics
  riverID2nodeID = riverID2nodeID[:n_river_nodes]
  river_rec = river_rec[:n_river_nodes]
  river_dons = river_dons[:n_river_nodes]
  river_dist2rec = river_dist2rec[:n_river_nodes]
  river_dist2dons = river_dist2rec[:n_river_nodes]
  river_stack = river_stack[:n_river_nodes]
  river_stack_ID = river_stack_ID[:n_river_nodes]

  # reIDfication, I am sorting the stack to get true topological order
  reidstack = np.argsort(river_stack_ID)
  river_stack = river_stack[reidstack]

  # iterating through the river nodes to build the local graph
  for inode in range(n_river_nodes):
    # Getting the dem node
    dem_node = riverID2nodeID[inode]
    # and the receiver dem node
    recdem = D8Srec[dem_node]
    # if the receiver is in the river network, I add it to the graph
    if(nodeID2riverID[recdem] >= 0):
      river_rec[inode] = nodeID2riverID[recdem]
      river_dist2rec = D8Sdist2rec[recdem]

    # Same here with the donors, there are jsut multiple ones
    dondem = D8Sdons[dem_node]
    for j in range(D8Sndons[dem_node]):
      ## If not a river, ignore
      if(nodeID2riverID[D8Sndons[dem_node,j]] < 0):
        continue
      ## else compute
      river_dons[inode,j] = nodeID2riverID[D8Sndons[dem_node,j]]
      river_dist2dons[inode,j] = D8Sdist2don[dem_node,j]

    # end of nested for
  # end of the main for

  return nodeID2riverID, riverID2nodeID, river_rec, river_dons, river_dist2rec, river_dist2dons, river_stack, mask_mother_dem




@nb.njit()
def compute_distance_from_outlets(river_stack, river_rec, river_dist2rec, dtype = np.float32):
  """
  Computes the flow distance form outlets to sources
  B.G.
  """
  output = np.zeros_like(river_stack, dtype = dtype)
  for inode in river_stack:
    if(inode == river_rec[inode]):
      continue
    output[inode] = output[river_rec[inode]] + river_dist2rec[inode]
  return output

@nb.njit()
def compute_max_distance_from_sources(river_stack, river_rec, river_dist2rec, dtype = np.float32):
  """
  Computes the flow distance form outlets to sources
  B.G.
  """
  output = np.zeros_like(river_stack, dtype = dtype)
  tid = 0
  for inode in river_stack[::-1]:
    if(inode == river_rec[inode]):
      continue
    next_thingy = output[inode] + river_dist2rec[inode]
    if(next_thingy > output[river_rec[inode]]):
      output[river_rec[inode]] = next_thingy
  return output


@nb.njit()
def compute_river_ID_by_length(sources, distance_from_outlets, river_rec):

  output = np.full_like(river_rec,-1,dtype = np.int32)
  sources_dfo = distance_from_outlets[sources]
  idsorted = np.argsort(sources_dfo)[::-1]

  cID = -1
  for tid in idsorted:
    cID += 1
    snode = sources[tid]
    recnode = river_rec[snode]
    do = True
    while(do):
      output[snode] = CID
      if(recnode == snode or output[recnode] >= 0):
        do = False
      else:
        snode = recnode
        recnode = river_rec[snode]
    # end while
  #end for
  return output










































#end of file


