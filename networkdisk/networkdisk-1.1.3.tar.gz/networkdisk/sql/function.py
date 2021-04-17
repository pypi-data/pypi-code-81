import functools, copy
import networkx as nx

@functools.wraps(nx.freeze)
def freeze(G):
	node = G._node
	del G._node
	G._node = node.to_readonly()
	adj = G._adj
	del G._adj
	G._adj = adj.to_readonly()
	edgestore = G.edgestore
	del G.edgestore
	G.edgestore = edgestore.to_readonly()
	if G.is_directed():
		pred = G._pred
		del G._pred
		G._pred = pred.to_readonly()
		del G._succ
		G._succ = G._adj
	return nx.freeze(G)

def frozen_copy(G):
	H = copy.copy(G)
	return freeze(H)

