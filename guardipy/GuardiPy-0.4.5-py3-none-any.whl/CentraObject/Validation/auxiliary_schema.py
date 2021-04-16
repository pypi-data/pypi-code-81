ASSET_TYPE = {
    "type": "string",
    "enum": ["IP", "VM"]
}

RECOMMENDATION_TYPE = {
    "type": "string",
    "enum": ["text", "expression", "mute", "bold"]
}

HANDLE_TEMPLATE = {
    "type": "string",
    "enum": [
        "VMRecommendation", "NetworkVMRecommendation",
        "FileQuarantineRecommendation", "RansomwareVMRecommendation",
        "RansomwareNonVMRecommendation", "PanIpRecommendation"
    ]
}

RULE_TYPE = {
    "type": "string",
    "enum": ["FILES", "NETWORK"]
}

FLAG_TYPE = {
    "type": "string",
    "enum": [
        "PollingMode", "OutdatedPolicy",
        "OutdatedConfiguration", "NoRevealReceived", 
        "HighDropRate", "AgentMissing", 
        "PartialPolicy", "EnforcementPaused", 
        "NoRevealReported", "RevealOffline", 
        "EnforcementOffline", "RevealModuleError",
        "EnforcementModuleError", "DetectionModuleError",
        "DeceptionModuleError", "ControllerModuleError"
    ]
}

CRITERIA_SCHEMA = {
    "type": "object",
    "properties": {
        "argument": {"type": "string"},
        "field": {"type": "string"},
        "op": {
            "type": "string",
            "enum": ["STARTSWITH", "ENDSWITH", "EQUALS", "CONTAINS", "SUBNET", "WILDCARDS"]
        },
        "source": {
            "type": "string",
            "enum": ["User", "Orchestration", "Agent"]
        },
        "label_id": {"type": "string"}
    },
    "required": ["argument", "field", "op"]
}

