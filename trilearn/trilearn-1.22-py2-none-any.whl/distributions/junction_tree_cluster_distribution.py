import numpy as np
import trilearn.graph.junction_tree as jtlib

def edge_prob(edge, prob_matrix):
    
    sep = edge[0] & edge[1]
    sepmat = np.triu(prob_matrix[np.ix_(list(sep), list(sep))])
    #node1_mat = np.triu(prob_matrix[np.ix_(list(edge[0]), list(edge[0]))])
    #node2_mat = np.triu(prob_matrix[np.ix_(list(edge[1]), list(edge[1]))])

    non_sep_mat = np.triu(prob_matrix[np.ix_(list(edge[0] - sep), list(edge[1] - sep))])

    #return node1_mat.sum() + node2_mat.sum() + (1-non_sep_mat).sum() #+ sepmat.sum()
    return (1-non_sep_mat).sum() #+ sepmat.sum()


def unnorm_prob(tree, prob_matrix):
    """
    Define the probability of the tree ar ste sum of the edge probabilities.
    The probability of an edge (a, b) is deined as
    sum(prob_matrix[a,a]) + sum(prob_matrix[b,b]) + sum(prob_matrix[s,s]) + sum(prob_matrix[a-s,b-s])
    where s = a & b.
    """
    seps = tree.get_separators()
    cliques = tree.nodes()

    weight = 0

    for clique in cliques:
        weight += np.triu(prob_matrix[np.ix_(list(clique), list(clique))]).sum()

    edge_probs = {}
    for sep, seplist in seps.items():
        
        #print("Cliques spearated by "+str(sep))
        for edge in seplist:
            #edge = frozenset([node1, node2])
            #print(node1, node2)
            edge_probs[edge] = edge_prob(edge, prob_matrix)
            weight += edge_probs[edge]
            #print(edge)
            #print(edge_probs[edge])

    
    #print(seps)
    #print(tree.edges)
    #print(prob_matrix)    
    #ixgrid = np.ix_([1,0], [0,2])
    #print(prob_matrix[ixgrid])
    return weight


def test():
    tree = jtlib.JunctionTree()
    np.random.seed(0)
    tree.add_node(frozenset([0,1,2]))
    tree.add_node(frozenset([3,4]))
    tree.add_node(frozenset([5]))
    tree.add_edge(frozenset([3,4]),frozenset([0,1,2]))
    tree.add_edge(frozenset([5]),frozenset([0,1,2]))

    #prob_matrix = np.random.rand(5, 5)
    #prob_matrix = np.array([[0.0, 0.9 ,0.9, 0.1, 0.1],
    #                        [0.0, 0.0 ,0.9, 0.1, 0.1],
    #                        [0.0, 0.0 ,0.0, 0.1, 0.1],
    #                        [0.0, 0.0 ,0.0, 0.0, 0.9],
    #                        [0.0, 0.0 ,0.0, 0.0, 0.0]
    #])
    prob_matrix = np.array([[0.0, 0.9 ,0.9, 0.1, 0.1, 0.1],
                            [0.0, 0.0 ,0.9, 0.1, 0.1, 0.1],
                            [0.0, 0.0 ,0.0, 0.1, 0.1, 0.1],
                            [0.0, 0.0 ,0.0, 0.0, 0.9, 0.1],
                            [0.0, 0.0 ,0.0, 0.0, 0.0, 0.1],
                            [0.0, 0.0 ,0.0, 0.0, 0.0, 0.0]
    ])
    #prob_matrix = np.array([[0.0, 0.9 ,0.9, 0.1, 0.1],
    #                        [0.0, 0.0 ,0.9, 0.8, 0.8],
    #                        [0.0, 0.0 ,0.0, 0.1, 0.1],
    #                        [0.0, 0.0 ,0.0, 0.0, 0.9],
    #                        [0.0, 0.0 ,0.0, 0.0, 0.0]
    #])
    #prob_matrix = np.array([[0.0, 0.9 ,0.9, 0.1, 0.1, 0.1],
    #                        [0.0, 0.0 ,0.9, 0.8, 0.8, 0.1],
    #                        [0.0, 0.0 ,0.0, 0.1, 0.1, 0.1],
    #                        [0.0, 0.0 ,0.0, 0.0, 0.9, 0.1],
    #                        [0.0, 0.0 ,0.0, 0.0, 0.0, 0.1],
    #                        [0.0, 0.0 ,0.0, 0.0, 0.0, 0.0]
    #])
    prob_matrix += prob_matrix.transpose()
    print("Matching probabilities")
    print(prob_matrix)
    prob = unnorm_prob(tree, prob_matrix)

    trprob = []
    maxprob = prob
    maxtree = tree
    print(maxprob)
    n_samples = 10000
    for i in range(n_samples):
        tree = jtlib.sample(prob_matrix.shape[0])
        prob = unnorm_prob(tree, prob_matrix)
        trprob.append((tree, prob))
        #print(prob)
        if prob > maxprob:
            maxprob = prob
            maxtree = tree
    print "Max weight (found by Monte Carlo sampling of " + str(n_samples) + " junction trees): ", str(maxprob)
    print "Max weight tree nodes"
    print(maxtree.nodes)
    print "Max weight tree edges"
    print(maxtree.edges)

    trprob.sort(key = lambda x: x[1]) 
    for t,p in trprob:
        print(p)
        print(t.nodes)
        print(t.edges)

if __name__ == "__main__":
    test()