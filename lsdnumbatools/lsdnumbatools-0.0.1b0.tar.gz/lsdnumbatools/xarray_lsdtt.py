import xarray as xr
import numpy as np
import numba as nb
import lsdnumbatools.node_graph as NG
import lsdnumbatools.mask_tools as MT
import lsdnumbatools.utils as ut


class DEM(object):
  """docstring for DEM"""
  def __init__(self):
    """Initiate a DEM object to None and documents the attributes"""
    # Generic object constructor
    super(DEM, self).__init__()

    # Node graph: everything related to coordinates, neighbours, iteration, topological order, distances, nodes to row/col conversions ...
    self.graph = None

    # Main xarray dataset: contains all the data directly linked to the DEM
    self.ds = None

  def set_main_raster(self, array, nx, ny, dx, dy, node_type = None, xmin = None, xmax = None, ymin = None, ymax = None, ymin_bottom = True):
    
    # Initialising the graph
    self.graph = NG.graph()
    
    # if the node type is not given, I default classic boundaries (external = open, internal = normal) 
    # This will be the hge majority of the cases for topographic analysis on real rasters
    # periodic boundaries and specific ones will be for models only I guess
    if(node_type is None):
      node_type = np.ones_like(array, dtype = np.int16).reshape(ny,nx)
      node_type[0,:] = 0
      node_type[-1,:] = 0
      node_type[:,0] = 0
      node_type[:,-1] = 0

    # Build the graph skeleton (setting raw dimensions, and iterations tools)
    # It does NOT compute the neightbours and all, it is just getting ready for it
    self.graph.initiatialise(nx, ny, dx, dy, node_type, array.ravel())

    # If the bounding box is not defined, I just consider the outlet at 0,0 bottom left corner
    if(xmin is None):
      xmin = 0
      xmax = (nx + 1) * dx
      ymin = 0
      ymax = (ny + 1) * dy

    # Setting the extent in the graph
    self.graph.set_extent(xmin,xmax,ymin,ymax, ymin_bottom = ymin_bottom)
    # Copying the dimensions of the graph (x,y,n_nodes,n_neighbours)
    self.ds.dims = self.graph.ds.dims
    # Loading the topography
    self.ds["topography"] = (("y","x"), array)

  def load_main_raster(self, fname = "dem.tif"):
    """
    Load the main raster file into the DEM object. it will be registered as "topography" and will be utilised by the subsequent calculations.
    The main raster also sets the dimensions of the DEM
    """
    try:
      import rasterio as rio
      from rasterio.transform import from_bounds
    except:
      print("rasterio is not installed correctly and is needed to load external rasters")
      raise 

    

    # Loading the raster with rasterio
    this_raster = rio.open(fname)

    array = this_raster.read(1)
        # I am padding a no_data contour
    self.graph = NG.graph()


    node_type = np.ones_like(array, dtype = np.int16) 
    node_type[0,:] = 0
    node_type[-1,:] = 0
    node_type[:,0] = 0
    node_type[:,-1] = 0

    self.graph.initiatialise(array.shape[1], array.shape[0], abs(this_raster.res[0]), abs(this_raster.res[1]), node_type, array.ravel())
    
    # gt = this_raster.res
    # self.graph.ds['x_min'] = gt[0]
    self.graph.ds["x_min"] = this_raster.bounds[0]
    self.graph.ds["y_min"] = this_raster.bounds[1]
    self.graph.ds["x_max"] = this_raster.bounds[2]
    self.graph.ds["y_max"] = this_raster.bounds[3]
    # self.graph['dy'] = gt[1]
    # # self.graph['nx'] = array.shape[1]
    # # self.graph['ny'] = array.shape[0]

    # print (this_raster.bounds[0],this_raster.bounds[2],this_raster.bounds[1],this_raster.bounds[3])
    self.graph.set_extent(this_raster.bounds[0],this_raster.bounds[2],this_raster.bounds[1],this_raster.bounds[3], ymin_bottom = True)
    # Initialising a dictionary containing the raster info for output

    try:
      self.graph.ds['crs'] = this_raster.crs['init']
    except (TypeError, KeyError) as e:
      self.graph.ds['crs'] = u'epsg:32601'

    self.graph.ds['nodata'] = ('nodata',list(this_raster.nodatavals))
    # self.ds.dims = self.graph.ds.dims
    self.ds = xr.Dataset()
    self.ds["y"] = self.graph.ds["y"]
    self.ds["x"] = self.graph.ds["x"]
    self.ds["topography"] = (("y","x"), array)


  def compute_graph(self, single_flow = True, multiple_flow = False, local_minima = "simple", affect_elevation = True):
    if(single_flow):
      self.graph.compute_D8S_graph()
      if(local_minima.lower() != "none"):
        print("Correcting flow")
        self.graph.correct_D8S_depressions( method = local_minima, affect_elevation = affect_elevation)
    if(multiple_flow):
      self.graph.compute_D8M_graph()

    if(affect_elevation):
      self.ds["topography"] = ("y","x"),self.graph.ds["topography"].values.reshape(int(self.graph.ds["ny"].values),int(self.graph.ds["nx"].values))


  def mask_watershed(self, ID_MASK ,method = "main_basin", multiple = False, masks = []):    
    if(len(masks) > 0):
      tmask = ut.combine_masks(self,masks, intersect = True)
    else:
      tmask = None
    self.ds[ID_MASK] = ("n_nodes", MT.dispatch_watershed_methods(self,method, multiple, mask = tmask) )
    return ID_MASK

  def save_raster(self, key, crs, fname, fmt = 'GTIFF'):
    '''
      Save a raster at fname. I followed tutorial there to do so : https://rasterio.readthedocs.io/en/latest/quickstart.html#creating-data
      Arguments:
        Z (2d numpy array): the array
        x_min (float): x min
        y_min (float): y min
        x_max (float): x max
        y_max (float): y max
        res (float): resolution
        crs: coordinate system code (usually you will call it from a dem object, just give it dem.crs)
        fname: path+name+.tif according to your OS  ex: Windows: C://Data/Albania/Holtas/Holt.tif, Linux: /home/Henri/Albania/Shenalvash/She_zoom.tif
        fmt (str): string defining the format. "GTIFF" for tif files, see GDAL for option. WARNING: few outputs are buggy, FOR EXAMPLE "ENVI" bil format can be with the wrong dimensions.
      Returns:
        Nothing but saves a raster with the given parameters
      Authors: 
        B.G. 
      Date:
        08/2018
    '''
    try:
      import rasterio as rio
      from rasterio.transform import from_bounds
    except:
      print("rasterio is not installed correctly and is needed to load external rasters")
      raise 


    transform = from_bounds(float(self.graph.ds["x_min"].values), float(self.graph.ds["y_min"].values),
     float(self.graph.ds["x_max"].values), float(self.graph.ds["y_max"].values), int(self.graph.ds["ny"].values), int(self.graph.ds["nx"].values))

    new_dataset = rio.open(fname, 'w', driver=fmt, height=int(self.graph.ds["ny"].values), width=int(self.graph.ds["nx"].values), count=1, dtype=self.ds[key].values.dtype.type, crs=crs, transform=transform, nodata = -9999)
    new_dataset.write(self.ds[key].values, 1)
    new_dataset.close()









