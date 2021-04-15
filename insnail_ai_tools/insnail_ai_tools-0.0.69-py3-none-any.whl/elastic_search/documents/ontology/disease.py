from elasticsearch_dsl import Document

from insnail_ai_tools.elastic_search.mixin import AioMixin
from insnail_ai_tools.elastic_search.mongodb_plugin import MongoToEs
from insnail_ai_tools.mongodb.model.ontology.disease import OntologyDisease


@MongoToEs(OntologyDisease)
class OntologyDiseaseIndex(Document, AioMixin):
    class Index:
        name = f"ontology_disease"
