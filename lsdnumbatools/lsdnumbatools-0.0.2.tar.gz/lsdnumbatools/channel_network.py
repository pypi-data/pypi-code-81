import numpy as np
import numba as nb
import lsdnumbatools._SFchannel_network as _Scn

class ChannelNetwork(object):
  """Abstract class for the channel networks"""
  def __init__(self, a_node_graph):

    super(ChannelNetwork, self).__init__()

    # The reference node graph
    self.node_graph = a_node_graph

    # The river ID converter
    self.riverID2nodeID = None
    self.nodeID2riverID = None

    # The river ID graph
    self.river_rec = None
    self.river_dons = None
    self.river_stack = None

    self.n_nodes = None
    self.mask_mother_dem = None

    self.river_dist2rec = None
    self.river_dist2dons = None

class SFChannelNetwork(ChannelNetwork):
  """Single flow channel network"""
  def __init__(self, a_node_graph, sources):
    
    super(SFChannelNetwork, self).__init__(a_node_graph)

    # Calling the function computing the local river graph 
    (self.nodeID2riverID, self.riverID2nodeID, self.river_rec, self.river_dons, 
      self.river_dist2rec, self.river_dist2dons, self.river_stack, self.mask_mother_dem)  =  \
      _Scn.restack_from_source_ID_S8S(self.node_graph.SStack, self.node_graph.SStackID, self.node_graph.D8Srec, 
      self.node_graph.D8Sndons, self.node_graph.D8Sdons, self.node_graph.D8Sdist, self.node_graph.D8Sdondist, sources)

    # graph constructed



    # Deriving secondary attributes
    ## Number of nodes
    self.n_nodes = self.river_stack.shape[0]
    ## Sources in river referential:
    self.sources = self.nodeID2riverID[sources]
    ## node dimension
    self.node_dim = np.arange(self.n_nodes)
    ## outlets
    self.outlets = self.node_dim[self.node_dim == self.river_rec[self.node_dim]]
    ## rows and cols
    self.rows = self.riverID2nodeID // self.node_graph.nx
    self.cols = self.riverID2nodeID % self.node_graph.nx
    ## distance from outlet
    self.distance_from_outlet = _Scn.compute_distance_from_outlets(self.river_stack, self.river_rec, self.river_dist2rec, dtype = np.float32)
    ## distance from sources
    self.distance_from_sources, self.river_ID = _Scn.compute_max_distance_from_sources(self.river_stack, self.river_rec, self.river_dist2rec, dtype = np.float32)








































    # End of file

    