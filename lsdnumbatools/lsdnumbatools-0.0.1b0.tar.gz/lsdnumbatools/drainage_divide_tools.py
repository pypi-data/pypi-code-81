import numba as nb
import numpy as np
import lsdnumbatools as lsdnb



@nb.jit(nopython = True, cache = True)
def extract_drainage_divide_nodes(basin_labels, nx, ny, drainage_divide_ID, drainage_divide_nodes):

  # preparating a D4 lookup
  loop_col = [0,-1,1,0]
  loop_row = [-1,0,0,1]
  # drainage_divide_ID = np.full_like(basin_labels, -1, dtype = np.int16)
  # drainage_divide_nodes = np.full_like(basin_labels, -1, dtype = np.int16)
  size_DD = 0

  # Iterating through nodes
  for r in range(1, ny - 1):
    for c in range(1, nx - 1):
      # Getting the node ID and initialising the slope
      inode = r * nx + c
      if(basin_labels[inode] < 0):
        continue
      # Iterating through neighbors
      for k in range(4):
        ineight = (r+loop_row[k])*nx + (c + loop_col[k])
        if(basin_labels[inode] != basin_labels[ineight]):
          drainage_divide_ID[inode] = basin_labels[inode]
          drainage_divide_nodes[size_DD] = inode
          size_DD += 1

