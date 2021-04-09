import unittest
import numpy as np
import graphepp as gg
from graphepp.graphepp import _mask_a, _mask_b, _mask_k


def random_graph(num_vertices, p=0.5):
    """Generate random gg.Graph.

    Graph with `num_vertices` vertices. Each edge exists with probability `p`.
    """
    edges = []
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if np.random.random() < p:
                edges += [(i, j)]
    return gg.Graph(N=num_vertices, E=edges)


class TestGraph(unittest.TestCase):
    def test_immutableish(self):
        # test that all the properties are read only
        test_graph = gg.Graph(
            N=5, E=[(0, 1), (1, 2), (2, 0), (3, 4)], sets=[[0, 3], [1, 4], [2]]
        )
        with self.assertRaises(AttributeError):
            test_graph.N = 3
        with self.assertRaises(AttributeError):
            test_graph.E = ((1, 2),)
        with self.assertRaises(TypeError):
            E = test_graph.E
            E[0] = (0, 1)
        with self.assertRaises(AttributeError):
            test_graph.sets = ((1, 2), (0, 3))
        with self.assertRaises(TypeError):
            sets = test_graph.sets
            sets[0] = (0, 2, 4)
        with self.assertRaises(AttributeError):
            test_graph.adj = np.array([[0, 1], [1, 0]], dtype=int)
        adj = test_graph.adj
        adj[0, 0] = 1
        adj[1, 0] = 0
        self.assertFalse(np.all(adj == test_graph.adj))

    def test_equivalence(self):
        # test that equivalent graphs are considered equal
        test_graph = gg.Graph(N=5, E=[(0, 1), (0, 2), (2, 3), (3, 4)])
        # other number of vertices
        graph1 = gg.Graph(N=6, E=[(0, 1), (0, 2), (2, 3), (3, 4)])
        self.assertNotEqual(graph1, test_graph)
        self.assertNotEqual(hash(graph1), hash(test_graph))
        # order of nodes in edges
        graph2 = gg.Graph(N=5, E=[(1, 0), (0, 2), (3, 2), (4, 3)])
        self.assertEqual(graph2, test_graph)
        self.assertEqual(hash(graph2), hash(test_graph))
        # order of edges should not matter
        graph3 = gg.Graph(N=5, E=[(0, 1), (3, 4), (0, 2), (2, 3)])
        self.assertEqual(graph3, test_graph)
        self.assertEqual(hash(graph3), hash(test_graph))
        # different sets are not equivalent
        test_graph1 = gg.Graph(
            N=5, E=[(0, 1), (0, 2), (2, 3), (3, 4)], sets=[[0, 3], [1, 2, 4]]
        )
        self.assertNotEqual(test_graph1, test_graph)
        self.assertNotEqual(hash(test_graph1), hash(test_graph))
        graph4 = gg.Graph(
            N=5, E=[(0, 1), (0, 2), (2, 3), (3, 4)], sets=[[0], [1, 2, 4], [3]]
        )
        self.assertNotEqual(graph4, test_graph1)
        self.assertNotEqual(hash(graph4), hash(test_graph1))
        # order within sets should not matter
        graph5 = gg.Graph(
            N=5, E=[(0, 1), (0, 2), (2, 3), (3, 4)], sets=[[3, 0], [1, 4, 2]]
        )
        self.assertEqual(graph5, test_graph1)
        self.assertEqual(hash(graph5), hash(test_graph1))
        # but order of sets matters
        graph6 = gg.Graph(
            N=5, E=[(0, 1), (0, 2), (2, 3), (3, 4)], sets=[[1, 2, 4], [0, 3]]
        )
        self.assertNotEqual(graph6, test_graph1)
        self.assertNotEqual(hash(graph6), hash(test_graph1))


