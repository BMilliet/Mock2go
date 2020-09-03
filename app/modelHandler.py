from . import decodables


def get_services_names(services):
    return [s.get_name() for s in services]


def get_paths_tuple(services):
    param_list = []
    regular_list = []

    for p in _get_all_paths_from_all(services):
        param_list.append(p) if 'PARAMETER' in p else regular_list.append(p)

    return (regular_list, param_list)


def get_response_from_path(path, services):
    return _get_route_for_path(path, _get_all_routes_from(services))


def is_same_route(path1, path2):
    try:
        return list(set(path2.split('/')).difference(path1.split('/')))[0] == 'PARAMETER'
    except:
        return False


def _get_all_paths_from_all(services):
    return [path for route_paths in _get_all_regular_paths_from(services) for path in route_paths]


def _get_all_regular_paths_from(services):
    return [s.get_paths() for s in services]


def _get_all_routes_from(services):
    routes = []
    for s in services:
        for r in s.get_routes():
            routes.append(r)
    return routes


def _get_route_for_path(path, routes):
    try:
        return list(filter(lambda r: r.get_path() == path, routes))[0]
    except:
        return None
