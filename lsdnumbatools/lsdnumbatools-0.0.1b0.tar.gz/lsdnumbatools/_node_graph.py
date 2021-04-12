import numba as nb
import numpy as np
from ._union_find import UnionFind
from ._looper import iterasator

@nb.jit(nopython = True, cache = False)
def compute_Srec_D8(elevation, D8Srec, D8Sdist, iterator_tool):
  """
  Compute the single flow recevers and the donors in a D8 manners
  """
  # Iterating through all nodes
  for inode in range(iterator_tool.nxy):
    # print(inode)
    D8Srec[inode] = inode
    D8Sdist[inode] = 0.
    slope_max = 0.

    # Iterating through neighbors
    k = -1
    neight = iterator_tool.get_neighbouring_nodes(inode)
    for ineighbour in neight:
      k+=1
      if(ineighbour == iterator_tool.nodata):
        continue

      # local slope (if donors, slope<0)
      slope = (elevation[inode] - elevation[ineighbour]) / iterator_tool.lengthener[k]

      # If higher slope -> receiver
      if slope > slope_max:
        slope_max = slope
        D8Srec[inode] = ineighbour
        D8Sdist[inode] = iterator_tool.lengthener[k]


@nb.jit(nopython = True, cache = False)
def compute_Srec_donors_D8(D8Sdons, D8Sndons, D8Srec, D8Sdondist, D8Sdist):
  """
  Compute the single donors and number of donors arrays from the D8 single receivers info
  """
  # Initialising the array of donors and ndonors
  # D8Sdons = -1 * np.ones((D8Srec.shape[0],8), dtype = np.int)
  # D8Sndons = np.zeros_like(D8Srec,dtype = np.int)

  # Iterating through all nodes
  for node in range(D8Srec.shape[0]):
    # receveir ID
    irec = D8Srec[node]
    # if base-level: ignore
    if(node == irec):
      continue
    # if not, add the donor to the list and increment the number of donors
    D8Sdons[irec,D8Sndons[irec]] = node
    D8Sdondist[irec,D8Sndons[irec]] = D8Sdist[node]
    D8Sndons[irec] += 1


@nb.jit(nopython = True, cache = False)
def compute_Mrec_D8(elevation, D8Mrec, D8Mdist, D8Snrecs, D8Mdons, D8Mndons, D8Mdondist, iterator_tool):
  """
  Compute the Multiple flow receivers and the donors in a D8 manners
  """
  # Iterating through all nodes
  for inode in np.arange(iterator_tool.nxy, dtype = np.intp):
      # Iterating through neighbors
      k = np.intp(-1)
      j = np.intp(0)
      l = np.intp(0)
      neight = iterator_tool.get_neighbouring_nodes(inode)
      for ineighbour in neight:
        k+=1
        if(ineighbour == iterator_tool.nodata):
          continue

        # local slope (if donors, slope<0)
        if(elevation[inode] > elevation[ineighbour]):
          D8Mrec[inode,j] = ineighbour
          D8Mdist[inode] = nb.float32(iterator_tool.lengthener[k])
          D8Snrecs[inode] += 1
          j+=1
        elif(elevation[inode] < elevation[ineighbour]):
          D8Mdons[inode,l] = ineighbour
          D8Mdondist[inode] = nb.float32(iterator_tool.lengthener[k])
          D8Mndons[inode] += 1
          l+=1


@nb.jit(nopython = True, cache = False)
def _add2stack(inode, ndonors, donors, Sstack, istack):
  """
  Recursive function to add the nodes to the stack (see Braun and Willett 2013)
  """
  for k in range(ndonors[inode]):
    idonor = donors[inode, k]
    Sstack[istack] = idonor
    istack += 1
    istack = _add2stack(idonor, ndonors, donors, Sstack, istack)

  return istack


@nb.jit(nopython = True, cache = False)
def compute_Sstack(Sstack, ndonors, donors, receivers, nnodes):
  """
  Single-receiver stack computation following a modified version of Braun and Willett 2013
  """
  istack = 0

  for inode in range(nnodes):
    if receivers[inode] == inode:
      Sstack[istack] = inode
      istack += 1
      istack = _add2stack(inode, ndonors, donors,
                          Sstack, istack)

