PLAN_TASK_SCHEMA = '''{
    "additionalProperties": false,
    "properties": {
        "storages": {
            "items": {
                "additionalProperties": false,
                "nullable": true,
                "properties": {
                    "balance": {
                        "additionalProperties": false,
                        "nullable": true,
                        "properties": {
                            "max_limit": {
                                "default": 0,
                                "format": "double",
                                "maximum": 10000000,
                                "minimum": 0,
                                "type": "number"
                            },
                            "min_limit": {
                                "default": 0,
                                "format": "double",
                                "maximum": 10000000,
                                "minimum": 0,
                                "type": "number"
                            },
                            "start_amount": {
                                "default": 0,
                                "format": "double",
                                "maximum": 10000000,
                                "minimum": 0,
                                "type": "number"
                            }
                        },
                        "required": [
                            "start_amount",
                            "min_limit",
                            "max_limit"
                        ],
                        "type": "object"
                    },
                    "forecast": {
                        "items": {
                            "additionalProperties": false,
                            "nullable": true,
                            "properties": {
                                "delta": {
                                    "default": 0,
                                    "format": "double",
                                    "maximum": 10000000,
                                    "minimum": -10000000,
                                    "type": "number"
                                },
                                "time_index": {
                                    "default": 0,
                                    "format": "int32",
                                    "maximum": 1000,
                                    "minimum": 0,
                                    "type": "integer"
                                }
                            },
                            "required": [
                                "time_index",
                                "delta"
                            ],
                            "type": "object"
                        },
                        "maxLength": 1000,
                        "minLength": 0,
                        "type": "array"
                    },
                    "key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "restricted_time_indexes": {
                        "items": {
                            "default": 0,
                            "format": "int32",
                            "maximum": 1000,
                            "minimum": 0,
                            "type": "integer"
                        },
                        "maxLength": 1000,
                        "minLength": 0,
                        "type": "array"
                    },
                    "tariff": {
                        "additionalProperties": false,
                        "nullable": true,
                        "properties": {
                            "storage_cost": {
                                "default": 0.001,
                                "format": "double",
                                "maximum": 10000,
                                "minimum": 0,
                                "type": "number"
                            },
                            "transfer_cost": {
                                "default": 0.001,
                                "format": "double",
                                "maximum": 1000000,
                                "minimum": 0,
                                "type": "number"
                            }
                        },
                        "required": [
                            "transfer_cost",
                            "storage_cost"
                        ],
                        "type": "object"
                    }
                },
                "required": [
                    "key",
                    "balance",
                    "forecast",
                    "tariff"
                ],
                "type": "object"
            },
            "maxItems": 10000,
            "minItems": 1,
            "type": "array"
        }
    },
    "required": [
        "storages"
    ],
    "type": "object"
}'''