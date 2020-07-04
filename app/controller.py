import time
from flask import render_template
from . import jsonLoader, decodables


services = []

control = jsonLoader.loadJson('./control/control.json')
for service in control['services']:
    services.append(decodables.Service.from_dict(service))


def get_response_for_route(path, delay=0):
    if path == 'index':
        return _render_index()
    time.sleep(delay)
    return _get_response(path)


def _get_response(path):
    for s in services:
        for p in s.get_paths():
            if _has_route_with_parameter(path, p):
                json_path = s.get_response_for_path(p)
                return jsonLoader.loadJson(json_path)
    return _get_response_for_path(path)


def _get_response_for_path(path):
    for s in services:
        if path in s.get_paths():
            json_path = s.get_response_for_path(path)
            return jsonLoader.loadJson(json_path)
    return 'path not found'


def _has_route_with_parameter(path1, path2):
    resp = set(path2.split('/')).difference(path1.split('/'))
    if len(resp) == 1:
        return list(resp)[0] == 'PARAMETER'
    return False


def _render_index():
    return render_template('index.html', services=services)
