from graphmanagerlib.Graph import Grapher
import torch
import torch_geometric.data
import networkx as nx
import numpy as np
import random
import pandas as pd


class DataTransformer:

    def from_networkx(self, G):
        """Converts a :obj:`networkx.Graph` or :obj:`networkx.DiGraph` to a
        :class:`torch_geometric.data.Data` instance.

        Args:
            G (networkx.Graph or networkx.DiGraph): A networkx graph.
        """

        G = nx.convert_node_labels_to_integers(G)
        edge_index = torch.tensor(list(G.edges)).t().contiguous()

        data = {}

        for i, (_, feat_dict) in enumerate(G.nodes(data=True)):
            for key, value in feat_dict.items():
                data[key] = [value] if i == 0 else data[key] + [value]

        for i, (_, _, feat_dict) in enumerate(G.edges(data=True)):
            for key, value in feat_dict.items():
                data[key] = [value] if i == 0 else data[key] + [value]

        for key, item in data.items():
            try:
                data[key] = torch.tensor(item)
            except ValueError:
                pass

        data['edge_index'] = edge_index.view(2, -1)
        data = torch_geometric.data.Data.from_dict(data)

        data.num_nodes = G.number_of_nodes()
        return data

    def get_data(self, documents, tags):
        files = documents.copy()
        random.shuffle(files)

        dfTotal = []
        list_of_graphs = []
        dfEdgesTotal = [[]]


        for document in files:
            connect = Grapher(document)
            G, _, df = connect.graph_formation()
            df = connect.relative_distance(image_width=700, image_height=850)
            individual_data = self.from_networkx(G)

            for col in df.columns:
                try:
                    df[col] = df[col].str.strip()
                except AttributeError:
                    pass


            print(f'{document.index} ---> Success',flush=True)
            dfTotal.append(df)
            edges = individual_data.edge_index
            transposed = np.transpose(edges)
            npArrayTransposed = np.array(transposed)
            if (len(dfEdgesTotal[0]) == 0):
                dfEdgesTotal = npArrayTransposed
            else:
                dfEdgesTotal = np.concatenate((dfEdgesTotal, npArrayTransposed))
            list_of_graphs.append(individual_data)

        nodes = pd.concat(dfTotal)
        edges = pd.DataFrame(dfEdgesTotal, columns=['source', 'target'])

        return nodes, edges,tags
