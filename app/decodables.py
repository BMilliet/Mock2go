

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
                return r.get_current_reponse()

    @classmethod
    def from_dict(cls, json_dict):
        return cls(**json_dict)


class Route:

    def __init__(self, path, current_reponse, responses):
        self.path = path
        self.current_reponse = current_reponse
        self.responses = responses

    def get_path(self):
        return self.path

    def get_responses(self):
        return self.responses

    def get_current_reponse(self):
        return self.current_reponse

    @classmethod
    def from_dict(cls, json_dict):
        return cls(**json_dict)
