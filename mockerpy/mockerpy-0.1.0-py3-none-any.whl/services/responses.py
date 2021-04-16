import datetime
import random
import string


def fake_service(name, labels={}, replicas=1, ip="0.0.0.0", image="busybox:latest", stack="test", env=[], mounts=[], secrets=[]):
    id_ = "".join(random.choices(string.ascii_lowercase + string.digits, k=25))
    created = datetime.datetime.now().isoformat()

    response = {
        "ID": id_,
        "Version": {"Index": 540403},
        "CreatedAt": created,
        "UpdatedAt": created,
        "Spec": {
            "Name": name,
            "Labels": labels,
            "TaskTemplate": {
                "ContainerSpec": {
                    "Image": image,
                    "Labels": {"com.docker.stack.namespace": stack},
                    "Env": env,
                    "Privileges": {"CredentialSpec": None, "SELinuxContext": None},
                    "Mounts": mounts,
                    "StopGracePeriod": 10000000000,
                    "DNSConfig": {},
                    "Secrets": secrets,
                    "Isolation": "default",
                },
                "Resources": {},
                "RestartPolicy": {"Condition": "any", "Delay": 5000000000, "MaxAttempts": 0},
                "Placement": {"Constraints": ["node.role == manager"]},
                "Networks": [{"Target": "dvk0wjcurx7fxuzyiow1lsg4l", "Aliases": ["worker"]}],
                "ForceUpdate": 0,
                "Runtime": "container",
            },
            "Mode": {"Replicated": {"Replicas": replicas}},
            "UpdateConfig": {
                "Parallelism": 1,
                "FailureAction": "pause",
                "Monitor": 5000000000,
                "MaxFailureRatio": 0,
                "Order": "start-first",
            },
            "RollbackConfig": {
                "Parallelism": 1,
                "FailureAction": "pause",
                "Monitor": 5000000000,
                "MaxFailureRatio": 0,
                "Order": "stop-first",
            },
            "EndpointSpec": {"Mode": "vip"},
        },
        "Endpoint": {
            "Spec": {"Mode": "vip"},
            "VirtualIPs": [{"NetworkID": "dvk0wjcurx7fxuzyiow1lsg4l", "Addr": f"{ip}/24"}],
        },
        "UpdateStatus": {
            "State": "completed",
            "StartedAt": "2020-09-03T14:25:16.896849425Z",
            "CompletedAt": "2020-09-03T14:25:26.360942508Z",
            "Message": "update completed",
        },
    }

    return response


def create_fake_task(ip, service_id, node_id, image="busybox:latest", stack="test", env=[], mounts=[], labels={}):
    id_ = "".join(random.choices(string.ascii_lowercase + string.digits, k=25))
    task = {
        "ID": id_,
        "Version": {"Index": 540233},
        "CreatedAt": "2020-09-03T14:25:02.234732726Z",
        "UpdatedAt": "2020-09-03T14:25:06.734835739Z",
        "Labels": labels,
        "Spec": {
            "ContainerSpec": {
                "Image": image,
                "Labels": {"com.docker.stack.namespace": stack},
                "Env": env,
                "Privileges": {"CredentialSpec": None, "SELinuxContext": None},
                "Mounts": mounts,
                "Isolation": "default",
            },
            "Resources": {},
            "Placement": {"Constraints": ["node.role == manager"]},
            "Networks": [{"Target": "dvk0wjcurx7fxuzyiow1lsg4l", "Aliases": ["worker"]}],
            "ForceUpdate": 0,
        },
        "ServiceID": service_id,
        "Slot": 1,
        "NodeID": node_id,
        "Status": {
            "Timestamp": "2020-09-03T14:25:21.343807002Z",
            "State": "running",
            "Message": "started",
            "ContainerStatus": {
                "ContainerID": "01ae8f99bb31723212e69c94eab584efd930499b96d6b2b4473386e1da5d2a33",
                "PID": 21359,
                "ExitCode": 0,
            },
            "PortStatus": {},
        },
        "DesiredState": "running",
        "NetworksAttachments": [
            {
                "Network": {
                    "ID": "dvk0wjcurx7fxuzyiow1lsg4l",
                    "Version": {"Index": 540168},
                    "CreatedAt": "2020-09-03T14:24:55.571659723Z",
                    "UpdatedAt": "2020-09-03T14:24:55.573490272Z",
                    "Spec": {
                        "Name": "compute_default",
                        "Labels": {"com.docker.stack.namespace": "compute"},
                        "DriverConfiguration": {"Name": "overlay"},
                        "Scope": "swarm",
                    },
                    "DriverState": {
                        "Name": "overlay",
                        "Options": {"com.docker.network.driver.overlay.vxlanid_list": "4098"},
                    },
                    "IPAMOptions": {
                        "Driver": {"Name": "default"},
                        "Configs": [{"Subnet": f"{ip}/24", "Gateway": ip}],
                    },
                },
                "Addresses": [f"{ip}/24"],
            }
        ],
    }

    return task
