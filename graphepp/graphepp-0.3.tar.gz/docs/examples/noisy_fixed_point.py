"""Find the fixed point of an EPP with noisy CNOT gates."""

import os, sys

sys.path.insert(0, os.path.abspath(".."))
import graphepp as gg
import numpy as np


# CNOT gate is modelled as local white noise acting on both of the qubits
# followed by the perfect operation
noise_param = 0.98
ghz5_graph = gg.Graph(
    N=5, E=((0, i) for i in range(1, 5)), sets=[(0,), (i for i in range(1, 5))]
)  # 5-qubit GHZ state

print("Noisy fixed point of the P1-P2 protocol for the 5-qubit GHZ state.")
print(
    f"CNOTs are noisy with local depolarizing noise with error parameter p={noise_param:.2f}"
)

rho = np.zeros(2 ** ghz5_graph.N, dtype=np.float)
rho[0] = 1.0  # perfect state

for i in range(
    100
):  # 100 iterations are more than enough to reach the fixed point with numerical precision
    rho = gg.wnoise_all(
        rho=rho, p=noise_param, graph=ghz5_graph
    )  # a noisy CNOT is acting on each of the qubits to perform the protocol
    rho = gg.p1(rho=rho, graph=ghz5_graph)
    rho = gg.wnoise_all(rho=rho, p=noise_param, graph=ghz5_graph)
    rho = gg.p2(rho=rho, graph=ghz5_graph)
    fixed_point_fidelity_p2 = rho[0]  # fidelity when ending with p2
rho = gg.wnoise_all(
    rho=rho, p=noise_param, graph=ghz5_graph
)  # a noisy CNOT is acting on each of the qubits to perform the protocol
rho = gg.p1(rho=rho, graph=ghz5_graph)
fixed_point_fidelity_p1 = rho[0]  # fidelity when ending with p1
print(f"Fixed point fidelity when ending with P1: {fixed_point_fidelity_p1}")
print(f"Fixed point fidelity when ending with P2: {fixed_point_fidelity_p2}")

print("=================")
print("Fixed point fidelity as function of CNOT noise parameter")


def noisy_fixed_point(graph, noise_param):
    rho = np.zeros(2 ** graph.N, dtype=np.float)
    rho[0] = 1.0  # perfect state
    for i in range(
        100
    ):  # 100 iterations are more than enough to reach the fixed point with numerical precision
        rho = gg.wnoise_all(
            rho=rho, p=noise_param, graph=graph
        )  # a noisy CNOT is acting on each of the qubits to perform the protocol
        rho = gg.p1(rho=rho, graph=ghz5_graph)
        rho = gg.wnoise_all(rho=rho, p=noise_param, graph=graph)
        rho = gg.p2(rho=rho, graph=ghz5_graph)
    return rho


ghz5_graph = gg.Graph(
    N=5, E=((0, i) for i in range(1, 5)), sets=[(0,), (i for i in range(1, 5))]
)
noise_list = np.linspace(0.9, 1, num=21)
print("Calculating fidelity list... (this may take a bit)")
fidelity_list = [
    noisy_fixed_point(graph=ghz5_graph, noise_param=p)[0] for p in noise_list
]
print(f"{noise_list=}")
print(f"{fidelity_list=}")
print("One can see that below a certain noise threshold, the EPP stops working.")
print("If pyplot is available, will show a plot.")

try:
    import matplotlib.pyplot as plt

    plotting_possible = True
except ImportError:
    plotting_possible = False

if plotting_possible:
    plt.scatter(noise_list, fidelity_list)
    plt.title("5-qubit GHZ state at EPP fixed point")
    plt.xlabel("Error parameter p for CNOT gates")
    plt.ylabel("Fidelity at fixed point")
    plt.show()