class TestNoise(unittest.TestCase):
    # the gg.noisy function does all the heavy lifting in this part,
    # the rest is basically just written down definitions
    """Tests for all the noise functions."""

    def test_noisy(self):
        # test small case with random numbers
        num_qubits = 2
        test_rho = np.random.random(2 ** num_qubits)
        test_rho = test_rho / np.sum(test_rho)
        test_result = gg.noisy(rho=test_rho, subset=[num_qubits - 1])
        known_result = np.array([test_rho[1], test_rho[0], test_rho[3], test_rho[2]])
        self.assertTrue(np.allclose(test_result, known_result))
        # test all single qubit patterns for an 8 qubit state
        num_qubits = 8
        test_rho = np.random.random(2 ** num_qubits)
        test_rho = test_rho / np.sum(test_rho)
        for qubit_index in range(num_qubits):
            test_result = gg.noisy(rho=test_rho, subset=[qubit_index])
            known_result = np.zeros_like(test_rho)
            binary_mask = 1 << ((num_qubits - 1) - qubit_index)
            for i in range(2 ** num_qubits):
                known_result[i] = test_rho[i ^ binary_mask]
            self.assertTrue(np.allclose(test_result, known_result))
        # test random patterns on states of random size
        for _ in range(256):
            num_qubits = np.random.randint(
                1, 16
            )  # up to 15 qubits shouldn't take too long to test
            test_rho = np.random.random(2 ** num_qubits)
            test_rho = test_rho / np.sum(test_rho)
            amount_choices = np.random.randint(num_qubits)
            chosen_qubits = np.sort(
                np.random.choice(num_qubits, size=amount_choices, replace=False)
            )
            test_result = gg.noisy(rho=test_rho, subset=chosen_qubits)
            binary_string = "0b"
            for i in range(num_qubits):
                if i in chosen_qubits:
                    binary_string += "1"
                else:
                    binary_string += "0"
            binary_mask = int(binary_string, 2)
            known_result = np.zeros_like(test_rho)
            for i in range(2 ** num_qubits):
                known_result[i] = test_rho[i ^ binary_mask]
            self.assertTrue(np.allclose(test_result, known_result))

    def test_znoisy(self):
        # kinda pointless because this is literally just the definition of
        # the function replicated
        num_qubits = 8
        test_rho = np.random.random(2 ** num_qubits)
        test_rho = test_rho / np.sum(test_rho)
        for i in range(num_qubits):
            test_result = gg.znoisy(rho=test_rho, qubit_index=i)
            # test calling with optional graph argument that does nothing
            test_result2 = gg.znoisy(
                rho=test_rho, qubit_index=i, graph=random_graph(num_qubits)
            )
            known_result = gg.noisy(rho=test_rho, subset=[i])
            self.assertTrue(np.allclose(test_result, known_result))
            self.assertTrue(np.allclose(test_result2, known_result))

    def test_xnoisy(self):
        # use an alternative way to do the same thing (but with more unnecessary function calls)
        num_qubits = 8
        test_rho = np.random.random(2 ** num_qubits)
        test_rho = test_rho / np.sum(test_rho)
        for i in range(num_qubits):
            test_graph = random_graph(num_qubits)
            test_result = gg.xnoisy(rho=test_rho, qubit_index=i, graph=test_graph)
            known_result = test_rho
            for j in range(
                num_qubits
            ):  # xnoise is equivalent to znoise on all neighbors
                if test_graph.adj[i, j]:
                    known_result = gg.znoisy(rho=known_result, qubit_index=j)
            self.assertTrue(np.allclose(test_result, known_result))

    def test_ynoisy(self):
        # use an alternative way to do the same thing (but with more unnecessary function calls)
        num_qubits = 8
        test_rho = np.random.random(2 ** num_qubits)
        test_rho = test_rho / np.sum(test_rho)
        for i in range(num_qubits):
            test_graph = random_graph(num_qubits)
            test_result = gg.ynoisy(rho=test_rho, qubit_index=i, graph=test_graph)
            # ynoise is equivalent to znoise on all neighbors AND the qubit itself
            known_result = gg.znoisy(rho=test_rho, qubit_index=i)
            for j in range(num_qubits):
                if test_graph.adj[i, j]:
                    known_result = gg.znoisy(rho=known_result, qubit_index=j)
            self.assertTrue(np.allclose(test_result, known_result))

    def test_znoise(self):
        # only reproducibility test because this function is just a definition
        test_rho = np.array([0.93, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01])
        test_graph = gg.Graph(N=3, E=[(0, 1), (0, 2)])  # GHZ graph
        test_result = gg.znoise(rho=test_rho, qubit_index=1, p=0.98, graph=test_graph)
        self.assertTrue(
            np.allclose(
                test_result,
                np.array([0.9116, 0.01, 0.0284, 0.01, 0.01, 0.01, 0.01, 0.01]),
            )
        )
        # now try different noise on all qubits
        ps = [0.7, 0.93, 0.98]
        test_result = test_rho
        for idx, p in enumerate(ps):
            test_result = gg.znoise(
                rho=test_result, qubit_index=idx, p=p, graph=test_graph
            )
        self.assertTrue(
            np.allclose(
                test_result,
                np.array(
                    [
                        0.5969416,
                        0.0219784,
                        0.0541784,
                        0.0109016,
                        0.2615464,
                        0.0151336,
                        0.0289336,
                        0.0103864,
                    ]
                ),
            )
        )

    def test_xnoise(self):
        # only reproducibility test because this function is just a definition
        test_rho = np.array([0.93, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01])
        test_graph = gg.Graph(N=3, E=[(0, 1), (0, 2)])  # GHZ graph
        test_result = gg.xnoise(rho=test_rho, qubit_index=1, p=0.98, graph=test_graph)
        self.assertTrue(
            np.allclose(
                test_result,
                np.array([0.9116, 0.01, 0.01, 0.01, 0.0284, 0.01, 0.01, 0.01]),
            )
        )
        # now try different noise on all qubits
        ps = [0.7, 0.93, 0.98]
        test_result = test_rho
        for idx, p in enumerate(ps):
            test_result = gg.xnoise(
                rho=test_result, qubit_index=idx, p=p, graph=test_graph
            )
        self.assertTrue(
            np.allclose(
                test_result,
                np.array(
                    [0.5978432, 0.01, 0.01, 0.2619328, 0.0661568, 0.01, 0.01, 0.0340672]
                ),
            )
        )

    def test_ynoise(self):
        # only reproducibility test because this function is just a definition
        test_rho = np.array([0.93, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01])
        test_graph = gg.Graph(N=3, E=[(0, 1), (0, 2)])  # GHZ graph
        test_result = gg.ynoise(rho=test_rho, qubit_index=1, p=0.98, graph=test_graph)
        self.assertTrue(
            np.allclose(
                test_result,
                np.array([0.9116, 0.01, 0.01, 0.01, 0.01, 0.01, 0.0284, 0.01]),
            )
        )
        # now try different noise on all qubits
        ps = [0.7, 0.93, 0.98]
        test_result = test_rho
        for idx, p in enumerate(ps):
            test_result = gg.ynoise(
                rho=test_result, qubit_index=idx, p=p, graph=test_graph
            )
        self.assertTrue(
            np.allclose(
                test_result,
                np.array(
                    [
                        0.5969416,
                        0.0289336,
                        0.0151336,
                        0.0109016,
                        0.0103864,
                        0.0219784,
                        0.0541784,
                        0.2615464,
                    ]
                ),
            )
        )

    def test_wnoise(self):
        # only reproducibility test because this function is just a definition
        test_rho = np.array([0.93, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01])
        test_graph = gg.Graph(N=3, E=[(0, 1), (0, 2)])  # GHZ graph
        test_result = gg.wnoise(rho=test_rho, qubit_index=1, p=0.98, graph=test_graph)
        self.assertTrue(
            np.allclose(
                test_result,
                np.array([0.9162, 0.01, 0.0146, 0.01, 0.0146, 0.01, 0.0146, 0.01]),
            )
        )
        # now try different noise on all qubits
        ps = [0.7, 0.93, 0.98]
        test_result = test_rho
        for idx, p in enumerate(ps):
            test_result = gg.wnoise(
                rho=test_result, qubit_index=idx, p=p, graph=test_graph
            )
        self.assertTrue(
            np.allclose(
                test_result,
                np.array(
                    [
                        0.6770368,
                        0.016164,
                        0.024214,
                        0.076056,
                        0.0900952,
                        0.016164,
                        0.024214,
                        0.076056,
                    ]
                ),
            )
        )

    def test_noise_pattern(self):
        # first compare to other functions
        test_rho = np.random.random(16)
        test_rho[0] += 16
        test_rho = test_rho / np.sum(test_rho)
        test_graph = random_graph(num_vertices=4, p=0.9)
        px = 0.5 + np.random.random() * 0.5
        known_result = gg.xnoise(rho=test_rho, qubit_index=2, p=px, graph=test_graph)
        test_result = gg.noise_pattern(
            rho=test_rho, qubit_index=2, ps=[px, 1 - px, 0, 0], graph=test_graph
        )
        self.assertTrue(np.allclose(test_result, known_result))
        py = 0.5 + np.random.random() * 0.5
        known_result = gg.ynoise(rho=test_rho, qubit_index=2, p=py, graph=test_graph)
        test_result = gg.noise_pattern(
            rho=test_rho, qubit_index=2, ps=[py, 0, 1 - py, 0], graph=test_graph
        )
        self.assertTrue(np.allclose(test_result, known_result))
        pz = 0.5 + np.random.random() * 0.5
        known_result = gg.znoise(rho=test_rho, qubit_index=2, p=pz, graph=test_graph)
        test_result = gg.noise_pattern(
            rho=test_rho, qubit_index=2, ps=[pz, 0, 0, 1 - pz], graph=test_graph
        )
        self.assertTrue(np.allclose(test_result, known_result))
        pw = 0.5 + np.random.random() * 0.5
        known_result = gg.wnoise(rho=test_rho, qubit_index=2, p=pw, graph=test_graph)
        test_result = gg.noise_pattern(
            rho=test_rho,
            qubit_index=2,
            ps=[pw + (1 - pw) / 4, (1 - pw) / 4, (1 - pw) / 4, (1 - pw) / 4],
            graph=test_graph,
        )
        self.assertTrue(np.allclose(test_result, known_result))
        # and reproducibility
        test_rho = np.array(
            [
                0.85,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
            ]
        )
        test_graph = gg.Graph(N=4, E=[(0, 1), (1, 2), (2, 3), (3, 0)])
        ps = [0.8, 0.1, 0.07, 0.03]
        test_result = gg.noise_pattern(
            rho=test_rho, qubit_index=2, ps=ps, graph=test_graph
        )
        self.assertTrue(
            np.allclose(
                test_result,
                np.array(
                    [
                        0.682,
                        0.01,
                        0.0352,
                        0.01,
                        0.01,
                        0.094,
                        0.01,
                        0.0688,
                        0.01,
                        0.01,
                        0.01,
                        0.01,
                        0.01,
                        0.01,
                        0.01,
                        0.01,
                    ]
                ),
            )
        )

    def test_wnoise_all(self):
        # again, this function is just writing down a definition
        test_rho = np.array([0.93, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01])
        test_graph = gg.Graph(N=3, E=[(0, 1), (0, 2)])  # GHZ graph
        p = 0.98
        test_result = gg.wnoise_all(rho=test_rho, p=p, graph=test_graph)
        self.assertTrue(
            np.allclose(
                test_result,
                np.array(
                    [
                        0.88928632,
                        0.014554,
                        0.014554,
                        0.014554,
                        0.02338968,
                        0.014554,
                        0.014554,
                        0.014554,
                    ]
                ),
            )
        )

    def test_noise_global(self):
        # again, this function is just following the definition
        test_rho = np.array([0.91, 0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.02])
        test_graph = gg.Graph(N=3, E=[(0, 1), (0, 2)])  # GHZ graph
        p = 0.98
        test_result = gg.noise_global(rho=test_rho, p=p, graph=test_graph)
        self.assertTrue(
            np.allclose(
                test_result,
                np.array(
                    [0.8943, 0.0221, 0.0123, 0.0123, 0.0123, 0.0123, 0.0123, 0.0221]
                ),
            )
        )


