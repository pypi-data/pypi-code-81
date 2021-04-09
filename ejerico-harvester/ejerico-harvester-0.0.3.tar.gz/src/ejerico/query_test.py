from rdflib import plugin, Graph, Literal, URIRef, ConjunctiveGraph

import json
from rdflib.store import Store
from rdflib_sqlalchemy import registerplugins
from rdflib import Graph
import psycopg2
import sys
from sqlalchemy import create_engine
from ejerico_sdk.rdf.graph_factory import GraphFactory
from ejerico.bootstrap import Bootstrap
import  argparse
from rdflib.plugins.sparql.results.jsonresults import JSONResultSerializer
from rdflib.plugins.sparql.results.xmlresults import XMLResultSerializer
from rdflib.query import ResultSerializer
from rdflib.plugins.sparql.processor import SPARQLResult
from io import BytesIO
from rdflib.query import EncodeOnlyUnicode


def regplugins():
    """
    If rdfextras is installed with setuptools, all plugins are registered
    through entry_points. This is strongly recommended.

    If only distutils is available, the plugins must be registed manually
    This method will register all rdfextras plugins

    """
    from rdflib import plugin
    from rdflib.query import Processor

    try:
        x = plugin.get('sparql', Processor)
        return  # plugins already registered
    except:
        pass  # must register plugins

    from rdflib.store import Store
    from rdflib.parser import Parser
    from rdflib.serializer import Serializer
    from rdflib.query import ResultParser, ResultSerializer, Result

    plugin.register('rdf-json', Parser,
                    'rdfextras.parsers.rdfjson', 'RdfJsonParser')
    plugin.register('json-ld', Parser,
                    'rdfextras.parsers.jsonld', 'JsonLDParser')
    plugin.register('rdf-json', Serializer,
                    'rdfextras.serializers.rdfjson', 'RdfJsonSerializer')
    plugin.register('json-ld', Serializer,
                    'rdfextras.serializers.jsonld', 'JsonLDSerializer')
    plugin.register('html', Serializer,
                    'rdfextras.sparql.results.htmlresults', 'HTMLSerializer')

    plugin.register('sparql', Result,
                    'rdfextras.sparql.query', 'SPARQLQueryResult')
    plugin.register('sparql', Processor,
                    'rdfextras.sparql.processor', 'Processor')

    plugin.register('html', ResultSerializer,
                    'rdfextras.sparql.results.htmlresults', 'HTMLResultSerializer')
    plugin.register('xml', ResultSerializer,
                    'rdfextras.sparql.results.xmlresults', 'XMLResultSerializer')
    plugin.register('json', ResultSerializer,
                    'rdfextras.sparql.results.jsonresults', 'JSONResultSerializer')
    plugin.register('xml', ResultParser,
                    'rdfextras.sparql.results.xmlresults', 'XMLResultParser')
    plugin.register('json', ResultParser,
                    'rdfextras.sparql.results.jsonresults', 'JSONResultParser')

    plugin.register('SPARQL', Store,
                    'rdfextras.store.SPARQL', 'SPARQLStore')

def querySQL():

    try:
        conn = psycopg2.connect("dbname='js3socib' user='ejerico' host='postgres.test.socib.es' port='5433' password='ejerico'")
    except:
        print
        "I am unable to connect to the database"

    cur = conn.cursor()
    cur.execute("""SELECT * from public.kb_50c30dab39_literal_statements""")
    rows = cur.fetchall()
    for row in rows:
        print(row)

def query4():
    store = plugin.get("SQLAlchemy", Store)(configuration="postgresql+psycopg2://ejerico:ejerico@postgres.test.socib.es:5433/js3socib")
    g = Graph(store, identifier="test")
    results = g.query("""SELECT ?s ?p ?o WHERE {?s ?p ?o .} LIMIT 1""")
    for row in results:
        print(row)

def query3():
    engine = create_engine('postgresql+psycopg2://ejerico:ejerico@postgres.test.socib.es:5433/js3socib')
    result = engine.execute("""SELECT * from public.kb_50c30dab39_literal_statements""")
    for r in result:
        print(r)