@nb.jit(nopython = True, cache = False)
def compute_Sstack_norecursions(Sstack, ndonors, donors, receivers, nnodes):
  """
  Single-receiver stack computation following a modified version of Braun and Willett 2013
  """
  istack = 0
  Q = np.empty(Sstack.shape,dtype=np.int32)
  insert_id = 0
  reading_id = -1

  for inode in range(nnodes):
    if receivers[inode] == inode:
      Sstack[istack] = inode
      istack += 1
      for k in range(ndonors[inode]):
        Q[insert_id] = donors[inode, k]
        insert_id += 1

      while(reading_id < insert_id):
        inode = Q[reading_id]
        reading_id += 1
        Sstack[istack] = inode
        istack += 1
        for k in range(ndonors[inode]):
          Q[insert_id] = donors[inode, k]
          insert_id += 1

      # istack = _add2stack(inode, ndonors, donors,
      #                     Sstack, istack)
      # for k in range(ndonors[inode]):
      #   idonor = donors[inode, k]
      #   Sstack[istack] = idonor
      #   istack += 1
      #   istack = _add2stack(idonor, ndonors, donors, Sstack, istack)

      # return istack


@nb.jit(nopython = True, cache = False)
def compute_argstack(stack,argstack):
  """
  Compute the argument-stack: ID = node ID and value = place in stack.
  The algorithm simply invert the stack
  """
  for i in range(stack.shape[0]):
    argstack[stack[i]] = i




@nb.jit(nopython = True, cache = False)
def define_subSstack_QDA_min_threshold(Sstack, Srec, donors, ndonors, QDA, threshold):
  """
  Take a stack and return a subset with its own stack, rec, donors and convertor to parent stack
  """
  # initialising the incrementor
  size_new_stack = 0 

  # initialising the arrays
  new_Sstack = np.zeros_like(Sstack, dtype = nb.intc)
  Id_to_new = np.full_like(Sstack,-1, dtype = nb.intc)

  for inode in Sstack:
    if(QDA[inode]>threshold):
      new_Sstack[size_new_stack] = inode
      Id_to_new[inode] = size_new_stack
      size_new_stack += 1

  return new_Sstack, Id_to_new

# @nb.jit(nopython = True, cache = False)
# def define_subSstack_from_node_ID(Sstack, Id2stack ndonors, node_id):
#   """
#   Take a stack and return a subset with its own stack, rec, donors and convertor to parent stack
#   """
#   # initialising the incrementor
#   size_new_stack = 0 

#   # initialising the arrays
#   new_Sstack = Sstack[Id2stack[node_id]]

  

#   return new_Sstack



###########
# The following set of funcions are adapted from xarray topo and are rerouting water from pits

@nb.jit(nopython = True, cache = False)
def compute_basins_Srec(Sbasins, outlets, Sstack, Srec, nnodes):
  """
  Computes the basin labels for Single receiver flow routines 
  """
  # Initiating the basin index to -1
  ibasin = -1

  # Iterating through the stack
  for inode in range(nnodes):
    istack = Sstack[inode]
    irec = Srec[istack]

    # if my receiver is meself -> outlet
    if irec == istack:
      # Then I increment the bsin index
      ibasin += 1
      # the outlet is saved 
      outlets[ibasin] = istack


    # and label the current node
    Sbasins[istack] = ibasin

  # correcting basin id to number of basins
  nbasins = ibasin + 1

  return nbasins


@nb.jit(nopython = True, cache = False)
def compute_pits(pits, outlets, nbasins, iterator_tool):
  """
  Comput the pits which need to be corrected based on an active node array (ie 1 where the node is internal, 0 when outletting outside of the model)
  """
  # Pit increment
  ipit = 0

  # Iterating through basin outlets (== basin base levels)
  for ibasin in range(nbasins):
    inode = outlets[ibasin]
    # If the outlet is a pit, then I save it
    if iterator_tool.node_type[inode] > 0:
      pits[ipit] = inode
      # and increment the thing
      ipit += 1

  npits = ipit

  return npits