class TestDistanceMeasures(unittest.TestCase):
    def _distance_measure_criterium(self, func):
        num_qubits = 5
        rho = np.random.random(2 ** num_qubits)
        rho = rho / np.sum(rho)
        # distance measure is 0 for same state
        self.assertAlmostEqual(func(rho, rho), 0)
        # distance measure is > 0 for different states
        sigma = np.random.random(2 ** num_qubits)
        sigma = sigma / np.sum(sigma)
        self.assertGreater(func(rho, sigma), 0)

    def test_fidelity(self):
        def dist_meas(rho, mu):
            return np.sqrt(np.abs(1 - gg.fidelity(rho, mu)))

        self._distance_measure_criterium(dist_meas)

        def dist_meas_2(rho, mu):
            return 1 - np.sqrt(gg.fidelity(rho, mu))

        self._distance_measure_criterium(dist_meas_2)
        # now a reproducibility test
        test_rho = np.array(
            [
                0.85,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
            ]
        )
        test_mu = np.array(
            [
                0.70,
                0.01,
                0.02,
                0.00,
                0.00,
                0.02,
                0.00,
                0.01,
                0.00,
                0.05,
                0.00,
                0.04,
                0.14,
                0.01,
                0.00,
                0.00,
            ]
        )
        self.assertAlmostEqual(gg.fidelity(test_rho, test_mu), 0.8270519315962255)

    def test_fid_alternative(self):
        def dist_meas(rho, mu):
            return np.sqrt(np.abs(1 - gg.fid_alternative(rho, mu) ** 2))

        self._distance_measure_criterium(dist_meas)

        def dist_meas_2(rho, mu):
            return 1 - gg.fid_alternative(rho, mu)

        self._distance_measure_criterium(dist_meas_2)
        test_rho = np.array(
            [
                0.85,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
            ]
        )
        test_mu = np.array(
            [
                0.70,
                0.01,
                0.02,
                0.00,
                0.00,
                0.02,
                0.00,
                0.01,
                0.00,
                0.05,
                0.00,
                0.04,
                0.14,
                0.01,
                0.00,
                0.00,
            ]
        )
        self.assertAlmostEqual(
            gg.fid_alternative(test_rho, test_mu), 0.9094239559172749
        )

    def test_trace_distance(self):
        self._distance_measure_criterium(gg.trace_distance)
        test_rho = np.array(
            [
                0.85,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
            ]
        )
        test_mu = np.array(
            [
                0.70,
                0.01,
                0.02,
                0.00,
                0.00,
                0.02,
                0.00,
                0.01,
                0.00,
                0.05,
                0.00,
                0.04,
                0.14,
                0.01,
                0.00,
                0.00,
            ]
        )
        self.assertAlmostEqual(gg.trace_distance(test_rho, test_mu), 0.22)

    def test_consistency(self):
        num_qubits = 5
        rho = np.random.random(2 ** num_qubits)
        rho = rho / np.sum(rho)
        sigma = np.random.random(2 ** num_qubits)
        sigma = sigma / np.sum(sigma)
        # assert relationship between fidelity and fid_alternative
        self.assertAlmostEqual(
            gg.fidelity(rho, sigma), gg.fid_alternative(rho, sigma) ** 2
        )
        # assert that the relation holds 1-sqrt(F) <= trace_distance <= sqrt(1-F)
        self.assertLessEqual(
            1 - np.sqrt(gg.fidelity(rho, sigma)), gg.trace_distance(rho, sigma)
        )
        self.assertLessEqual(
            gg.trace_distance(rho, sigma), np.sqrt(np.abs(1 - gg.fidelity(rho, sigma)))
        )


