from .dialect import sqlitedialect as dialect
import networkdisk.sql as ndsql
import networkdisk.sqlite as ndsqlite

@dialect.register(False)
class DiGraph(dialect.DiGraph, dialect.Graph):
	pass