@nb.jit(nopython = True, cache = False)
def _connect_basins(conn_basins, conn_nodes, conn_weights,
          nbasins, basins, outlets, receivers, stack,
          elevation, iterator_tool):
  """Connect adjacent basins together through their lowest pass.

  Creates an (undirected) graph of basins and their connections.

  The resulting graph is defined by:

  - `conn_basins` (nconn, 2): ids of adjacent basins forming the edges
  - `conn_nodes` (nconn, 2): ids of grid nodes forming the lowest passes
    between two adjacent basins.
  - `conn_weights` (nconn) weights assigned to the edges. It is equal to the
    elevations of the passes, i.e., the highest elevation found for each
    node couples defining the passes.

  The function returns:

  - `nconn` : number of edges.
  - `basin0` : id of one open basin (i.e., where `outlets[id]` is not a
    pit node) given as reference.

  The algorithm parses each grid node of the flow-ordered stack and checks if
  the node and (each of) its neighbors together form the lowest pass between
  two different basins.

  Node neighbor lookup doesn't include diagonals to ensure that the
  resulting graph of connected basins is always planar.

  Connections between open basins are handled differently:

  Instead of finding connections between adjacent basins, virtual
  connections are added between one given basin and all other
  basins.  This may save a lot of uneccessary computation, while it
  ensures a connected graph (i.e., every node has at least an edge),
  as required for applying minimum spanning tree algorithms implemented in
  this package.

  """
  iconn = 0

  basin0 = nb.intp(-1)
  ibasin = nb.intp(0)

  conn_pos = np.full(nbasins, -1, dtype=nb.intp)
  conn_pos_used = np.empty(nbasins, dtype=nb.intp)
  conn_pos_used_size = 0

  iactive = False

  for istack in stack:
    irec = receivers[istack]

    # new basin
    if irec == istack:
      ibasin = nb.intp(basins[istack])
      iactive = nb.intp(iterator_tool.node_type[irec])

      for iused in conn_pos_used[:conn_pos_used_size]:
        conn_pos[iused] = -1
      conn_pos_used_size = 0

      if iactive == 0:
        if basin0 == -1:
          basin0 = ibasin
        else:
          conn_basins[iconn] = (basin0, ibasin)
          conn_nodes[iconn] = (-1, -1)
          conn_weights[iconn] = -np.inf
          iconn += 1

    if iactive > 0 :
      for ineighbor in iterator_tool.get_neighbouring_nodes(istack):
        # No data is no good
        if(ineighbor == iterator_tool.nodata):
          continue

        ineighbor_basin = nb.intp(basins[ineighbor])
        ineighbor_outlet = nb.intp(outlets[ineighbor_basin])

        # skip same basin or already connected adjacent basin
        # don't skip adjacent basin if it's an open basin
        if ibasin >= ineighbor_basin and iterator_tool.node_type[ineighbor_outlet]>0:
          continue

        weight = max(elevation[istack], elevation[ineighbor])
        conn_idx = conn_pos[ineighbor_basin]

        # add new connection
        if conn_idx == -1:
          conn_basins[iconn] = (ibasin, ineighbor_basin)
          conn_nodes[iconn] = (istack, ineighbor)
          conn_weights[iconn] = weight

          conn_pos[ineighbor_basin] = iconn
          iconn += 1

          conn_pos_used[conn_pos_used_size] = ineighbor_basin
          conn_pos_used_size += 1

        # update existing connection
        elif weight < conn_weights[conn_idx]:
          conn_nodes[conn_idx] = (istack, ineighbor)
          conn_weights[conn_idx] = weight

  nconn = iconn

  return nconn, basin0






@nb.jit(nopython = True, cache = False)
def _compute_mst_kruskal(conn_basins, conn_weights, nbasins):
  """Compute the minimum spanning tree of the (undirected) basin graph.

  The method used here is Kruskal's algorithm. Applied to a fully
  connected graph, the complexity of the algorithm is O(m log m)
  where `m` is the number of edges.

  """
  mstree = np.empty(nbasins - 1, np.intp)
  mstree_size = 0

  # sort edges
  sort_id = np.argsort(conn_weights)

  uf = UnionFind(nbasins)

  for eid in sort_id:
    b0 = conn_basins[eid, 0]
    b1 = conn_basins[eid, 1]

    if uf.find(b0) != uf.find(b1):
      mstree[mstree_size] = eid
      mstree_size += 1
      uf.union(b0, b1)

  return mstree


