"""
Small API managing the non-numba part of the masking tools
"""
import numpy as np
import xarray as xr
import lsdnumbatools._mask_tools as _MT

def dispatch_watershed_methods(xalsd,method, multiple, mask = None, **kwargs):
  """
    ingest the methods and arguments for the watershed masking from a xarray lsd object.
    Also performs the checks, debugs and things like that.
  """
  # Initialising the output to nothing in order to track any fail
  makoutput = None

  # Checking the mask
  if(mask == None):
    # if none, then I create an all_true mask
    mask = xalsd.graph.ds["all_true"].values.view()

  # My method is main_basin: extracting the largest basin in the thing
  if(method == "main_basin"):
    # Checking if the accumulation raster is already produced
    if("NodeAccSF" not in list(xalsd.ds.keys())):
      xalsd.ds["NodeAccSF"] = ("n_nodes", xalsd.graph.accumulate_down_constant_D8S(1, dtype = np.int32))

    # Getting the node ID of the max thingy
    node = np.argmax(xalsd.ds["NodeAccSF"].values)
    # print(xalsd.ds["NodeAccSF"].values[node])

    if(multiple == False):
      makoutput = _MT.mask_upstream_from_node_ID_SF(node, xalsd.graph.ds["SStack"].values, xalsd.graph.ds["D8Srec"].values, xalsd.ds["NodeAccSF"].values, xalsd.graph.ds["argSstack"].values, mask)
    else:
      makoutput = _MT.mask_upstream_from_node_ID_MF(node, xalsd.graph.ds["SStack"].values, xalsd.graph.ds["D8Srec"].values, xalsd.graph.ds["D8Mrecs"].values,
       xalsd.graph.ds["D8Mdons"].values, xalsd.graph.ds["D8Mndons"].values, xalsd.graph.ds["D8Mnrecs"].values, xalsd.ds["NodeAccSF"].values, xalsd.graph.ds["argSstack"].values, mask)
  return makoutput



