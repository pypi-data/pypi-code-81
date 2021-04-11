# import dask.array as da
# arr = da.from_zarr("http://localhost:8000/first/first")
#
# from napari import Viewer, gui_qt
#
# with gui_qt():
#     viewer = Viewer()
#     viewer.add_image(arr, name='arr', visible=True)
from dexp.datasets.operations.view import dataset_view

dataset_view('http://localhost:8000')
