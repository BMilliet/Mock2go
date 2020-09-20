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
    if path is None:
        return None

    all_routes = sorted(_get_all_routes_from(
        services),
        key=lambda e: e.get_path())

    start = 0
    end = len(all_routes) - 1

    while start <= end:

        middle = int((start + end) / 2)
        list_mid = all_routes[middle].get_path()

        if list_mid > path:
            end = middle - 1
        elif list_mid < path:
            start = middle + 1
        else:
            return all_routes[middle]


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
