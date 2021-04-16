import json
import os

from .responses import *


def create_fake_service(path, name, labels={}, replicas=1, service_ip=None):
    services = read_fake_services(path)
    tasks = read_fake_tasks(path)

    if not service_ip:
        service_ip = f"10.0.0.{random.randint(1, 255)}"
    service = fake_service(name, labels, replicas, service_ip)
    service_id = service.get("ID")
    services.append(service)

    for r in range(0, replicas):
        task_ip = f"10.0.0.{random.randint(1, 255)}"
        node_id = "".join(random.choices(string.ascii_lowercase + string.digits, k=25))
        tasks.append(create_fake_task(task_ip, service_id, node_id))

    with open(os.path.join(path, "services.json"), "w") as file:
        json.dump(services, file)

    with open(os.path.join(path, "tasks.json"), "w") as file:
        json.dump(services, file)


def read_fake_services(path):
    file_path = os.path.join(path, "services.json")

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
    else:
        data = []

    return data


def read_fake_tasks(path):
    file_path = os.path.join(path, "tasks.json")

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
    else:
        data = []

    return data
