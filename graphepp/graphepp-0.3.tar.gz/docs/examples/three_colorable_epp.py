"""Perform the entanglement purification protocol for arbitrary graph states.

Here we look at an example for a 6-qubit graph state that is three-colorable.
"""

import os, sys

sys.path.insert(0, os.path.abspath(".."))
import graphepp as gg
import numpy as np

# as main graph we use this 6-qubit state that is linked to a
# universal quantum error correction code
# For visualization of this particular coloring and the auxiliary graphs
# see Fig.9 and Fig. 20 in https://arxiv.org/abs/1609.05754
main_graph = gg.Graph(
    N=6,
    E=[(0, 1), (0, 4), (0, 5), (1, 2), (1, 3), (2, 3), (2, 5), (3, 4), (4, 5)],
    sets=[[0, 2], [1, 4], [3, 5]],
)
aux_graph1 = gg.Graph(N=6, E=[(0, 1), (0, 4), (0, 5), (1, 2), (2, 3), (2, 5)])
aux_graph2 = gg.Graph(N=6, E=[(0, 1), (0, 4), (1, 2), (1, 3), (3, 4), (4, 5)])
aux_graph3 = gg.Graph(N=6, E=[(0, 5), (1, 3), (2, 3), (2, 5), (3, 4), (4, 5)])

# assume we have all these states available, with the same noise per qubit
rho = np.zeros(2 ** main_graph.N, dtype=np.float)
rho[0] = 1.0  # perfect graph state
rho = gg.wnoise_all(rho=rho, p=0.98, graph=main_graph)

mu1 = np.zeros(2 ** aux_graph1.N, dtype=np.float)
mu1[0] = 1.0
mu1 = gg.wnoise_all(rho=mu1, p=0.98, graph=aux_graph1)

mu2 = np.zeros(2 ** aux_graph2.N, dtype=np.float)
mu2[0] = 1.0
mu2 = gg.wnoise_all(rho=mu2, p=0.98, graph=aux_graph2)

mu3 = np.zeros(2 ** aux_graph3.N, dtype=np.float)
mu3[0] = 1.0
mu3 = gg.wnoise_all(rho=mu3, p=0.98, graph=aux_graph3)

# do one protocol for each color, here we assume perfect CNOTs
print(f"Fidelity before: {rho[0]}")
rho = gg.pk(
    rho=rho, sigma=mu1, graph1=main_graph, graph2=aux_graph1, subset=main_graph.sets[0]
)
print(f"Fidelity after first subprotocol: {rho[0]:.5f}")
rho = gg.pk(
    rho=rho, sigma=mu2, graph1=main_graph, graph2=aux_graph2, subset=main_graph.sets[1]
)
print(f"Fidelity after second subprotocol: {rho[0]:.5f}")
rho = gg.pk(
    rho=rho, sigma=mu3, graph1=main_graph, graph2=aux_graph3, subset=main_graph.sets[2]
)
print(f"Fidelity after third subprotocol: {rho[0]:.5f}")
