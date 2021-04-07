import logging

from jsonschema import validate, ValidationError, SchemaError

GC_CSV_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "severity": {"enum": ["Low", "Medium", "High"]},
        "start_time (utc)": {"type": "string"},
        "incident_type": {"enum": ["Incident", "Deception", "Network Scan", "Reveal", "Experimental"]},
        "affected_assets": {"type": "string"},
        "tags": {"type": "string"},
        "incident_group": {"type": "string"},
        "exporting_error": {"type": "string"}
    },
    "required": ["id", "affected_assets"]
}

CENTRA_SCHEMA = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "dev_host": {"type": "string"},
        "password": {"type": "string"}
    },
    "required": ["username", "dev_host", "password"]
}


def is_valid_format(entity, schema) -> bool:
    valid = False
    try:
        validate(entity, schema)
        valid = True
    except (ValidationError, SchemaError):
        valid = False
        logging.error(f"Object validation failed.", exc_info=True)
    finally:
        return valid