@nb.jit(nopython = True, cache = True)
def build_separated_undirected_graphs_D4_from_drainage_divide_nodes(drainage_divide_ID, drainage_divide_nodes, nrows, ncols, D4dcons, D4ncons, basin_labels):
  """
    Builds a D4 undirected graph for drainage divide nodes by 1: link all the DD nodes belonging to a same watershed ID to their D4 neighbors, and then
    breaking the unwanted connections
  """

  # pregenerating node, row, cols
  nodes = np.arange(nrows*ncols, dtype = np.int16)
  rows, cols = lsdnb.rectangle_compartimentor( nrows, ncols, nodes)
  loop_row = [-1,0,0,1]
  loop_col = [0,-1,1,0]

  # first iterating through the DD ndoes and checking the neighbors in a D4 (king) algorithm
  # if a neighboring node is of the same DD ID -> create edge
  for i in range(drainage_divide_nodes.shape[0]):
    # get node, DDID, row col, ...
    inode = drainage_divide_nodes[i]
    tid = drainage_divide_ID[inode]
    r = rows[inode]
    c = cols[inode]
    # Iterate through neighbors
    for j in range(4):
      nr = r + loop_row[j]
      nc = c + loop_col[j]
      # Checking neighbor is real
      if(nr<0 or nr>= nrows or nc < 0 or nc >= ncols):
        continue
      # getting node ID
      nnode = r * ncols + c
      #If same ID: create edge
      if(drainage_divide_ID[nnode] == tid):
        D4dcons[inode,D4ncons[inode]] = nnode
        D4ncons[inode] += 1


  # now "cleaning it": any node should only have 2 connections, if one has more than 2, his "anomalic neightbor" will also have more than 2
  #However if they have more than 2 conflicting connection, it becomes ambiguous and I need to gather these nodes for further conflict solving algorithm
  conflict_nodes = []
  for i in range(drainage_divide_nodes.shape[0]):
    inode = drainage_divide_nodes[i]
    if(D4ncons[inode] < 3):
      continue

    # Identifying conflict nodes
    to_keep = []
    to_correct = []
    for j in range(D4ncons[inode]):
      nnode = D4dcons[inode,j]
      if(D4ncons[nnode]<3):
        to_keep.append(nnode)
      else:
        to_correct.append(nnode)

    # If there is only one conflict edge, is easy:
    # I remove the edge from both vertices
    if(len(to_correct) == 1):

      D4ncons[inode] = len(to_keep)
      for j in range(4):
        if( j < D4ncons[inode]):
          D4dcons[inode,j] = to_keep[j]
        else:
          D4dcons[inode,j] = -1

      for nnode in to_correct:
        to_keep = []
        for j in range(D4ncons[nnode]):
          if(D4dcons[nnode,j] != inode):
            to_keep.append(D4dcons[nnode,j])

      D4ncons[nnode] = len(to_keep)
      for j in range(4):
        if( j < D4ncons[nnode]):
          D4dcons[nnode,j] = to_keep[j]
        else:
          D4dcons[nnode,j] = -1
    
    else:
      # gathering super_conflicts
      conflict_nodes.append(inode)

  # Dealing with super conflicts yaay
  superconflicts = np.full_like(drainage_divide_ID, -1, dtype = np.int16)
  #Labelling them
  for inode in conflict_nodes:
    superconflicts[inode] = 1
  for inode in conflict_nodes:
    # checking neighbors
    tid = drainage_divide_ID[inode]
    r = rows[inode]
    c = cols[inode]

    axe_NS = True
    # Iterate through neighbors
    for j in range(4):
      nr = r + loop_row[j]
      nc = c + loop_col[j]
      # Checking neighbor is real
      if(nr<0 or nr>= nrows or nc < 0 or nc >= ncols):
        if(j == 0 or j == 3):
          axe_NS = False
        else:
          axe_NS = True
        continue
      # getting node ID
      nnode = r * ncols + c
      if(drainage_divide_ID[nnode] < 0):
        if(basin_labels[nnode] == tid):
          if(j == 0 or j == 3):
            axe_NS = False
          else:
            axe_NS = True
        else:
          if(basin_labels[nnode] == tid):
            if(j == 0 or j == 3):
              axe_NS = True
            else:
              axe_NS = False

    # Now I determined the axe of deletion
    if(axe_NS):
      loop_row_deletion = [-1,1]
      loop_col_deletion = [0,0]
    else:
      loop_row_deletion = [0,0]
      loop_col_deletion = [-1,1]

    for j in range(2):
      nr = r + loop_row[j]
      nc = c + loop_col[j]
      # Checking neighbor is real
      if(nr<0 or nr>= nrows or nc < 0 or nc >= ncols):
        continue;
      nnode = r * ncols + c
      if(superconflicts[nnode] == 1):
        to_keep = []
        for k in range(D4ncons[inode]):
          if(D4dcons[inode,k] != nnode):
            to_keep.append(nnode)
        D4ncons[inode] = len(to_keep)
        for k in range(4):
          if(k < D4ncons[inode]):
            D4dcons[inode,k] = to_keep[k]
          else:
            D4dcons[inode,k] = -1

  # # super conflict connection
  # NconnectionwithSC = np.zeros_like(drainage_divide_ID, dtype = np.int16)
  # isdone = {-1:False}
  # for inode in conflict_nodes:
  #   isdone[inode] = False
  #   for j in range(D4ncons[inode]):
  #     if(superconflicts[D4dcons[inode,j]] ==1):
  #       NconnectionwithSC[inode] += 1


  # n_conflict_to_fix = len(conflict_nodes)
  # while(n_conflict_to_fix>0):
  #   nodes_to_decrement = []
  #   for inode in conflict_nodes:
  #     if(isdone[inode]):
  #       continue

  #     if(NconnectionwithSC[inode] <= 2):
  #       found_node = False
  #       node_to_disconnect = []

  #       for j in range(D4ncons[inode]):
  #         if(NconnectionwithSC[D4dcons[inode,j]] <= 2 and superconflicts[D4dcons[inode,j]] == 1):    
  #           node_to_disconnect.append(D4dcons[inode,j])

  #       if(len(node_to_disconnect) == 1):
  #         #yeah, it kindle joy

  #         # THINGS TO TAKE CARE OF:
  #         ## REMOVING NODE WITH ONLY ONE PIXEL
  #         ## DEALING WITH SUPER CONFLICTS
        


@nb.jit(nopython = True, cache = True)
def orient_undirected_D4_drainage_divide_graph_per_basin_ID(basin_labels,D4dcons,D4ncons,ordered_DD_nodes, ordered_DD_basID, outlets):

  visited = np.zeros_like(basin_labels, dtype = np.bool)
  incrementor = 0
  for out in outlets:
    this_basID = basin_labels[out]
    ordered_DD_nodes[incrementor] = out
    ordered_DD_basID = this_basID



@nb.jit(nopython = True, cache = True)
def propagate_upstream_labels_from_all_BL(labels,stack,D8dons,D8ndons):
  for inode in stack:
    for j in range(D8ndons[inode]):
      labels[D8dons[inode,j]] = labels[inode]

# @nb.jit(nopython = True, cache = True)
# def thin_by_unique_label_and_distance(arr, )













