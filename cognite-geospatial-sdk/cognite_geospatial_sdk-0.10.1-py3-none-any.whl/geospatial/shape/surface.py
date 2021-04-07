# Copyright 2020 Cognite AS

import copy

import numpy as np
from cognite.geospatial.visualization import Plot
from scipy.interpolate import griddata

from .affine import AffineTransformation
from .box import Box2
from .geometry_definition import GeometryDefinition
from .index import Index2, Position2


class Surface(Plot):
    """Surface is regularly gridded surface with an associated GeometryDefinition described the grid.

    Examples
    --------
    >>> surface = Surface(data = np.random.rand(300,2) )
    >>> surface.geometry.origin = [100, 100]
    >>> surface.geometry.grid_bottom_right = [500, 800]
    >>> surface.geometry.update_extent()
    >>> surface = surface.interpolate_to_grid()
    """

    def __init__(self, data, grid=None, geometry: GeometryDefinition = None, name: str = None, id: int = None):
        self.id = id
        self.name = name
        self.data = np.array(data)
        if grid is None:
            self.grid = None
        else:
            self.grid = np.array(grid, dtype=np.int32)
        self.is_gridded = grid is not None

        if geometry is None:
            self.geometry = GeometryDefinition()
            if len(data) > 0:
                self._update_extent_from_point(self.data, self.geometry)
                self.geometry.origin = self.geometry.top_left
        else:
            self.geometry = geometry

    @property
    def mean_x(self) -> float:
        """Mean X value

        Returns:
            Mean X float64
        """
        return np.mean(self.data[:, 0])

    @property
    def mean_y(self) -> float:
        """Mean Y value

        Returns:
            Mean Y float64
        """
        return np.mean(self.data[:, 1])

    @property
    def mean_z(self) -> float:
        """Mean Z value

        Returns:
            Mean Z float64
        """
        if self.data.shape[1] <= 2:
            return np.nan
        return np.mean(self.data[:, 2])

    @property
    def points(self):
        """Surface points

        Returns:
            points arrays
        """
        return self.data

    @property
    def extent(self):
        """Extent of the surface

        Returns:
           array: Geometry extent
        """
        return self.geometry.extent

    @property
    def grid_box(self):
        """Get grid box

        Returns:
            array (int): top left and bottom right coordinate
        """
        grid_box = self._layer_meta().grid_box()
        if grid_box is not None:
            return np.array([self.geometry.grid_top_left, self.geometry.grid_bottom_right], dtype=np.int32)
        return None

    def attribute(self, i: int = 0):
        width = self.geometry.grid_width
        height = self.geometry.grid_height
        rows = np.array(self.grid[:, 0] - self.geometry.grid_min_j, dtype=np.int32)
        columns = np.array(self.grid[:, 1] - self.geometry.grid_min_i, dtype=np.int32)

        attribute = np.zeros((width, height), dtype=np.float32)
        attribute[columns, rows] = self.data[:, i + 2]

        return attribute

    def attributes(self):
        """Attribute values

        Returns:
            Attributes matrix
        """
        data_shape = self.data.shape
        size = data_shape[1] - 2
        width = self.geometry.grid_width
        height = self.geometry.grid_height
        rows = np.array(self.grid[:, 0] - self.geometry.grid_min_j, dtype=np.int32)
        columns = np.array(self.grid[:, 1] - self.geometry.grid_min_i, dtype=np.int32)

        attributes = np.zeros((size, width, height), dtype=np.float32)
        attributes[:, columns, rows] = self.data[:, 2:].T

        return attributes

    def crop(self, box: Box2):
        """Crop surface by X, Y location

        Args:
            box (Box2) - the bounded box
        Returns:
            Surface within a bounded box
        """
        indexes = np.all(np.logical_and(box.lower_left <= self.data, self.data <= box.upper_right), axis=1)
        filtered_grid = np.array(self.grid[indexes], copy=True)
        filtered_data = np.array(self.data[indexes], copy=True)

        filtered_geometry = copy.deepcopy(self.geometry)

        min_grid = np.min(filtered_grid, axis=0)
        max_grid = np.max(filtered_grid, axis=0)
        filtered_geometry.grid_top_left = Index2(max_grid)
        filtered_geometry.grid_bottom_right = Index2(min_grid)

        self._update_extent_from_point(filtered_data, filtered_geometry)

        return Surface(data=filtered_data, grid=filtered_grid, geometry=filtered_geometry, name=self.name)

    def window(self, row_range, column_range):
        """Window (crop) out part of the surface.

        Args:
            row_range (array): A window for row (min,max)
            column_range (array): A window for column (min,max)

        Returns:
            Surface within a window
        """
        if not self.is_gridded:
            raise Exception("Surface not grided! Grid the surface before using this function.")

        row_ind = Index2(row_range)
        col_ind = Index2(column_range)
        indexes = np.argwhere(
            (self.grid[:, 0] >= row_ind.i)
            & (self.grid[:, 0] < row_ind.j)
            & (self.grid[:, 1] >= col_ind.i)
            & (self.grid[:, 1] < col_ind.j)
        )
        indexes = indexes.reshape(len(indexes))
        filtered_grid = np.array(self.grid[indexes], copy=True)
        filtered_data = np.array(self.data[indexes], copy=True)

        filtered_geometry = copy.deepcopy(self.geometry)
        filtered_geometry.grid_top_left = Index2(row_ind.i, col_ind.i)
        filtered_geometry.grid_bottom_right = Index2(row_ind.j - 1, col_ind.j - 1)

        self._update_extent_from_point(filtered_data, filtered_geometry)

        return Surface(data=filtered_data, grid=filtered_grid, geometry=filtered_geometry, name=self.name)

    def _update_extent_from_point(self, data, geometry):
        min_coord = np.min(data, axis=0)
        max_coord = np.max(data, axis=0)

        geometry._top_left = Position2(min_coord[0], max_coord[1])
        geometry._top_right = Position2(max_coord[0:2])
        geometry._bottom_right = Position2(max_coord[0], min_coord[1])
        geometry._bottom_left = Position2(min_coord[0:2])

    def sample(self, data_sampling):
        """Sample surface

        Args:
            data_sampling (int): take each N point
        Returns:
            Sampled surface
        """
        data = np.array(self.data[::data_sampling, :], copy=True)
        sample_geometry = copy.deepcopy(self.geometry)

        min_coord = np.min(data, axis=0)
        max_coord = np.max(data, axis=0)

        sample_geometry._top_left = Position2(min_coord[0], max_coord[1])
        sample_geometry._top_right = Position2(max_coord[0:2])
        sample_geometry._bottom_right = Position2(max_coord[0], min_coord[1])
        sample_geometry._bottom_left = Position2(min_coord[0:2])

        grid = None
        if self.grid is not None:
            grid = np.array(self.grid[::data_sampling, :], copy=True)
            min_grid = np.min(grid, axis=0)
            max_grid = np.max(grid, axis=0)

            sample_geometry._grid_top_left = Index2(min_grid[0:2])
            sample_geometry._grid_bottom_right = Index2(max_grid[0:2])

        return Surface(data=data, grid=grid, geometry=sample_geometry, name=self.name)

    def interpolate_to_grid(self, geometry=None, method="cubic", fill_value=np.nan):
        """Interpolate unstructured data to the grid using geometry. If geometry is not provided use own geometry.

        Args:
            geometry (GeometryDefinition, optional): geometry to make a grid
            method (str, optional): {'linear', 'nearest', 'cubic'} Cubic interpolation is default.
                    nearest - return the value at the data point closest to the point of interpolation.
                    linear - tessellate the input point set to N-D simplices, and interpolate linearly on each simplex.
                    cubic - return the value determined from a piecewise cubic.
            fill_value (float, optional): Value used to fill in for requested points outside of the convex hull of the input points. If not provided, the the default is nan.
        Returns:
            Interpolated surface
        """
        if geometry is None:
            use_geometry = self.geometry
        else:
            use_geometry = geometry

        X, Y = use_geometry.xy_grid_mesh()
        data_on_grid = griddata(self.data[:, :2], self.data[:, 2:], (X, Y), method=method, fill_value=fill_value)
        data = np.stack((X.flatten(), Y.flatten(), data_on_grid.flatten()), axis=-1)

        row, column = use_geometry.row_column_grid_mesh()
        grid = np.stack((row.flatten(), column.flatten()), axis=-1)

        return Surface(data=data, grid=grid, geometry=copy.deepcopy(use_geometry), name=self.name)

    def _apply_transformation(self, transformation):
        points = transformation.transform(self.data[:, :2])
        data_shape = self.data.shape
        if data_shape[1] > 2:
            return np.hstack((points, self.data[:, 2:]))

        return points

    def _update_geometry(self, transformation):
        new_geometry = copy.deepcopy(self.geometry)
        extent = [
            self.geometry.top_left,
            self.geometry.top_right,
            self.geometry.bottom_right,
            self.geometry.bottom_left,
            self.geometry.origin,
        ]
        new_extent = transformation.transform(extent)
        new_geometry.affine = new_geometry.affine.compose(transformation)

        new_geometry.top_left = new_extent[0]
        new_geometry.top_right = new_extent[1]
        new_geometry.bottom_right = new_extent[2]
        new_geometry.bottom_left = new_extent[3]
        new_geometry.origin = new_extent[4]
        return new_geometry

    def translate(self, origin):
        """Translate surface to X, Y

        Args:
            origin (array): X, Y to translate points
        Returns:
            Translated Surface
        """
        transformation = AffineTransformation()
        transformation = transformation.translate(origin)
        return self._apply_full(transformation)

    def rotate(self, theta):
        """Rotate surface

        Args:
            theta (float): angle
        Returns:
            Rotated Surface
        """
        transformation = AffineTransformation()
        transformation = transformation.translate(-self.geometry.origin)
        transformation = transformation.rotate(theta)
        transformation = transformation.translate(self.geometry.origin)
        return self._apply_full(transformation)

    def scale(self, scale):
        """Scale surface

        Args:
            scale (array): X, Y scale directions
        Returns:
            Scaled Surface
        """
        transformation = AffineTransformation()
        transformation = transformation.translate(-self.geometry.origin)
        transformation = transformation.scale(scale)
        transformation = transformation.translate(self.geometry.origin)
        return self._apply_full(transformation)

    def _apply_full(self, transformation):
        new_data = self._apply_transformation(transformation)
        new_geometry = self._update_geometry(transformation)

        return Surface(data=new_data, grid=self.grid, geometry=new_geometry, name=self.name)

    def move_to_geometry(self, geometry=None, to_grid=False):
        """Move to geometry

        Args:
            geometry (GeometryDefinition): Move to geometry. If geometry is None use surface geometry.
        Returns:
            Moved Surface
        """
        if geometry is None:
            geometry = self.geometry
        transformation = geometry.to_compute_grid_transformation(to_grid=to_grid)
        return self._apply_full(transformation)

    def __str__(self):
        return f"Surface: {self.name}\nGeometry\n{self.geometry}"

    def __repr__(self):
        return self.__str__()
