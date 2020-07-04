

def generate_route(routes):
    routes_list = []
    for route in routes:
        routes_list.append(Route.from_dict(route))
    return routes_list


class Service:

    def __init__(self, name, routes):
        self.name = name
        self.routes = generate_route(routes)

    def get_name(self):
        return self.name

    def get_routes(self):
        return self.routes

    def get_paths(self):
        path_list = []
        for r in self.routes:
            path_list.append(r.get_path())
        return path_list

    def get_response_for_path(self, path):
        for r in self.routes:
            if r.get_path() == path:
                return (r.get_current_response(),
                        r.get_status(),
                        r.get_delay())
        return None

    @classmethod
    def from_dict(cls, json_dict):
        return cls(**json_dict)


class Route:

    def __init__(self, path, current_response, status, delay, responses):
        self.path = path
        self.current_response = current_response
        self.status = status
        self.delay = delay
        self.responses = responses

    def get_path(self):
        return self.path

    def get_responses(self):
        return self.responses

    def get_current_response(self):
        return self.current_response

    def get_status(self):
        return self.status

    def get_delay(self):
        return self.delay

    @classmethod
    def from_dict(cls, json_dict):
        return cls(**json_dict)