@nb.jit(nopython = True, cache =   True)
def _orient_basin_tree(conn_basins, conn_nodes, nbasins, basin0, tree):
  """Orient the graph (tree) of basins so that the edges are directed in
  the inverse of the flow direction.

  If needed, swap values given for each edges (row) in `conn_basins`
  and `conn_nodes`.

  """

  # nodes connections
  nodes_connects_size = np.zeros(nbasins, np.intp)
  nodes_connects_ptr = np.empty(nbasins, np.intp)

  # parse the edges to compute the number of edges per node
  for i in tree:
    nodes_connects_size[conn_basins[i, 0]] += 1
    nodes_connects_size[conn_basins[i, 1]] += 1

  # compute the id of first edge in adjacency table
  nodes_connects_ptr[0] = 0
  for i in range(1, nbasins):
    nodes_connects_ptr[i] = (nodes_connects_ptr[i - 1] +
                 nodes_connects_size[i - 1])
    nodes_connects_size[i - 1] = 0

  # create the adjacency table
  nodes_adjacency_size = nodes_connects_ptr[-1] + nodes_connects_size[-1]
  nodes_connects_size[-1] = 0
  nodes_adjacency = np.zeros(nodes_adjacency_size, np.intp)

  # parse the edges to update the adjacency
  for i in tree:
    n1 = conn_basins[i, 0]
    n2 = conn_basins[i, 1]
    nodes_adjacency[nodes_connects_ptr[n1] + nodes_connects_size[n1]] = i
    nodes_adjacency[nodes_connects_ptr[n2] + nodes_connects_size[n2]] = i
    nodes_connects_size[n1] += 1
    nodes_connects_size[n2] += 1

  # depth-first parse of the tree, starting from basin0
  # stack of node, parent
  stack = np.empty((nbasins, 2), np.intp)
  stack_size = 1
  stack[0] = (basin0, basin0)

  while stack_size > 0:
    # get parsed node
    stack_size -= 1
    node = stack[stack_size, 0]
    parent = stack[stack_size, 1]

    # for each edge of the graph
    for i in range(nodes_connects_ptr[node],
             nodes_connects_ptr[node] + nodes_connects_size[node]):
      edge_id = nodes_adjacency[i]

      # the edge comming from the parent node has already been updated.
      # in this case, the edge is (parent, node)
      if conn_basins[edge_id, 0] == parent and node != parent:
        continue

      # we want the edge to be (node, next)
      # we check if the first node of the edge is not "node"
      if(node != conn_basins[edge_id, 0]):
        # swap n1 and n2
        conn_basins[edge_id, 0], conn_basins[edge_id, 1] = (
          conn_basins[edge_id, 1], conn_basins[edge_id, 0])
        # swap p1 and p2
        conn_nodes[edge_id, 0], conn_nodes[edge_id, 1] = (
          conn_nodes[edge_id, 1], conn_nodes[edge_id, 0])

      # add the opposite node to the stack
      stack[stack_size] = (conn_basins[edge_id, 1], node)
      stack_size += 1


@nb.jit(nopython = True, cache = False)
def _update_pits_receivers_simple(receivers, dist2receivers, outlets,
               conn_basins, conn_nodes, mstree,
               elevation, iterator_tool):
  """Update receivers of pit nodes (and possibly lowest pass nodes)
  based on basin connectivity.

  Distances to receivers are also updated. An infinite distance is
  arbitrarily assigned to pit nodes.

  A minimum spanning tree of the basin graph is used here. Edges of
  the graph are also assumed to be oriented in the inverse of flow direction.

  """
  for i in mstree:
    node_to = conn_nodes[i, 0]
    node_from = conn_nodes[i, 1]
    # print("bulf")
    # print(node_to)

    # skip open basins
    if node_from == -1:
      continue

    outlet_from = outlets[conn_basins[i, 1]]
    # print(outlet_from)
    dist2receivers[outlet_from] = 10000 * iterator_tool.dx * iterator_tool.dy


    if elevation[node_from] < elevation[node_to]:
      receivers[outlet_from] = node_to
    else:
      receivers[outlet_from] = node_from
      receivers[node_from] = node_to

      if node_from % iterator_tool.nx == node_to % iterator_tool.nx:
        dist2receivers[node_from] = iterator_tool.dx
      elif node_from % iterator_tool.ny == node_to % iterator_tool.ny:
        dist2receivers[node_from] = iterator_tool.dy
      else:
        dist2receivers[node_from] = iterator_tool.dxy

