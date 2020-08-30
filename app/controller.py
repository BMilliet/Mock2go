import time
from flask import render_template, Response, json, redirect
from . import formHandler, jsonHandler, decodables, modelHandler


def get_response_for_route(path, req):
    if path == 'index':
        return _handle_index(req)
    elif path == 'edit':
        return _handle_edit(req)
    elif path == 'add':
        return _handle_add(req)

    return _get_response(path)


def _get_response(path):
    services = jsonHandler.get_services()
    existing_paths = modelHandler.get_paths_tuple(services)

    if path in existing_paths[0]:
        print("in regular")
        return _try_response_for_path(path, services)

    return _try_response_for_path_with_param(path, existing_paths[1], services)


def _try_response_for_path(path, services):
    route = modelHandler.get_response_from_path(path, services)
    return _get_response_for_route(route)


def _try_response_for_path_with_param(path, paths, services):
    route = None

    print("try with params")

    for p in paths:
        if modelHandler.is_same_route(path, p):
            print("found route")
            route = modelHandler.get_response_from_path(p, services)

    return _get_response_for_route(route)


def _get_response_for_route(route):
    if route is None:
        return Response('path not found', status=404)

    return _build_reponse(route.to_tuple())


def _handle_index(req):
    if req.method == 'POST':
        formHandler.update_control_from_post_form(req.form)
        return redirect(req.url)

    return render_template('index.html', services=jsonHandler.get_services())


def _build_reponse(response_tuple):
    time.sleep(response_tuple[2])
    body = jsonHandler.get_json_content(response_tuple[0])
    return Response(response=json.dumps(body),
                    status=response_tuple[1],
                    mimetype='application/json')


def _handle_add(req):
    if req.method == 'POST':
        formHandler.update_control_from_post_form_add_new(req)
        return redirect('/index')
    return render_template('add_form.html')


def _handle_edit(req):
    if req.method == 'POST':
        formHandler.update_control_from_edit_form(req)
        return redirect('/index')
    return render_template('edit_form.html',
                           service=_get_service_by_name(req.args['name']))


def _get_service_by_name(name):
    for s in jsonHandler.get_services():
        if name == s.get_name():
            return s
    return None
