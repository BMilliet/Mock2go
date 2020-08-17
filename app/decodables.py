

def generate_route(routes):
    routes_list = []
    for route in routes:
        routes_list.append(Route.from_dict(route))
    return routes_list


def get_services_names(services):
    names = []
    for s in services:
        names.append(s.get_name())
    return names


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

    def serialize(self):
        return {
            'name': self.name,
            'routes': self.get_serialized_routes()
        }

    def get_serialized_routes(self):
        serialized_routes = []
        for r in self.routes:
            serialized_routes.append(r.serialize())
        return serialized_routes

    def merge_routes(self, new_route):
        for route in self.routes:
            if route.get_path() == new_route.get_path():
                for new_response in new_route.get_responses():
                    if new_response not in route.get_responses():
                        route.responses.append(new_response)
            return
        self.routes.append(new_route)

    @classmethod
    def from_dict(cls, json_dict):
        return cls(**json_dict)


class Route:

    def __init__(self, path, current_response, status, delay, responses):
        self.path = path
        self.current_response = current_response
        self.status = int(status)
        self.delay = int(delay)
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

    def remove_response(self, resp):
        self.responses.remove(resp)

    def get_responses_formatted(self):
        formatted = ""
        for r in self.get_responses():
            formatted += ("%s\r\n" % r)
        return formatted

    def get_responses_json(self):
        json_list = []
        for r in self.get_responses():
            json_list.append(r.split('/')[-1])
        return json_list

    def update_routes(self):
        if len(self.responses) > 0:
            self.current_response = self.responses[0]
        else:
            self.current_response = ""

    def serialize(self):
        return {
            'path': self.path,
            'current_response': self.current_response,
            'status': self.status,
            'delay': self.delay,
            'responses': self.responses
        }

    @classmethod
    def from_dict(cls, json_dict):
        return cls(**json_dict)
