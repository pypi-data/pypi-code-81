OS = {
    "type": "string",
    "enum": [
        "Unknown",
        "Windows",
        "Linux"
    ]
}

STATUS = {
    "type": "string",
    "enum": [
        "OFFLINE",
        "ONLINE"
    ]
}

ENFORCEMENT = {
    "type": "string",
    "enum": [
        "Active",
        "Not Deployed",
        "Enforcement disabled from management console"
    ]
}

DEPLOYMENT = {
    "type": "string",
    "enum": [
        "Active",
        "Not Deployed"
    ]
}

ACTIVITY = {
    "type": "string",
    "enum": [
        "last_month",
        "last_week",
        "last_12_hours",
        "last_24_hours",
        "not_active"
    ]
}

INSTALLED_MODULES = {
    "type": "string",
    "enum": [
        "DECEPTION_AGENT",
        "REVEAL_AGENT",
        "ENFORCEMENT_AGENT",
        "DETECTION_AGENT",
        "CONTROLLER"
    ]
}

CONFIGURATION_REPORTED_ERRORS = {
    "type": "object",
    "properties": {
        "enforcementagent": {
            "type": "object",
            "properties": {
                "agent_dns_enable": {"type": "string"},
                "agent_dns_rate_limit": {"type": "string"}
            }
        }
    },
    "additional_properties": False,
    "required_properties": ["enforcementagent"]
}