@nb.jit(nopython = True, cache = False)
def _update_pits_receivers_carve(receivers, dist2receivers, outlets,
               conn_basins, conn_nodes, mstree,
               elevation, iterator_tool, affect_elevation):
  """Update receivers of pit nodes (and possibly lowest pass nodes)
  based on basin connectivity.

  Distances to receivers are also updated. An infinite distance is
  arbitrarily assigned to pit nodes.

  A minimum spanning tree of the basin graph is used here. Edges of
  the graph are also assumed to be oriented in the inverse of flow direction.

  """
  for i in mstree:
    node_to = conn_nodes[i, 0]
    node_from = conn_nodes[i, 1]
    # print("bulf")
    # print(node_to)

    # skip open basins
    if node_from == -1:
      continue

    outlet_from = outlets[conn_basins[i, 1]]

    n_cur = node_from
    n_next = receivers[n_cur]
    while(n_cur != outlet_from):
      # last_n = n_cur
      n_tmp = receivers[n_next]
      receivers[n_next] = n_cur
      n_cur = n_next
      n_next = n_tmp

    # receivers[n_cur] = last_n
    receivers[node_from] = node_to
    # Done with the carving, now is extra work to affect elevation
    if(affect_elevation ):
      starting_point = outlet_from
      starting_elevation = elevation[outlet_from]
      next_node = receivers[starting_point]
      n_nodes_to_affect = 1
      while(starting_elevation <= elevation[next_node]):
        if(next_node == receivers[next_node]):
          elevation[next_node] = starting_elevation - 0.001
          break
        next_node = receivers[next_node]
        n_nodes_to_affect += 1

      dz = (starting_elevation - elevation[next_node])/n_nodes_to_affect
      endnode = next_node
      curnode = starting_point
      nst = 0
      while(curnode != endnode):
        elevation[curnode] = starting_elevation -  nst * dz
        curnode = receivers[curnode]
        nst += 1





    # print(outlet_from)
    # dist2receivers[outlet_from] = 10000 * iterator_tool.dx * iterator_tool.dy


    # if elevation[node_from] < elevation[node_to]:
    #   receivers[outlet_from] = node_to
    # else:
    #   receivers[outlet_from] = node_from
    #   receivers[node_from] = node_to

    #   if node_from % iterator_tool.nx == node_to % iterator_tool.nx:
    #     dist2receivers[node_from] = iterator_tool.dx
    #   elif node_from % iterator_tool.ny == node_to % iterator_tool.ny:
    #     dist2receivers[node_from] = iterator_tool.dy
    #   else:
    #     dist2receivers[node_from] = iterator_tool.dxy




def correct_flowrouting(receivers, dist2receivers, dist2donors, ndonors, donors,
            stack, nbasins, basins, outlets,
            elevation, iterator_tool, method, affect_elevation):
  """Ensure that no flow is captured in sinks.

  If needed, update `receivers`, `dist2receivers`, `ndonors`,
  `donors` and `stack`.

  """
  nnodes = iterator_tool.nxy

  # theory of planar graph -> max nb. of connections known
  ## BG updated that, might need to be checked
  nconn_max = nbasins * 8

  conn_basins = np.empty((nconn_max, 2), dtype=np.intp)
  conn_nodes = np.empty((nconn_max, 2), dtype=np.intp)
  conn_weights = np.empty(nconn_max, dtype=np.float64)

  nconn, basin0 = _connect_basins(
    conn_basins, conn_nodes, conn_weights,
    nbasins, basins, outlets, receivers, stack,
    elevation, iterator_tool)

  conn_basins = np.resize(conn_basins, (nconn, 2))
  conn_nodes = np.resize(conn_nodes, (nconn, 2))
  conn_weights = np.resize(conn_weights, nconn)

  mstree = _compute_mst_kruskal(conn_basins, conn_weights, nbasins)

  _orient_basin_tree(conn_basins, conn_nodes, nbasins, basin0, mstree)

  if(method == "simple"):
    _update_pits_receivers_simple(receivers, dist2receivers, outlets,
               conn_basins, conn_nodes,
               mstree, elevation, iterator_tool)
  elif(method == "carve"):
    _update_pits_receivers_carve(receivers, dist2receivers, outlets,
               conn_basins, conn_nodes,
               mstree, elevation, iterator_tool, affect_elevation)

  # donors = donors * 0 - 1
  # ndonors = ndonors * 0

  # if(affect_elevation and method != "simple"):
  #   # print("IHUSDF")
  #   receivers = receivers * 0 - 1
  #   compute_Srec_D8(elevation, receivers, dist2receivers, iterator_tool)

  # compute_Srec_donors_D8(donors,ndonors ,receivers, dist2donors, dist2receivers)
  # compute_Sstack(stack, ndonors, donors, receivers, nnodes)



