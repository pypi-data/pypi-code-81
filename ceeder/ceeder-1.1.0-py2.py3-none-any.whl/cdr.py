from typing import Dict

import jsonschema


def cdr(extracted_text="Hello world!") -> Dict:
    """cdr returns a fairly bare-bones CDR object that should pass
    validation."""
    return {
        "uri": "https://qntfy.com",
        "source_uri": "https://qntfy.com",
        "timestamp": "2019-09-24T12:23:51.000Z",
        "capture_source": "BackgroundSource",
        "extracted_ntriples": '<http://graph.causeex.com/documents/sources#x> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://ontology.causeex.com/ontology/odps/DataProvenance#Document> .\n<http://graph.causeex.com/documents/sources#x> <http://ontology.causeex.com/ontology/odps/DataProvenance#has_capture_source> <http://ontology.causeex.com/ontology/odps/DataProvenance#BackgroundSource> .\n<http://graph.causeex.com/documents/sources#x> <http://ontology.causeex.com/ontology/odps/DataProvenance#original_source> "x.pdf" .\n<http://graph.causeex.com/documents/sources#x> <http://ontology.causeex.com/ontology/odps/GeneralConcepts#canonical_label> "x" .\n<http://graph.causeex.com/documents/sources#x> <http://ontology.causeex.com/ontology/odps/DataProvenance#time_retrieved> "2019-09-24T12:23:51"^^<http://www.w3.org/2001/XMLSchema#dateTime> .\n<http://graph.causeex.com/documents/sources#x> <http://ontology.causeex.com/ontology/odps/DataProvenance#has_document_type> <http://ontology.causeex.com/ontology/odps/DataProvenance#Unstructured> .\n<http://graph.causeex.com/documents/sources#x> <http://ontology.causeex.com/ontology/odps/DataProvenance#date_created> "2017-11-10" .\n<http://graph.causeex.com/documents/sources#x> <http://ontology.causeex.com/ontology/odps/DataProvenance#author> "SOPER Anna" .\n<http://graph.causeex.com/documents/sources#x> <http://ontology.causeex.com/ontology/odps/DataProvenance#date_modified> "2017-11-10" .\n',
        "extracted_metadata": {
            "CreationDate": "2017-11-10",
            "ModDate": "2017-11-10",
            "Author": "SOPER Anna",
            "Pages": 3,
            "Creator": "Microsoft? Publisher 2016",
            "Producer": "Microsoft? Publisher 2016",
        },
        "content_type": "application/pdf",
        "team": "Two Six Labs",
        "document_id": "x",
        "extracted_text": extracted_text,
    }


def schema() -> Dict:
    """schema returns the CDR V5 schema as a dictionary."""
    from pkg_resources import resource_string
    import json

    data = resource_string("ceeder.schemas", "cdr-v5.json")
    return json.loads(data)


def validate(cdr: Dict):
    """validate takes in a dictionary and validates it against a CDR schema.

    This throws an exception if it fails, so be prepared to handle
    that if calling this code in a function."""
    jsonschema.validate(instance=cdr, schema=schema())
