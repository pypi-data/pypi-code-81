#!/usr/bin/python
import networkx as nx
import squarify
import matplotlib.pyplot as plt
import seaborn as sns
import os

from pandas.core.frame import DataFrame
from typing import List

def save_graph(path_name: str) -> bool:
    if not path_name:
        raise ValueError("Please provide the path_name.")

    plt.savefig(path_name)
    return os.path.exists(path_name)

def plot_treemap(df: DataFrame,
                 ncols: int,
                 region: str,
                 columns: List[str],
                 dimension: tuple = (75, 15),
                 palette: str = 'flare_r',
                 nrows: int = 1,
                 save: bool = False
                 ):
    if not isinstance(df, DataFrame):
        raise TypeError("Please proivde the right dataframe.")

    if not all([ncols, region, columns, dimension]):
        raise ValueError("Please provide the required parameters such as ncols, region, columns, and dimensions.")

    plt.rcParams['figure.figsize'] = dimension
    fig, axs = plt.subplots(ncols=ncols, nrows=nrows)

    for index, ax in enumerate(axs.ravel()):
        organizations, counts = zip(
            *df.query(f"region_name == '{region}'")[columns[index]].value_counts().to_dict().items())
        squarify.plot(sizes=counts,
                      label=organizations,
                      color=sns.color_palette(palette=palette,
                                              n_colors=50
                                              ),
                      text_kwargs={'color': 'white',
                                   'weight': 'bold'},
                      ax=ax
                      )
        title: str = f"{region} news articles: {columns[index]}  Keywords".title()
        ax.set_title(title,
                     fontweight='bold',
                     fontsize=22)

        ax.invert_yaxis()
        ax.axis('off')

    if save:
        file_path: str = f"{title.replace(' ', '_')}.jpg"
        status: bool = save_graph(file_path)
        return {'file': file_path,
                'status': status
                }

def draw_spring_network(nodes: List,
                        edges: List,
                        title: str,
                        scale: int = 18,
                        k: int = 0.29,
                        node_color: str = 'red',
                        node_size: int = 100,
                        figsize: tuple = (25, 12),
                        font_size: int = 12,
                        edge_color: str = "grey",
                        save: bool = False
                        ):

    if not all([nodes, edges, title]):
        raise ValueError("Please provide the following parameters: nodes, edges, and title")

    nx_graph = nx.Graph()
    nx_graph.add_nodes_from(nodes)

    for entity_attr in edges:
        nx_graph.add_edge(entity_attr[0], entity_attr[1], weight=entity_attr[-1])

    pos = nx.spring_layout(nx_graph, scale=scale, k=k)

    plt.rcParams['figure.figsize'] = figsize
    nx.draw_networkx_nodes(nx_graph, pos, node_color=node_color, node_size=node_size)
    nx.draw_networkx_labels(nx_graph, pos, font_size=font_size)
    nx.draw_networkx_edges(nx_graph, pos, edge_color=edge_color)
    plt.axis('off')
    plt.title(title, fontsize=26, fontweight='bold')

    if save:
        file_path: str = f"{title.replace(' ', '_')}.jpg"
        status: bool = save_graph(file_path)
        return {'file': file_path,
                'status': status}