@nb.jit(nopython = True, cache = False)
def stack_checker(Sstack):
  checker = np.zeros_like(Sstack)
  for i in range(Sstack.size):
    checker[Sstack[i]] = i
  return checker



@nb.jit(nopython = True, cache = False)
def multiple_stack_fastscape(D8MStack, D8Mrecs, D8Mnrecs,D8Mndons,iterator_tool):

  n_element = iterator_tool.nxy
  vis = np.zeros(n_element, dtype = np.intp) 
  parse = np.full(n_element,-1, dtype = np.intp) 
  
  nparse = -1
  nstack = -1


  for i in range(n_element):
    if (D8Mndons[i] == 0):
      nparse = nparse + 1
      parse[nparse] = i

    # we go through the parsing stack
    while (nparse > -1):
      ijn = parse[nparse]
      nparse = nparse - 1
      nstack = nstack + 1

      D8MStack[nstack] = ijn

      for ijk in np.arange(D8Mnrecs[ijn], dtype = np.intp):
        ijr = D8Mrecs[ijn,ijk] 
        vis[ijr] = vis[ijr] + 1
        # // if the counter is equal to the number of donors for that node we add it to the parsing stack
        if (vis[ijr] == D8Mndons[ijr]):
          nparse = nparse+1
          parse[nparse] = ijr

@nb.njit()
def accumulate_down_constant_D8S(SStack, D8Srec, value,iterator_tool, dtype = np.float64):
  """
    Accumulate constant values from top to bottom.
    For example drainage area.
    B.G.
  """
  output = np.zeros(iterator_tool.nxy, dtype = dtype)
  for i in SStack[::-1]:
    output[i] += value
    if(i != D8Srec[i]):
      output[D8Srec[i]] += output[i]
  return output

@nb.njit()
def accumulate_down_variable_D8S(SStack, D8Srec, value,iterator_tool, dtype = np.float64):
  """
    Accumulate constant values from top to bottom.
    For example drainage area.
    B.G.
  """
  output = np.zeros(iterator_tool.nxy, dtype = dtype)
  for i in SStack[::-1]:
    output[i] += value[i]
    if(i != D8Srec[i]):
      output[D8Srec[i]] += output[i]
  return output


@nb.njit()
def mask_from_range_downstream_accumulator_D8S(SStack, D8Srec, DAQ, acc_array, min_value, max_value = np.inf):
  """
  Iterates through the inversed stack (Upstrem to downstream), finds the value at which the minimum value is encountered while the maximum is not
   and mask the upstream nodes.
  Typical example:
    - masking all basin between a given drainage area min and max
    - masking all basins above a certain threshold
  B.G.
  """

  mask = np.full_like(SStack, False, dtype = np.bool)
  trange = np.arange(SStack.shape[0] - 1, 0,1)

  for i in trange:
    node = SStack[i]
    
    if(mask[node]):
      continue
    
    if(DAQ[node] < min_value or DAQ[node] > max_value):
      continue

    if(DAQ[D8Srec[node]] < max_value):
      continue

    tndons = acc_array[node]
    mask[node:node+tndons] = True

  return mask




























# End Of File



