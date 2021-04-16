PLAN_RESULT_SCHEMA = '''{
    "additionalProperties": false,
    "properties": {
        "tracedata": {
            "additionalProperties": false,
            "properties": {
                "client": {
                    "maxLength": 256,
                    "minLength": 2,
                    "type": "string"
                },
                "code": {
                    "maxLength": 256,
                    "minLength": 3,
                    "type": "string"
                },
                "method": {
                    "enum": [
                        "PLAN",
                        "CONVERT",
                        "ANALYTICS",
                        "PREDICT",
                        "ACTUALIZE",
                        "VALIDATE",
                        "ROUTE",
                        "MATRIX",
                        "CLUSTER"
                    ],
                    "type": "string"
                },
                "server": {
                    "maxLength": 256,
                    "minLength": 2,
                    "type": "string"
                },
                "service": {
                    "enum": [
                        "LASTMILE",
                        "DELIVERY",
                        "FIELDSERVICE",
                        "MERCHANDISER",
                        "ROUTING",
                        "CLUSTERING",
                        "ACCOUNT",
                        "STOCK",
                        "ADMIN"
                    ],
                    "type": "string"
                },
                "time": {
                    "format": "date-time",
                    "type": "string"
                }
            },
            "required": [
                "code"
            ],
            "type": "object"
        },
        "transfers": {
            "items": {
                "additionalProperties": false,
                "nullable": true,
                "properties": {
                    "input_amount": {
                        "default": 0,
                        "format": "double",
                        "maximum": 10000000,
                        "minimum": 0,
                        "type": "number"
                    },
                    "output_amount": {
                        "default": 0,
                        "format": "double",
                        "maximum": 10000000,
                        "minimum": 0,
                        "type": "number"
                    },
                    "storage_key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "time_index": {
                        "default": 0,
                        "format": "int32",
                        "maximum": 60,
                        "minimum": 0,
                        "type": "integer"
                    }
                },
                "required": [
                    "storage_key",
                    "time_index",
                    "input_amount",
                    "output_amount"
                ],
                "type": "object"
            },
            "maxItems": 10000,
            "minItems": 0,
            "type": "array"
        },
        "validations": {
            "items": {
                "additionalProperties": false,
                "properties": {
                    "entity_key": {
                        "maxLength": 1024,
                        "type": "string"
                    },
                    "entity_type": {
                        "maxLength": 1024,
                        "type": "string"
                    },
                    "info": {
                        "type": "string"
                    },
                    "type": {
                        "enum": [
                            "info",
                            "warning",
                            "error"
                        ],
                        "nullable": false,
                        "type": "string"
                    }
                },
                "required": [
                    "type",
                    "info"
                ],
                "type": "object"
            },
            "maxItems": 10000,
            "minItems": 0,
            "type": "array"
        }
    },
    "required": [
        "transfers"
    ],
    "type": "object"
}'''