from typing import List

import pandas as pd
import numpy as np


class DeformationMap:
    def __init__(self, file_path: str, data_cols: List[int]):
        data = pd.read_csv(file_path, skiprows=1, usecols=data_cols).to_numpy()

        self.x = data[:, 0]
        self.y = data[:, 1]
        self.x_displacement = data[:, 2]
        self.y_displacement = data[:, 3]

        binning_x = min(abs(np.diff(self.x)))
        binning_y = max(abs(np.diff(self.y)))
        assert binning_x == binning_y
        assert binning_x % 1 == 0
        self.binning = int(binning_x)

        self.x_size = int((self.x.max() - self.x.min()) / self.binning) + 1
        self.y_size = int((self.y.max() - self.y.min()) / self.binning) + 1

        self.x_map = self.map_missing(self.x_displacement)
        self.y_map = self.map_missing(self.y_displacement)

        self.f12, self.f11 = np.gradient(self.x_map, self.binning, self.binning)
        self.f22, self.f21 = np.gradient(self.y_map, self.binning, self.binning)
        self.max_shear = np.sqrt(
            (((self.f11 - self.f22) / 2.) ** 2) + ((self.f12 + self.f21) / 2.) ** 2)
        self.map_shape = np.shape(self.max_shear)

    def map_missing(self, data_col):
        data_map = np.full((self.y_size, self.x_size), np.nan)

        xc = ((self.x - self.x.min()) / self.binning).astype(int)
        yc = ((self.y - self.y.min()) / self.binning).astype(int)

        # Note the reversed x/y coords
        data_map[yc, xc] = data_col

        return data_map


def detect_cutoff(data: np.ndarray, percentage: float):
    """Get the index of the first data point after the maximum which is percentage below the max
    value."""
    max_index = int(np.argmax(data))
    cutoff_value = np.max(data) - np.max(data) * (percentage / 100)
    for index in range(max_index, len(data)):
        if data[index] < cutoff_value:
            return index
    return len(data)


def true_stress(eng_stress: np.ndarray, eng_strain: np.ndarray) -> np.ndarray:
    """Convert engineering stress to True stress."""
    return eng_stress * (1 + eng_strain)


def true_strain(eng_strain: np.ndarray) -> np.ndarray:
    """Convert engineering strain to True strain."""
    return np.log(eng_strain + 1)
