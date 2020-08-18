from . import decodables, jsonHandler, fileHandler


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

    new_routes = []
    for i, route in enumerate(req.form.getlist('route')):
        responses_path = []
        files = req.files.getlist('responses%s' % i)
        if files:
            for f in files:

                if _valid_json(f.filename):
                    file_path = fileHandler.build_file_path(
                        req.form['service_name'],
                        route,
                        f.filename)

                    fileHandler.save_file_on_path(file_path, f)
                    responses_path.append(file_path)

        if len(responses_path) > 0:
            new_routes.append(_create_route(route, responses_path))

    services = jsonHandler.get_services()

    if req.form['service_name'] in decodables.get_services_names(services):
        for service in services:
            if service.get_name() == req.form['service_name']:
                for new in new_routes:
                    new.update_routes()
                    service.merge_routes(new)

    else:
        serialize_routes = map(_get_serialize_routes, new_routes)
        services.append(decodables.Service(
            req.form['service_name'], serialize_routes))

    jsonHandler.update_control(services)


def update_control_from_edit_form(req):
    if not req.form:
        return

    _update_control_from_remove(
        req) if 'remove' in req.form['service_name'] else _update_control_from_form_edit(req)


def _update_control_from_remove(req):
    services = jsonHandler.get_services()
    for s in services:
        if ("%s_remove" % s.get_name()) == req.form['service_name']:
            services.remove(s)
            fileHandler.delete_service(s.get_name())
    jsonHandler.update_control(services)


def _update_control_from_form_edit(req):
    if not req.form:
        return

    services = jsonHandler.get_services()
    for s in services:
        if s.get_name() == req.form['service_name']:
            print("edit on existing route %s" % req.form['service_name']) # apagar
            for route in s.get_routes():

                for response_path in route.get_responses():
                    json_file = fileHandler.get_file_name(response_path)

                    file_key = req.form.get('%s%s_remove_json' %
                                            (route.get_path(),
                                             json_file), None)

                    if file_key is not None:
                        fileHandler.remove_file(response_path)
                        route.remove_response(response_path)
                        route.update_routes()

    jsonHandler.update_control(services)
    update_control_from_post_form_add_new(req)


def _create_route(route, responses):
    return decodables.Route(route, responses[0], 200, 0, responses)


def _get_serialize_routes(route):
    return route.serialize()


def _valid_json(filename):
    return filename.endswith(".json")
