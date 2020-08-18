

def generate_route(routes):
    return [Route.from_dict(route) for route in routes]


def get_services_names(services):
    return [s.get_name() for s in services]


class Service:

    def __init__(self, name, routes):
        self.name = name
        self.routes = generate_route(routes)

    def get_name(self):
        return self.name

    def get_routes(self):
        return self.routes

    def get_paths(self):
        return [r.get_path() for r in self.routes]

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
        return [r.serialize() for r in self.routes]

    def merge_routes(self, new_route):
        if new_route.get_path() in self.get_paths():

            for existing_route in self.get_routes():
                if existing_route.get_path() == new_route.get_path():

                    existing_route.responses = list(
                        set(existing_route.responses + new_route.responses))
                    break
        else:
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

    def get_responses_json(self):
        return [r.split('/')[-1] for r in self.get_responses()]

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
