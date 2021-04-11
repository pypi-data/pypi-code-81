import tempfile
from os.path import join

# arr = np.random.rand(1024, 1024)
# serve(arr)  # creates an in-memory store if not zarr.Array or zarr.Group
from dexp.datasets.operations.serve import dataset_serve
from dexp.datasets.zarr_dataset import ZDataset

with tempfile.TemporaryDirectory() as tmpdir:
    print('created temporary directory', tmpdir)

    zdataset = ZDataset(path=join(tmpdir, 'test.zarr'),
                        mode='w',
                        store='dir')

    array = zdataset.add_channel(name='first',
                                 shape=(10, 100, 100, 100),
                                 chunks=(1, 50, 50, 50),
                                 dtype='f4',
                                 codec='zstd',
                                 clevel=3)

    # we initialise almost everything:
    array[...] = 13

    dataset_serve(zdataset)
