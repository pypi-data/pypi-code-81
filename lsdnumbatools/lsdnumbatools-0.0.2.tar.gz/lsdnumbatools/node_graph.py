"""
  This module contains all the algorithms organising the nodes together:
    - donors, receivers computation
    - topological ordering
    - graph transersals
    - isolating subgraph (e.g. watershed)
"""
import numba as nb
import numpy as np
import xarray as xr
from ._union_find import UnionFind
from ._looper import iterasator
# from ._node_graph import *
import lsdnumbatools._node_graph as _NG


class graph(object):
  """docstring for node_graph"""
  def __init__(self):
    
    # Generic object constructor
    super(graph, self).__init__()
    # Initialising the dataset
    self.ds = xr.Dataset()
    # this numba class will need to be reconstructed at each launch
    self.iterator_tool = None

  def initiatialise(self,nx,ny,dx,dy,node_type,topography):
    """
      Initialise a Dataset from scratch and create the iterator_tool
    """
    # Number of cols
    self.ds["nx"] = nx
    # Number of rows
    self.ds["ny"] = ny
    # spacing in x dimension
    self.ds["dx"] = dx
    # Spacing in Y dimnsion
    self.ds["dy"] = dy
    # Number of elements
    self.ds["nxy"] = nx * ny
    self.ds["shape"] = ('shape_dim',[ny , nx])
    # node type (see inexisting doc for info haha)
    self.ds["node_type"] = ("n_nodes", node_type.ravel())
    # Topography used to generate the data
    self.ds["topography"] = ("n_nodes", topography.ravel())
    # Iterasator
    self.iterator_tool = iterasator(self.ds["node_type"].values,nx,ny,dx,dy)
    # an all_true mask
    self.ds["all_true"] = ("n_nodes", np.ones( nx * ny, dtype = np.int8) )




  def compute_D8S_graph(self, recursive = True):
    print("Building the SF-graph ", end = "...")
    self.compute_D8S_graph_nostack()
    print("... OK!")
    print("Building the SF-topological order", end = "...")
    if(recursive):
      _NG.compute_Sstack(self.ds["SStack"].values, self.ds["D8Sndons"].values, self.ds["D8Sdons"].values, self.ds["D8Srec"].values, self.iterator_tool.nxy)
    if(recursive == False):
      _NG.compute_Sstack_norecursions(self.ds["SStack"].values, self.ds["D8Sndons"].values, self.ds["D8Sdons"].values, self.ds["D8Srec"].values, self.iterator_tool.nxy)
    _NG.compute_argstack(self.ds["SStack"].values,self.ds["argSstack"].values)
    print("... OK!")

  def compute_D8S_graph_nostack(self):
    #Initalising the arrays to the right format
    self.ds["D8Srec"] = (("n_nodes"),np.zeros(self.iterator_tool.nxy, dtype = np.int32))
    self.ds["SStack"] = (("n_nodes"),np.zeros(self.iterator_tool.nxy, dtype = np.int32))
    self.ds["argSstack"] = (("n_nodes"),np.zeros(self.iterator_tool.nxy, dtype = np.int32))
    self.ds["D8Sdist"] = (("n_nodes"),np.zeros(self.iterator_tool.nxy, dtype = np.float32))
    self.ds["D8Sdons"] = (("n_nodes", "n_neighbours"),np.zeros((self.iterator_tool.nxy,8), dtype = np.int32))
    self.ds["D8Sdondist"] = (("n_nodes", "n_neighbours"),np.zeros((self.iterator_tool.nxy,8), dtype = np.float32))
    self.ds["D8Sndons"] = (("n_nodes"),np.zeros(self.iterator_tool.nxy, dtype = np.int32))

    # Processing
    _NG.compute_Srec_D8(self.ds["topography"].values, self.ds["D8Srec"].values, self.ds["D8Sdist"].values, self.iterator_tool)
    _NG.compute_Srec_donors_D8(self.ds["D8Sdons"].values, self.ds["D8Sndons"].values, self.ds["D8Srec"].values, self.ds["D8Sdondist"].values, self.ds["D8Sdist"].values)

  def compute_D8S_only_stack(self,recursive = True):
    if(recursive):
      _NG.compute_Sstack(self.ds["SStack"].values, self.ds["D8Sndons"].values, self.ds["D8Sdons"].values, self.ds["D8Srec"].values, self.iterator_tool.nxy)
    if(recursive == False):
      _NG.compute_Sstack_norecursions(self.ds["SStack"].values, self.ds["D8Sndons"].values, self.ds["D8Sdons"].values, self.ds["D8Srec"].values, self.iterator_tool.nxy)
    

  def compute_D8M_graph(self):
    print("Building the MF-graph ", end = "...")
    self.ds["D8Mrecs"] = (("n_nodes", "n_neighbours"), np.full((self.iterator_tool.nxy,8),-1, dtype = np.int32))
    self.ds["D8Mdons"] = (("n_nodes", "n_neighbours"), np.full((self.iterator_tool.nxy,8),-1, dtype = np.int32))
    self.ds["D8Mnrecs"] = (("n_nodes"), np.zeros(self.iterator_tool.nxy, dtype = np.int32))
    self.ds["D8Mndons"] = (("n_nodes"), np.zeros(self.iterator_tool.nxy, dtype = np.int32))
    self.ds["D8MStack"] = (("n_nodes"), np.zeros(self.iterator_tool.nxy, dtype = np.int32))
    self.ds["D8Mdist"] = (("n_nodes", "n_neighbours"), np.zeros((self.iterator_tool.nxy, 8), dtype = np.float32))
    self.ds["D8Mdondist"] = (("n_nodes", "n_neighbours"), np.zeros((self.iterator_tool.nxy, 8), dtype = np.float32))

    _NG.compute_Mrec_D8(self.ds["topography"].values, self.ds["D8Mrecs"].values, self.ds["D8Mdist"].values, self.ds["D8Mnrecs"].values, self.ds["D8Mdons"].values, self.ds["D8Mndons"].values, self.ds["D8Mdondist"].values, self.iterator_tool)
    print("... OK!")
    print("Building the MF-topological order ", end = "...")
    _NG.multiple_stack_fastscape(self.ds["D8MStack"].values, self.ds["D8Mrecs"].values, self.ds["D8Mnrecs"].values,self.ds["D8Mndons"].values,self.iterator_tool)
    print("... OK!")

  def correct_D8S_depressions(self, method = "simple", affect_elevation = True):

    self.ds["D8Basins"] = ("n_nodes", np.zeros(self.iterator_tool.nxy, dtype = np.int32))

    outlets = np.empty(self.iterator_tool.nxy, dtype = np.int32)
    pits = np.empty(self.iterator_tool.nxy, dtype = np.int32)

    self.ds["n_basins"] = _NG.compute_basins_Srec(self.ds["D8Basins"].values, outlets,
     self.ds["SStack"].values, self.ds["D8Srec"].values, self.iterator_tool.nxy)
    outlets.resize(self.ds["n_basins"].values)
    self.ds["outlets"] = ("n_outlets", outlets)

    if(self.ds["n_basins"] > 0):

      self.n_pits = _NG.compute_pits(pits, self.ds["outlets"].values, int(self.ds["n_basins"].values), self.iterator_tool)
      pits.resize(self.n_pits)
      self.ds["pits"] = ("n_pits", pits)

      _NG.correct_flowrouting(self.ds["D8Srec"].values, self.ds["D8Sdist"].values, self.ds["D8Sdondist"].values, self.ds["D8Sndons"].values, self.ds["D8Sdons"].values,
              self.ds["SStack"].values, int(self.ds["n_basins"].values), self.ds["D8Basins"].values, self.ds["outlets"].values,
              self.ds["topography"].values, self.iterator_tool, method, affect_elevation)

      self.compute_D8S_graph()

  # def carve_depressions_experimental(self):
  #   """
  #     Uses the algorithm from Cordonnier et al., 2019 to carve the depressions.
  #   """
  #   # First recomputing the D8 receivers (could be otpimise)
  #   new_receivers = self.ds["D8Srec"].values[self.ds["pits"].values]
  #   original_rec = np.zeros(self.iterator_tool.nxy, dtype = np.int32)
  #   original_dist = np.zeros(self.iterator_tool.nxy, dtype = np.int32)
  #   _NG.compute_Srec_D8(self.ds["topography"].values, original_rec, 
  #     original_dist, self.iterator_tool)

  #   # Now sending to numba
  #   _NG.carve_me_dem(self.ds["topography"].values, original_rec, 
  #     self.ds["pits"].values, new_receivers, self.ds["D8Basins"].values, self.iterator_tool)



  def accumulate_down_constant_D8S(self, value,return_2D = False, dtype = np.float64):
    """
      Accumulate variable values from top to bottom.
      For example precipitation.
      B.G.
    """
    output = _NG.accumulate_down_constant_D8S(self.ds["SStack"].values, self.ds["D8Srec"].values, value,self.iterator_tool, dtype = dtype)
    if(return_2D):
      return output.reshape(int(self.ds["ny"].values), int(self.ds["nx"].values))
    else:
      return output

  def accumulate_down_variable_D8S(self, value,return_2D = False, dtype = np.float64):
    """
      Accumulate variable values from top to bottom.
      For example precipitation.
      B.G.
    """
    output = _NG.accumulate_down_variable_D8S(self.ds["SStack"].values, self.ds["D8Srec"].values, value,self.iterator_tool, dtype = np.float64)
    if(return_2D):
      return output.reshape(self.ds["ny"], self.ds["nx"])
    else:
      return output

  def set_extent(self,xmin,xmax,ymin,ymax, ymin_bottom = True):

    self.ds["extent"] = ("extent",[xmin,xmax,ymin,ymax])
    self.ds["ymin_bottom"] = ymin_bottom
    self.ds["xmin"] = xmin
    self.ds["xmax"] = xmax
    self.ds["ymin"] = ymin
    self.ds["ymax"] = ymax
    # self.ds.dims["x"] =
    
    Y = np.arange(ymin, ymax, self.ds["dy"].values) + self.ds["dy"].values/2

    if(ymin_bottom):
      Y = Y[::-1]

    self.ds["y"] = ("y",Y)
    self.ds["x"] = (("x"), np.arange(xmin, xmax, self.ds["dx"].values) + self.ds["dx"].values/2)

  def xy2rowcol(self, x,y):
    """
      Converts an array or scalar of XY coordinates to row col
    """

    col = (x - self.ds.extent.values[0]) / self.ds.dx.values
    col = np.floor(col)

    row = (y - self.ds.extent[2].values) / self.ds.dy.values
    if(self.ds.ymin_bottom.values):
      row = np.ceil(row)
      row = self.ny - row
    else:
      row = np.floor(row)
    return row, col













  # end of file