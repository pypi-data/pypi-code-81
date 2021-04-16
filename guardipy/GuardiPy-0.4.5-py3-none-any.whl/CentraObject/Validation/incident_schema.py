SEVERITY = {
    "oneOf": [
        {
            "type": "string",
            "enum": ["Low", "Medium", "High"]
        },
        {
            "type": "array",
            "items": {
                "type": "string",
                "enum": ["Low", "Medium", "High"]
            }
        }
    ]
}

INCIDENT_TYPE = {
    "oneOf": [
        {
            "type": "string",
            "enum": ["Incident", "Deception", "Network Scan", "Reveal", "Experimental"]
        },
        {
            "type": "array",
            "items": {
                "type": "string",
                "enum": ["Incident", "Deception", "Network Scan", "Reveal", "Experimental"]
            }
        }
    ]
}

PREFIXED_FILTER = {
    "type": "string",
    "enum": ["lateral_movements", "policy_violations", "network_scans", "bad_reputation", "integrity_violations"]
}

DIRECTION = {
    "type": "string",
    "enum": ["unidirectional", "bidirectional"]
}

SENSOR_TYPE = {
    "type": "string",
    "enum": ["HONEYPOT", "DATAPATH_AGENT", "MITIGATION_AGENT", "VISIBILITY"]
}

CLS = {
    "type": "string",
    "enum": ["Incident.NetworkVisibilityIncident", "Incident.NetworkScanIncident", "Incident.HoneypotIncident"]
}
