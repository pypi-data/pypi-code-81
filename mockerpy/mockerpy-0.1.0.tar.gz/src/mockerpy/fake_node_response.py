import datetime
import json
import os
import random
import string


def fake_node(labels={}, role="worker", cpus=4, ram=16, hostname="node0"):
    id_ = "".join(random.choices(string.ascii_lowercase + string.digits, k=25))
    created = datetime.datetime.now().isoformat()
    cpus = cpus * 10e9
    ram = ram * 10e9
    address = f"10.0.0.{random.randint(1, 255)}"

    response = {
        "ID": id_,
        "Version": {"Index": 102289},
        "CreatedAt": created,
        "UpdatedAt": created,
        "Spec": {"Labels": labels, "Role": role, "Availability": "active"},
        "Description": {
            "Hostname": hostname,
            "Platform": {"Architecture": "x86_64", "OS": "linux"},
            "Resources": {"NanoCPUs": cpus, "MemoryBytes": ram},
            "Engine": {
                "EngineVersion": "19.03.8",
                "Plugins": [
                    {"Type": "Log", "Name": "awslogs"},
                    {"Type": "Log", "Name": "fluentd"},
                    {"Type": "Log", "Name": "gcplogs"},
                    {"Type": "Log", "Name": "gelf"},
                    {"Type": "Log", "Name": "journald"},
                    {"Type": "Log", "Name": "json-file"},
                    {"Type": "Log", "Name": "local"},
                    {"Type": "Log", "Name": "logentries"},
                    {"Type": "Log", "Name": "splunk"},
                    {"Type": "Log", "Name": "syslog"},
                    {"Type": "Network", "Name": "bridge"},
                    {"Type": "Network", "Name": "host"},
                    {"Type": "Network", "Name": "ipvlan"},
                    {"Type": "Network", "Name": "macvlan"},
                    {"Type": "Network", "Name": "null"},
                    {"Type": "Network", "Name": "overlay"},
                    {"Type": "Volume", "Name": "local"},
                ],
            },
            "TLSInfo": {
                "TrustRoot": "-----BEGIN CERTIFICATE-----\nMIIBajCCARCgAwIBAgIUf3AASOFsXsm839+ejXV0CWcPMLQwCgYIKoZIzj0EAwIw\nEzERMA8GA1UEAxMIc3dhcm0tY2EwHhcNMjAwNTAxMTI0NTAwWhcNNDAwNDI2MTI0\nNTAwWjATMREwDwYDVQQDEwhzd2FybS1jYTBZMBMGByqGSM49AgEGCCqGSM49AwEH\nA0IABEWvr5dTY+OlBkOWYDOzHfWattzfi/kFimfNN3B6KMSRf+yU/9t3NiL+SneT\ncFTUF1TxwAfmX56Hn2QEFeDqIyWjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMB\nAf8EBTADAQH/MB0GA1UdDgQWBBS7KSOtEz4xhbFFCgh6fFUnCJ0nyDAKBggqhkjO\nPQQDAgNIADBFAiBK+peMx+5tpvBPmoeITV+U5zl0K4vhGPNwlDWHdzlepQIhALWY\nbqfjOSntec0g+wzeggEnewFlQn7afHftm7x8Y22z\n-----END CERTIFICATE-----\n",
                "CertIssuerSubject": "MBMxETAPBgNVBAMTCHN3YXJtLWNh",
                "CertIssuerPublicKey": "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAERa+vl1Nj46UGQ5ZgM7Md9Zq23N+L+QWKZ803cHooxJF/7JT/23c2Iv5Kd5NwVNQXVPHAB+ZfnoefZAQV4OojJQ==",
            },
        },
        "Status": {"State": "ready", "Addr": address},
    }
    if role == "manager":
        response.update({"ManagerStatus": {"Leader": True, "Reachability": "reachable", "Addr": f"{address}.1:2377"}})
    return response


def create_fake_node(path, labels={}, role="worker", cpus=4, ram=16, hostname="node0"):
    data = read_fake_nodes(path)
    data.append(fake_node(labels, role, cpus, ram, hostname))

    with open(os.path.join(path, "nodes.json"), "w") as file:
        json.dump(data, file)


def read_fake_nodes(path):
    file_path = os.path.join(path, "nodes.json")

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
    else:
        data = []

    return data
