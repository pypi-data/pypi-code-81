import itertools, functools
import networkx.classes.digraph as nxdigraph
from networkdisk import sql as ndsql
from networkdisk.sql.dialect import sqldialect as dialect
from networkdisk.utils import notProvidedArg
from networkdisk.mock import copymock
from networkdisk.exception import NetworkDiskError
from networkdisk.sql import classes as ndclasses

__all__ = ["DiGraph"]

@dialect.register(False)
class DiGraph(dialect.Graph, nxdigraph.DiGraph):
	nx_variant = nxdigraph.DiGraph
	def __post_init__(self):
		del self._pred
		self._pred = self.pred_dict_factory()
		return super().__post_init__()

	@property
	def schema_class(self):
		return self.dialect.graph_schema.DiGraphSchema.func
	@property
	def default_schema(self):
		return self.dialect.schemata.load_digraph

	def _get_all_tupleDicts(self):
		yield from super()._get_all_tupleDicts()
		yield self._pred

	@property
	def edges(self):
		return ndsql.classes.OutEdgeView(self)
	@property
	def in_edges(self):
		return ndsql.classes.InEdgeView(self)
	@property
	def out_edges(self):
		return self.edges
	@property
	def degree(self):
		return ndsql.classes.DiDegreeView(self)
	@property
	def in_degree(self):
		return ndsql.classes.InDegreeView(self)
	@property
	def out_degree(self):
		return ndsql.classes.OutDegreeView(self)

	reverse = ndclasses.reverse_view

	def to_undirected(self, as_view=True, reciprocal=False):
		if not as_view:
			raise NetworkDiskError(f"Cannot perform deepcopy of {self.__class__} in DB")
		unschema = self.schema.to_undirected(reciprocal=reciprocal)
		G = self.dialect.Graph(db=self.helper, schema=unschema, create=False, insert_schema=False)
		G._graph = self
		return G

