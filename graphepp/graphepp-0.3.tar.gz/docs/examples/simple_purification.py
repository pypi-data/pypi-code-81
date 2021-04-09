"""Applying the multipartite entanglement purification protocol."""

import os, sys

sys.path.insert(0, os.path.abspath(".."))
import graphepp as gg
import numpy as np

# Example 1: apply P1 and P2 to a noisy GHZ state
print("Example 1: apply P1 and P2 to a noisy GHZ state")

# graph state version of the GHZ state
ghz_graph = gg.Graph(N=3, E=((0, 1), (0, 2)), sets=[[0], [1, 2]])
# the sets indicate the coloring of this two-colorable graph state
# note that vertices are counting from 0...N-1

rho = np.zeros(2 ** ghz_graph.N, dtype=np.float)
rho[0] = 1.0  # this means the state is the perfect graph state
perfect_state = np.copy(rho)
# start with an initally noise state
rho = gg.wnoise_all(rho=rho, p=0.95, graph=ghz_graph)
print(f"Fidelity before: {gg.fidelity(rho, perfect_state):.5f}")
# now apply P1 once then P2 once
rho = gg.p1(rho=rho, graph=ghz_graph)
rho = gg.p2(rho=rho, graph=ghz_graph)
print(f"Fidelity after: {gg.fidelity(rho, perfect_state):.5f}")


# Example 2: Show that a sufficiently high-fidelity state will converge to the
#            the perfect graph state. Here: Linear cluster state of 5 qubits
print("=================")
print("Example 2: Linear cluster state convergence")

linear_cluster_graph = gg.Graph(
    N=5, E=((0, 1), (1, 2), (2, 3), (3, 4)), sets=[[0, 2, 4], [1, 3]]
)
rho = np.zeros(2 ** linear_cluster_graph.N, dtype=np.float)
rho[0] = 1.0  # the perfect graph state
# first consider a slightly noisy state
mu = gg.wnoise_all(rho=rho, p=0.95, graph=linear_cluster_graph)
print("a) Purification works for sufficiently high-fidelity state.")
print(f"Slightly noisy state initial fidelity: {gg.fidelity(mu, rho):.5f}")
# 100 purification steps should be more than enough to get to the fixed point
# within numerical precision
for i in range(100):
    mu = gg.p1(rho=mu, graph=linear_cluster_graph)
    mu = gg.p2(rho=mu, graph=linear_cluster_graph)
# if initial fidelity is high enough this should converge to the perfect state
print(f"Fidelity after 100 purification steps: {gg.fidelity(mu, rho):.5f}")
print("---------")
mu = gg.wnoise_all(rho=rho, p=0.5, graph=linear_cluster_graph)
print("b) Purification fails for initial states that are too noisy.")
print(f"Very noisy state initial fidelity: {gg.fidelity(mu, rho):.5f}")
for i in range(100):
    mu = gg.p1(rho=mu, graph=linear_cluster_graph)
    mu = gg.p2(rho=mu, graph=linear_cluster_graph)
print(f"Fidelity after 100 purification steps: {gg.fidelity(mu, rho):.5f}")

print("=================")
print("Example 3: GHZ Fidelity change during purification")
ghz_graph = gg.Graph(N=3, E=((0, 1), (0, 2)), sets=[[0], [1, 2]])


rho = np.zeros(2 ** ghz_graph.N, dtype=np.float)
rho[0] = 1.0
perfect_state = np.copy(rho)
# start with an initally noise state
rho = gg.wnoise_all(rho=rho, p=0.8, graph=ghz_graph)
fidelities = [gg.fidelity(rho, perfect_state)]
for i in range(7):
    rho = gg.p1(rho=rho, graph=ghz_graph)
    fidelities += [gg.fidelity(rho, perfect_state)]
    rho = gg.p2(rho=rho, graph=ghz_graph)
    fidelities += [gg.fidelity(rho, perfect_state)]
print(f"Fidelity change over 14 purification steps: {fidelities}")
print("If pyplot is available, will show a plot.")

try:
    import matplotlib.pyplot as plt

    plotting_possible = True
except ImportError:
    plotting_possible = False

if plotting_possible:
    plt.scatter(np.arange(len(fidelities)), fidelities)
    plt.ylim(0.6, 1.01)
    plt.xlabel("Purification steps")
    plt.ylabel("Fidelity")
    plt.grid()
    plt.show()
