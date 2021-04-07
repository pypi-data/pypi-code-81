import networkx


def read_graph_edges(filename):
    return networkx.read_edgelist(filename)


def get_graph_summary(graph):
    return "V:{}; E:{}".format(graph.number_of_nodes(), graph.number_of_edges())


def get_graph_vertices_at_distance(graph, vertex, distance):
    vertices = list(networkx.descendants_at_distance(graph, vertex, distance))
    vertices.sort()
    return vertices


def get_graph_vertices_up_to_distance(graph, vertex, max_distance):
    list = []
    for distance in range(max_distance + 1):
        vertices = get_graph_vertices_at_distance(graph, vertex, distance)
        list.extend(vertices)
    list.sort()
    return list
