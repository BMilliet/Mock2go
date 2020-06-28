from . import jsonLoader, decodables


services = []

control = jsonLoader.loadJson('./control/control.json')
for service in control['services']:
    services.append(decodables.Service.from_dict(service))


def get_response_for_route(path):
    for s in services:
        if path in s.get_paths():
            json_path = s.get_response_for_path(path)
            return jsonLoader.loadJson(json_path)
    return 'path not found'
