# -*- coding: utf-8 -*-
# Author: TAO Nianze (Augus)
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from .structure import rgb
from matplotlib.colors import (
    ListedColormap,
    BoundaryNorm,
)


c_map = ListedColormap(rgb)
bounds = [
    25,
    50,
    75,
    100,
    125,
    150,
    175,
    200,
    300,
    400
]
norm = BoundaryNorm(
    bounds,
    c_map.N,
    extend='both',
)


def create_colorbar(file_name: str):
    fig, ax = plt.subplots(
        figsize=(10, 1),
    )
    fig.subplots_adjust(
        bottom=0.5,
    )
    fig.colorbar(
        cm.ScalarMappable(
            norm=norm,
            cmap=c_map,
        ),
        cax=ax,
        orientation='horizontal',
        spacing='proportional',
    )
    plt.savefig(
        file_name,
        dpi=200,
    )
    plt.close()
