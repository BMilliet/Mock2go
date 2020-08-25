from flask import json
from . import decodables


def get_services():
    control = get_json_content('./control/control.json')
    return [decodables.Service.from_dict(s) for s in control['services']]


def get_json_content(file_path):
    with open(file_path) as f:
        return json.loads(f.read())


def update_control(services):
    _create_json_file(_create_control_json(services))


def _create_json_file(json_file):
    with open('./control/control.json', 'w') as f:
        f.write(json_file)


def _create_control_json(services):
    control_json = {
        'services': [s.serialize() for s in services]
    }
    return json.dumps(control_json, indent=2, sort_keys=True)
