from jsonschema import validate, ValidationError, SchemaError
import logging

from GuardiPy.CentraObject.Validation.agent_schema import (
    OS,
    STATUS,
    ENFORCEMENT,
    DEPLOYMENT,
    ACTIVITY,
    INSTALLED_MODULES,
    CONFIGURATION_REPORTED_ERRORS
)

from GuardiPy.CentraObject.Validation.incident_schema import (
    SEVERITY,
    INCIDENT_TYPE,
    PREFIXED_FILTER,
    DIRECTION,
    SENSOR_TYPE,
    CLS
)

from GuardiPy.CentraObject.Validation.auxiliary_schema import (
    ASSET_TYPE,
    RECOMMENDATION_TYPE,
    HANDLE_TEMPLATE,
    RULE_TYPE,
    FLAG_TYPE
)

from GuardiPy.CentraObject.Validation.event_schema import (
    EVENT_TYPE
)


def fits_schema(entity, schema) -> bool:
    is_valid = False
    try:
        if entity is not None:
            validate(entity, schema)
        is_valid = True
    except (ValidationError, SchemaError):
        logging.error("Failed to validate entity.", exc_info=True)
    finally:
        return is_valid
