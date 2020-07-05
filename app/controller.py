import time
from flask import render_template, Response, json, request, redirect
from . import decodables


def get_response_for_route(path, req):
    services = _get_services()
    if path == 'index':
        return _handle_index(req)
    return _get_response(path, services)


def _get_response(path, services):
    for s in services:
        for p in s.get_paths():
            if _has_route_with_parameter(path, p):
                response = s.get_response_for_path(p)
                return _build_reponse(response)

    return _get_response_for_path(path, services)


def _get_response_for_path(path, services):
    for s in services:
        if path in s.get_paths():
            response = s.get_response_for_path(path)
            return _build_reponse(response)
    return Response('path not found', status=404)


def _has_route_with_parameter(path1, path2):
    resp = set(path2.split('/')).difference(path1.split('/'))
    if len(resp) == 1:
        return list(resp)[0] == 'PARAMETER'
    return False


def _handle_index(req):
    if req.method == 'POST':
        _handle_post_form(request.form)
        return redirect(req.url)
    return render_template('index.html', services=_get_services())


def _get_services():
    services = []

    control = _loadJson('./control/control.json')
    for service in control['services']:
        services.append(decodables.Service.from_dict(service))
    return services


def _build_reponse(response_tuple):
    time.sleep(response_tuple[2])
    body = _loadJson(response_tuple[0])
    return Response(response=json.dumps(body),
                    status=response_tuple[1],
                    mimetype='application/json')


def _loadJson(file_path):
    with open(file_path) as f:
        return json.loads(f.read())


def _handle_post_form(form):
    services = _get_services()
    for s in services:
        if s.get_name() == form['service_name']:
            print(form['service_name'])
