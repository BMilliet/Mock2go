from flask import json
from . import decodables


def get_services():
    services = []

    control = get_json_content('./control/control.json')
    for service in control['services']:
        services.append(decodables.Service.from_dict(service))
    return services


def get_json_content(file_path):
    with open(file_path) as f:
        return json.loads(f.read())


def update_control(services):
    _create_json_file(_create_control_json(services))


def _create_json_file(json_file):
    with open('./control/control.json', 'w') as f:
        f.write(json_file)


def _create_control_json(services):
    services_list = []
    for s in services:
        services_list.append(s.serialize())
    control_json = {
        'services': services_list
    }
    return json.dumps(control_json, indent=2, sort_keys=True)
