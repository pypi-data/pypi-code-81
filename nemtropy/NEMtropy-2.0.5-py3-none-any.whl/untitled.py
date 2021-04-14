from graph_classes import *
edgelist=[(0,1),(0,2),(0,4),(1,3),(2,3)]
ciao2 = BipartiteGraph(edgelist=edgelist)
ciao2.solve_tool(method='newton')
print(ciao2)