class TestAuxiliaryFunctions(unittest.TestCase):
    def test_normalize(self):
        num_qubits = 5
        rho = np.random.random(2 ** num_qubits)
        self.assertAlmostEqual(np.sum(gg.normalize(rho)), 1)
        # assert catching of numerical phenomena (usually happens when subtracting similar states)
        rho[0] = -1e-16
        rho[2] = -2.4e-15
        self.assertTrue(np.all(gg.normalize(rho) >= 0))
        # should never be called with large negative numbers, but make sure that norm is 1 anyway
        rho[2] = -2.4e-5
        self.assertAlmostEqual(np.sum(gg.normalize(rho)), 1)

    def test_local_complementation(self):
        # first test with known examples
        test_graph = gg.Graph(N=3, E=[(0, 1), (0, 2)])
        test_result = gg.local_complementation(n=0, graph=test_graph)
        known_result = gg.Graph(N=3, E=[(0, 1), (0, 2), (1, 2)])
        self.assertEqual(test_result, known_result)
        test_graph = gg.Graph(
            N=6, E=[(0, 1), (1, 2), (0, 3), (1, 4), (2, 5), (3, 4), (4, 5)]
        )  # butterfly graph
        test_result = gg.local_complementation(n=1, graph=test_graph)
        known_result = gg.Graph(
            N=6,
            E=[
                (0, 1),
                (1, 2),
                (0, 3),
                (1, 4),
                (2, 5),
                (3, 4),
                (4, 5),
                (0, 4),
                (2, 4),
                (0, 2),
            ],
        )
        self.assertEqual(test_result, known_result)
        # test with random graphs and stupid verification function
        for _ in range(10):
            num_vertices = 10
            test_graph = random_graph(num_vertices)
            for lc_vertex in range(num_vertices):  # try all possible complementations
                complemented_graph = gg.local_complementation(
                    n=lc_vertex, graph=test_graph
                )
                # now do the verification
                for i in range(num_vertices):
                    for j in range(i + 1, num_vertices):
                        if (
                            test_graph.adj[j, lc_vertex]
                            and test_graph.adj[i, lc_vertex]
                        ):  # i and j are both in the neighborhood of lc_vertex
                            self.assertEqual(
                                complemented_graph.adj[i, j],
                                (test_graph.adj[i, j] + 1) % 2,
                            )
                        else:
                            self.assertEqual(
                                complemented_graph.adj[i, j], test_graph.adj[i, j]
                            )


