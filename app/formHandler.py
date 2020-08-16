from . import decodables, jsonHandler
from werkzeug.utils import secure_filename
import os

JSON_STORAGE_DIR = "jsonMock"


def update_control_from_post_form(form):
    services = jsonHandler.get_services()
    for s in services:
        for r in s.get_routes():
            r.current_response = form[(
                'selected_response_%s' % r.get_path())]
            r.status = form[('status_%s' % r.get_path())]
            r.delay = form[('delay_%s' % r.get_path())]
    jsonHandler.update_control(services)


def update_control_from_post_form_add_new(req):
    if not req.form or not req.files:
        return

    routes = []
    for i, route in enumerate(req.form.getlist('route')):
        responses_path = []
        files = req.files.getlist('responses%s' % i)
        if files:
            for f in files:

                if not _valid_json(f.filename):
                    return

                file_path = './%s/%s/%s/%s' % (JSON_STORAGE_DIR,
                                               req.form['service_name'],
                                               route,
                                               secure_filename(f.filename))
                # file_path.save(os.path)

                # os.makedirs(os.path.dirname(file_path), exist_ok=True)

                responses_path.append(file_path)
        routes.append(_create_route(route, responses_path))

    services = jsonHandler.get_services()
    services.append(decodables.Service(req.form['service_name'], routes))
    jsonHandler.update_control(services)


def update_control_from_edit_form(req):
    if not req.form:
        return

    _update_control_from_remove(
        req) if 'remove' in req.form['service_name'] else _update_control_from_form_edit(req)


def _update_control_from_remove(req):
    ...
    # services = jsonHandler.get_services()
    # for s in services:
    #     if ("%s_remove" % s.get_name()) == form['service_name']:
    #         services.remove(s)
    # jsonHandler.update_control(services)


def _update_control_from_form_edit(req):
    ...
    # services = jsonHandler.get_services()
    # new = decodables.Service(
    #     form['service_name'], _create_routes_from_form(form))
    # for s in services:
    #     if s.get_name() == new.get_name():
    #         services.remove(s)
    #         services.append(new)
    # jsonHandler.update_control(services)


def _create_routes_from_form(form):
    routes = []
    for i, r in enumerate(form.getlist('route')):
        responses = form.getlist('responses')[i].split('\r\n')
        routes.append(decodables.Route(
            r, responses[0], 200, 0, responses).serialize())
    return routes


def _create_route(route, responses):
    return decodables.Route(route, responses[0], 200, 0, responses).serialize()


def _valid_json(filename):
    return filename.endswith(".json")
