from .dialect import dialect
from networkdisk.oracle import columns
from networkdisk.oracle import queries
from networkdisk.oracle import schema
from networkdisk.oracle import helper	#after schema and queries!
from networkdisk.oracle import tupledict
import networkdisk.oracle.graph
import networkdisk.oracle.digraph

__all__ = [
	'dialect', 'Graph', 'DiGraph', 'MasterGraphs',
	'load_graph', 'load_ungraph', 'load_digraph',
	'list_graphs', 'list_ungraphs', 'list_digraphs'
]

Graph = dialect.Graph
DiGraph = dialect.DiGraph
MasterGraphs = dialect.master.MasterGraphs

load_graph = dialect.master.load_graph
load_digraph = dialect.master.load_digraph
load_unraph = dialect.master.load_ungraph
list_graphs = dialect.master.list_graphs
list_ungraphs = dialect.master.list_ungraphs
list_digraphs = dialect.master.list_digraphs