class TestTwoColorableEPP(unittest.TestCase):
    def test_mask_a(self):
        for _ in range(10):
            num_vertices = 10
            test_graph = random_graph(num_vertices)
            # randomly split in two sets - actual colorability doesn't matter for this test
            first_set = sorted(
                np.random.choice(
                    np.arange(num_vertices, dtype=int),
                    size=np.random.randint(num_vertices),
                    replace=False,
                )
            )
            second_set = [i for i in range(num_vertices) if i not in first_set]
            test_graph = gg.Graph(
                N=test_graph.N, E=test_graph.E, sets=[first_set, second_set]
            )
            for short_bit_string in range(2 ** len(test_graph.a)):
                long_bit_string = _mask_a(j=short_bit_string, graph=test_graph)
                short_string = format(
                    short_bit_string, "0" + str(len(test_graph.a)) + "b"
                )
                long_string = format(long_bit_string, "0" + str(test_graph.N) + "b")
                for bit, idx in zip(short_string, test_graph.a):
                    self.assertEqual(bit, long_string[idx])

    def test_mask_b(self):
        for _ in range(10):
            num_vertices = 10
            test_graph = random_graph(num_vertices)
            # randomly split in two sets - actual colorability doesn't matter for this test
            first_set = sorted(
                np.random.choice(
                    np.arange(num_vertices, dtype=int),
                    size=np.random.randint(num_vertices),
                    replace=False,
                )
            )
            second_set = [i for i in range(num_vertices) if i not in first_set]
            test_graph = gg.Graph(
                N=test_graph.N, E=test_graph.E, sets=[first_set, second_set]
            )
            for short_bit_string in range(2 ** len(test_graph.b)):
                long_bit_string = _mask_b(j=short_bit_string, graph=test_graph)
                short_string = format(
                    short_bit_string, "0" + str(len(test_graph.b)) + "b"
                )
                long_string = format(long_bit_string, "0" + str(test_graph.N) + "b")
                for bit, idx in zip(short_string, test_graph.b):
                    self.assertEqual(bit, long_string[idx])

    def test_p1(self):
        # only reproducibility tests for now - an alternative implementation with density matrices would be ideal
        test_graph = gg.Graph(
            N=4, E=((0, 1), (0, 2), (0, 3)), sets=[[0], [1, 2, 3]]
        )  # 4 qubit GHZ graph; two-colorable
        test_rho = np.array(
            [
                0.70,
                0.01,
                0.02,
                0.00,
                0.00,
                0.02,
                0.00,
                0.01,
                0.00,
                0.05,
                0.00,
                0.04,
                0.14,
                0.01,
                0.00,
                0.00,
            ]
        )
        test_result = gg.p1(rho=test_rho, graph=test_graph)
        self.assertTrue(
            np.allclose(
                test_result,
                np.array(
                    [
                        7.72984887e-01,
                        2.20403023e-02,
                        4.47103275e-02,
                        6.29722922e-04,
                        6.29722922e-04,
                        4.47103275e-02,
                        3.14861461e-04,
                        2.32997481e-02,
                        3.74685139e-02,
                        4.40806045e-03,
                        6.29722922e-03,
                        0.00000000e00,
                        1.57430730e-03,
                        2.20403023e-02,
                        1.25944584e-03,
                        1.76322418e-02,
                    ]
                ),
            )
        )
        test_graph = gg.Graph(
            N=5, E=((0, 1), (1, 2), (2, 3), (3, 4)), sets=[[0, 2, 4], [1, 3]]
        )  # 5 qubit linear cluster state
        test_rho = np.zeros(2 ** 5, dtype=np.float)
        test_rho[0] = 1.0
        test_rho = gg.wnoise_all(rho=test_rho, p=0.99, graph=test_graph)
        test_result = gg.p1(rho=test_rho, graph=test_graph)
        self.assertTrue(
            np.allclose(
                test_result,
                np.array(
                    [
                        9.75112509e-01,
                        1.25003027e-05,
                        9.87411374e-03,
                        1.25003027e-05,
                        1.25028117e-05,
                        1.25003027e-05,
                        3.76852011e-07,
                        1.25003027e-05,
                        9.87411374e-03,
                        2.51861704e-07,
                        5.01148266e-03,
                        2.51861704e-07,
                        3.76852011e-07,
                        2.51861704e-07,
                        1.25021931e-05,
                        2.51861704e-07,
                        1.25003027e-05,
                        6.43999920e-10,
                        2.51861704e-07,
                        6.43999920e-10,
                        1.25003027e-05,
                        6.43999920e-10,
                        2.51861704e-07,
                        6.43999920e-10,
                        1.25003027e-05,
                        6.43999920e-10,
                        2.51861704e-07,
                        6.43999920e-10,
                        1.25003027e-05,
                        6.43999920e-10,
                        2.51861704e-07,
                        6.43999920e-10,
                    ]
                ),
            )
        )

    def test_p2(self):
        test_graph = gg.Graph(
            N=4, E=((0, 1), (0, 2), (0, 3)), sets=[[0], [1, 2, 3]]
        )  # 4 qubit GHZ graph; two-colorable
        test_rho = np.array(
            [
                0.70,
                0.01,
                0.02,
                0.00,
                0.00,
                0.02,
                0.00,
                0.01,
                0.00,
                0.05,
                0.00,
                0.04,
                0.14,
                0.01,
                0.00,
                0.00,
            ]
        )
        test_result = gg.p2(rho=test_rho, graph=test_graph)
        self.assertTrue(
            np.allclose(
                test_result,
                np.array(
                    [
                        9.49244479e-01,
                        5.03680744e-03,
                        7.74893452e-04,
                        3.09957381e-03,
                        3.79697792e-02,
                        9.68616815e-04,
                        0.00000000e00,
                        1.93723363e-04,
                        0.00000000e00,
                        1.93723363e-03,
                        0.00000000e00,
                        0.00000000e00,
                        0.00000000e00,
                        7.74893452e-04,
                        0.00000000e00,
                        0.00000000e00,
                    ]
                ),
            )
        )
        test_graph = gg.Graph(
            N=5, E=((0, 1), (1, 2), (2, 3), (3, 4)), sets=[[0, 2, 4], [1, 3]]
        )  # 5 qubit linear cluster state
        test_rho = np.zeros(2 ** 5, dtype=np.float)
        test_rho[0] = 1.0
        test_rho = gg.wnoise_all(rho=test_rho, p=0.99, graph=test_graph)
        test_result = gg.p2(rho=test_rho, graph=test_graph)
        self.assertTrue(
            np.allclose(
                test_result,
                np.array(
                    [
                        9.74888853e-01,
                        4.94873525e-03,
                        3.73657691e-05,
                        2.51192019e-05,
                        4.98572109e-03,
                        4.94873525e-03,
                        1.28738842e-05,
                        2.51192019e-05,
                        3.73657691e-05,
                        3.79924263e-07,
                        1.25002804e-05,
                        2.53094747e-07,
                        1.28738842e-05,
                        3.79924263e-07,
                        1.24996619e-05,
                        2.53094747e-07,
                        4.94873525e-03,
                        5.01102580e-05,
                        3.79924263e-07,
                        3.79299534e-07,
                        4.94873525e-03,
                        5.01102580e-05,
                        3.79924263e-07,
                        3.79299534e-07,
                        2.51192019e-05,
                        3.79299534e-07,
                        2.53094747e-07,
                        1.29395220e-07,
                        2.51192019e-05,
                        3.79299534e-07,
                        2.53094747e-07,
                        1.29395220e-07,
                    ]
                ),
            )
        )

    def test_p1_var(self):
        # assert that calling it with rho=sigma is equivalent to p1
        test_graph = gg.Graph(
            N=4, E=((0, 1), (0, 2), (0, 3)), sets=[[0], [1, 2, 3]]
        )  # 4 qubit GHZ graph; two-colorable
        test_rho = np.random.random(2 ** 4)
        test_rho = test_rho / np.sum(test_rho)
        test_result1 = gg.p1(rho=test_rho, graph=test_graph)
        test_result2 = gg.p1_var(rho=test_rho, sigma=test_rho, graph=test_graph)
        self.assertTrue(np.allclose(test_result1, test_result2))
        # also small reproducibility test
        test_rho = np.array(
            [
                0.70,
                0.01,
                0.02,
                0.00,
                0.00,
                0.02,
                0.00,
                0.01,
                0.00,
                0.05,
                0.00,
                0.04,
                0.14,
                0.01,
                0.00,
                0.00,
            ]
        )
        test_sigma = np.array(
            [
                0.84,
                0.01,
                0.00,
                0.01,
                0.00,
                0.02,
                0.00,
                0.01,
                0.00,
                0.00,
                0.05,
                0.02,
                0.03,
                0.01,
                0.00,
                0.00,
            ]
        )
        test_result = gg.p1_var(rho=test_rho, sigma=test_sigma, graph=test_graph)
        self.assertTrue(
            np.allclose(
                test_result,
                np.array(
                    [
                        8.37507114e-01,
                        2.21969266e-02,
                        2.46158224e-02,
                        1.02447353e-02,
                        7.11439954e-04,
                        4.41092772e-02,
                        5.69151964e-04,
                        2.24815026e-02,
                        7.25668754e-03,
                        5.26465566e-03,
                        1.42287991e-03,
                        3.55719977e-03,
                        7.11439954e-04,
                        2.13431986e-03,
                        1.08138873e-02,
                        6.40295959e-03,
                    ]
                ),
            )
        )

    def test_p2_var(self):
        # assert that calling it with rho=sigma is equivalent to p2
        test_graph = gg.Graph(
            N=4, E=((0, 1), (0, 2), (0, 3)), sets=[[0], [1, 2, 3]]
        )  # 4 qubit GHZ graph; two-colorable
        test_rho = np.random.random(2 ** 4)
        test_rho = test_rho / np.sum(test_rho)
        test_result1 = gg.p2(rho=test_rho, graph=test_graph)
        test_result2 = gg.p2_var(rho=test_rho, sigma=test_rho, graph=test_graph)
        self.assertTrue(np.allclose(test_result1, test_result2))
        # also small reproducibility test
        test_rho = np.array(
            [
                0.70,
                0.01,
                0.02,
                0.00,
                0.00,
                0.02,
                0.00,
                0.01,
                0.00,
                0.05,
                0.00,
                0.04,
                0.14,
                0.01,
                0.00,
                0.00,
            ]
        )
        test_sigma = np.array(
            [
                0.84,
                0.01,
                0.00,
                0.01,
                0.00,
                0.02,
                0.00,
                0.01,
                0.00,
                0.00,
                0.05,
                0.02,
                0.03,
                0.01,
                0.00,
                0.00,
            ]
        )
        test_result = gg.p2_var(rho=test_rho, sigma=test_sigma, graph=test_graph)
        self.assertTrue(
            np.allclose(
                test_result,
                np.array(
                    [
                        9.86577181e-01,
                        1.67785235e-04,
                        0.00000000e00,
                        1.34228188e-03,
                        7.04697987e-03,
                        8.38926174e-04,
                        0.00000000e00,
                        1.67785235e-04,
                        0.00000000e00,
                        8.38926174e-04,
                        1.67785235e-03,
                        6.71140940e-04,
                        0.00000000e00,
                        6.71140940e-04,
                        0.00000000e00,
                        0.00000000e00,
                    ]
                ),
            )
        )