def query2():

    registerplugins()
    identifier = URIRef("js3socib")
    db_uri = Literal('postgresql+psycopg2://ejerico:ejerico@postgres.test.socib.es:5433/js3socib')
    store = plugin.get("SQLAlchemy", Store)(identifier=identifier)
    graph = ConjunctiveGraph(store, identifier=identifier)
    graph.open(db_uri)
    # do stuff with graph
    query = "select ?s ?p ?o where { ?s ?p ?o } limit 25"
    query_result = graph.query(query)
    for subject, predicate in query_result:
        print(subject, predicate)
    graph.close()

def query1():
    register(
        'xml', Serializer,
        'rdflib.plugins.serializers.rdfxml', 'XMLSerializer')
    registerplugins()
    identifier = URIRef("ejerico")
    db_uri = Literal('postgresql://ejerico:ejerico@postgres.test.socib.es:5433/js3socib')
    store = plugin.get("EJERICOStore", Store)(identifier=identifier, configuration=db_uri)
    graph = Graph(store, identifier=identifier)

    query = "select ?s ?p ?o where { ?s ?p ?o } limit 25"
    query_result = graph.query(query)

    for subject, predicate in query_result:
        print(subject, predicate)

    graph.close()
    print("done")

'''
https://programtalk.com/python-examples-amp/rdflib.plugin.get/
    def serialize(
            self, destination=None, encoding="utf-8", format='xml', **args):

        if self.type in ('CONSTRUCT', 'DESCRIBE'):
            return self.graph.serialize(
                destination, encoding=encoding, format=format, **args)

        """stolen wholesale from graph.serialize"""
        from rdflib import plugin
        serializer = plugin.get(format, ResultSerializer)(self)
        if destination is None:
            stream = BytesIO()
            stream2 = EncodeOnlyUnicode(stream)
            serializer.serialize(stream2, encoding=encoding, **args)
            return stream.getvalue()
        if hasattr(destination, "write"):
            stream = destination
            serializer.serialize(stream, encoding=encoding, **args)
        else:
            location = destination
            scheme, netloc, path, params, query, fragment = urlparse(location)
            if netloc != "":
                print("WARNING: not saving as location" +
                      "is not a local file reference")
                return
            fd, name = tempfile.mkstemp()
            stream = os.fdopen(fd, 'wb')
            serializer.serialize(stream, encoding=encoding, **args)
            stream.close()
            if hasattr(shutil, "move"):
                shutil.move(name, path)
            else:
                shutil.copy(name, path)
                os.remove(name)
'''

def query():
    #regplugins()
    graph = GraphFactory.createGraph()
    #a= graph.serialize(format='xml')

    format = "xml"
    encoding = "utf-8"
    query = "select ?s ?p ?o where { ?s ?p ?o } limit 5"
    query_result = graph.query(query)
    serializer = plugin.get(format, ResultSerializer)(query_result)
    stream = BytesIO()
    stream2 = EncodeOnlyUnicode(stream)
    JSONResultSerializer(query_result).serialize(stream2)
    #serializer.serialize(stream2, encoding=encoding, format="json")

    a = stream.getvalue()
    JSONResultSerializer(query_result).serialize(sys.stdout)
    #for row in query_result:
    #    print(row)

    graph.close()
    print("done")

if __name__ == "__main__":
    #[COMMAND] command line arguments (definition & parser)
    parser = argparse.ArgumentParser("ejerico")

    parser.add_argument("-cp", "--config_path", type=str, help="configuration - config file path", action="append")
    parser.add_argument("-cu", "--config_url", type=str, help="configuration - server url")
    parser.add_argument("-cuu", "--config_username", type=str, help="configuration - server username")
    parser.add_argument("-cup", "--config_password", type=str, help="configuration - server password")
    parser.add_argument("-cut", "--config_token", type=str, help="configuration - server jwt token")

    args = parser.parse_args()

    #[CONFIG] get configuration
    bootstrap = Bootstrap.instance()
    bootstrap.boot(args)

    query()
