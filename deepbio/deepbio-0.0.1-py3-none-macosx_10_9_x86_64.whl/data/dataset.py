"""The dataset module defines the core `Dataset` class.

A `Dataset` should be instantiated from any single filetype or directory
tarball, with the same developer facing API and everything should "just work".

The same code will scale from small numpy arrays to pedabytes of disk data with
native data parallel and distributed support with downstream `Dataloader`s.

Example:
    You can instantiate `Dataset`s with various levels of parameterization.
    literal blocks::

        antibodies = deepbio.data.Dataset("cancer_cure.csv")
        chrom11_chipseq = deepbio.data.Dataset("genomics.tar")

Sensible defaults for parsing different filetypes are included out-of-the-box.
Internals are of course easily parameterized via kwargs.

Todo:
    * Support for `.json`
    * Support for creation of custom tarball directories
"""

import os

import torch
import webdataset_latch as wd


class Dataset(torch.utils.data.IterableDataset):

    """Dataset is the core data representation in DeepBio.

    The class should be flexibly instantiated from any filetype or in-memory
    primitive. Downstream interactions with `DataLoader`s or `Model`s are then
    guranteed to play nice.

    Datasets hold the necessary information to lazily load and transform data,
    ie. file path, metadata, allowing the class the be instantiated with
    massive files and directories as easily as in-memory structures like python
    lists.

    Attributes:
        X (:obj:`Iterable`): Core datapoints
        y (:obj:`Iterable`, optional): Optional labels (one-to-one mapping)
    """

    def __init__(self, file_path: str, X: str = None, y: str = None):
        """Dataset should be consistently instantiated for all filetypes.

        Args:
            file_path: Location of data file.
            X (optional): Metadata annotation (ie. csv column header) to
                identitfy X.
            y (optional): Metadata annotation (ie. csv column header) to
                identitfy y.
        """
        super(Dataset).__init__()

        self.handle = file_path

        # Parse filetype and conditionally instantiate.
        _, ftype = os.path.splitext(file_path)
        ftype = ftype[1:]

        if ftype == "tar":

            self._wd_dataset = wd.Dataset(
                file_path).decode().to_tuple("x*", "y*")

        elif ftype == "csv":

            # When reading the csv, run sensible type conversions.
            # TODO: don't directly read file into memory...

            raise NotImplementedError

        else:
            raise TypeError(f"Unsupported filetype {ftype}")

        self._ftype = ftype
        self._featurizer = None
        self._batch_size = None

    def _add_batchsize(self, batch_size: int):
        """Adds batch size to self."""

        self._batch_size = batch_size

    @property
    def is_fixed(self) -> bool:
        """Private ~ intended for DeepBio internals. """

        if type(self._is_fixed) is bool:
            return self._is_fixed

        first_len = len(self._X[0])
        self._is_fixed = all([len(x) == first_len for x in self._X])
        return self._is_fixed

    def __iter__(self):

        if self._ftype == "tar":

            wd_dataset = self._wd_dataset

            if self._featurizer:
                wd_dataset = wd_dataset.map_tuple(self._featurizer)

            if self._batch_size:
                wd_dataset = wd_dataset.batched(self._batch_size)

            return wd_dataset.__iter__()

        else:

            raise TypeError(f"Unsupported filetype {self._ftype}")

    def __getstate__(self):
        result = dict(self.__dict__)
        result["source"] = None
        return result

    def __repr__(self) -> str:

        return "todo"

    def __unicode__(self) -> str:

        return "todo"
