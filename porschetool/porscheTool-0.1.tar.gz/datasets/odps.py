import math

import torch
import torch.distributed as dist

from odps import ODPS


class OdpsDataset(torch.utils.data.IterableDataset):
    def __init__(self, project, table, partition, access_id, access_key, endpoint=None, mode='divide'):
        super(OdpsDataset).__init__()
        o = ODPS(access_id, access_key, project=project, endpoint=endpoint)
        self.partition = o.get_table(table).get_partition(partition)
        self.mode = mode

        self.size = partition.size

    def __iter__(self):
        wold_size = self.__get_world_size()
        rank = self.__get_rank()
        reader = self.partition.open_reader()

        if self.mode == 'divide':
            part = int(math.ceil(self.size * 1.0 / wold_size))
            start = rank * part
            end = (rank + 1) * part if (rank + 1) * part < self.size else self.size
            return reader[start, end]

        if self.mode == 'hop':
            return reader[rank, self.size, wold_size]

    @staticmethod
    def __get_rank():
        if not dist.is_available():
            return 0

        if not dist.is_initialized():
            return 0

        return dist.get_rank()

    @staticmethod
    def __get_world_size():
        if not dist.is_available():
            return 1

        if not dist.is_initialized():
            return 1

        return dist.get_world_size()