class TestArbitraryGraphEPP(unittest.TestCase):
    def test_mask_k(self):
        for _ in range(10):
            num_vertices = 10
            test_graph = random_graph(num_vertices)
            # randomly pick a subset - actual colorability doesn't matter for this test
            random_set = tuple(
                sorted(
                    np.random.choice(
                        np.arange(num_vertices, dtype=int),
                        size=np.random.randint(num_vertices),
                        replace=False,
                    )
                )
            )
            for short_bit_string in range(2 ** len(random_set)):
                long_bit_string = _mask_k(
                    j=short_bit_string, graph=test_graph, subset=random_set
                )
                short_string = format(
                    short_bit_string, "0" + str(len(random_set)) + "b"
                )
                long_string = format(long_bit_string, "0" + str(test_graph.N) + "b")
                for bit, idx in zip(short_string, random_set):
                    self.assertEqual(bit, long_string[idx])

    def test_pk(self):
        # assert that for a two-colorables state with graph1 == graph2 and
        # appropriate subset, this is equivalent to p1_var or p2_var
        test_graph = gg.Graph(
            N=4, E=((0, 1), (0, 2), (0, 3)), sets=[[0], [1, 2, 3]]
        )  # 4 qubit GHZ graph; two-colorable
        for _ in range(10):
            test_rho = np.random.random(2 ** 4)
            test_rho = test_rho / np.sum(test_rho)
            test_sigma = np.random.random(2 ** 4)
            test_sigma = test_sigma / np.sum(test_sigma)
            test_result1 = gg.pk(
                rho=test_rho,
                sigma=test_sigma,
                graph1=test_graph,
                graph2=test_graph,
                subset=test_graph.a,
            )
            test_result2 = gg.pk(
                rho=test_rho,
                sigma=test_sigma,
                graph1=test_graph,
                graph2=test_graph,
                subset=test_graph.b,
            )
            known_result1 = gg.p1_var(rho=test_rho, sigma=test_sigma, graph=test_graph)
            known_result2 = gg.p2_var(rho=test_rho, sigma=test_sigma, graph=test_graph)
            self.assertTrue(np.allclose(test_result1, known_result1))
            self.assertTrue(np.allclose(test_result2, known_result2))
        # small reproducibility test
        test_graph = gg.Graph(
            N=4, E=((0, 1), (1, 2), (2, 0), (2, 3)), sets=[[0, 3], [1], [2]]
        )  # small graph that is actually not two-colorable, we choose a coloring with 3 colors
        subgraph0 = gg.Graph(N=4, E=((0, 1), (2, 0), (2, 3)), sets=[[0, 3], [1, 2]])
        subgraph1 = gg.Graph(N=4, E=((0, 1), (1, 2)), sets=[[1], [0, 2, 3]])
        subgraph2 = gg.Graph(N=4, E=((1, 2), (2, 0), (2, 3)), sets=[[2], [0, 1, 3]])
        test_rho = np.array(
            [
                0.70,
                0.01,
                0.02,
                0.00,
                0.00,
                0.02,
                0.00,
                0.01,
                0.00,
                0.05,
                0.00,
                0.04,
                0.14,
                0.01,
                0.00,
                0.00,
            ]
        )
        test_sigma = np.array(
            [
                0.84,
                0.01,
                0.00,
                0.01,
                0.00,
                0.02,
                0.00,
                0.01,
                0.00,
                0.00,
                0.05,
                0.02,
                0.03,
                0.01,
                0.00,
                0.00,
            ]
        )
        test_result0 = gg.pk(
            rho=test_rho,
            sigma=test_sigma,
            graph1=test_graph,
            graph2=subgraph0,
            subset=test_graph.sets[0],
        )
        self.assertTrue(
            np.allclose(
                test_result0,
                np.array(
                    [
                        9.46859903e-01,
                        9.66183575e-04,
                        2.70531401e-02,
                        8.05152979e-04,
                        0.00000000e00,
                        8.05152979e-04,
                        0.00000000e00,
                        6.44122383e-04,
                        6.76328502e-03,
                        1.44927536e-03,
                        0.00000000e00,
                        1.61030596e-03,
                        0.00000000e00,
                        8.05152979e-04,
                        1.12721417e-02,
                        9.66183575e-04,
                    ]
                ),
            )
        )
        test_result1 = gg.pk(
            rho=test_rho,
            sigma=test_sigma,
            graph1=test_graph,
            graph2=subgraph1,
            subset=test_graph.sets[1],
        )
        self.assertTrue(
            np.allclose(
                test_result1,
                np.array(
                    [
                        7.59674923e-01,
                        2.27038184e-02,
                        2.30908153e-02,
                        1.25128999e-02,
                        6.19195046e-03,
                        2.19298246e-03,
                        5.15995872e-04,
                        0.00000000e00,
                        2.45098039e-03,
                        5.46955624e-02,
                        4.65686275e-02,
                        6.20485036e-02,
                        5.15995872e-04,
                        4.38596491e-03,
                        2.57997936e-04,
                        2.19298246e-03,
                    ]
                ),
            )
        )
        test_result2 = gg.pk(
            rho=test_rho,
            sigma=test_sigma,
            graph1=test_graph,
            graph2=subgraph2,
            subset=test_graph.sets[2],
        )
        self.assertTrue(
            np.allclose(
                test_result2,
                np.array(
                    [
                        6.95285011e-01,
                        2.00562984e-02,
                        1.05559465e-03,
                        2.58034248e-03,
                        1.05559465e-03,
                        3.78841192e-02,
                        1.17288295e-04,
                        2.34576589e-04,
                        1.05559465e-03,
                        5.32488858e-02,
                        1.64203612e-03,
                        4.69153179e-04,
                        1.63969036e-01,
                        2.00562984e-02,
                        7.03729768e-04,
                        5.86441473e-04,
                    ]
                ),
            )
        )


if __name__ == "__main__":
    unittest.main()
