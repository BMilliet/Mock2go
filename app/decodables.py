
def generate_route(routes):
    return [Route.from_dict(route) for route in routes]


class Service:

    def __init__(self, name, routes):
        self.name = name
        self.routes = generate_route(routes)

    def __str__(self):
        return 'Service => name: %s, routes: %s' % (self.get_name(), self.get_paths())

    def get_name(self):
        return self.name

    def get_routes(self):
        return self.routes

    def get_paths(self):
        return [r.get_path() for r in self.routes]

    def get_response_for_path(self, path):
        try:
            return list(filter(lambda r: r.get_path() == path, self.routes))[0].to_tuple()
        except:
            return None

    def serialize(self):
        return {
            'name': self.name,
            'routes': self.get_serialized_routes()
        }

    def get_serialized_routes(self):
        return [r.serialize() for r in self.routes]

    def merge_routes(self, new_routes):
        for new in new_routes:
            self._merge_route(new)

    def _merge_route(self, new_route):
        if new_route.get_path() in self.get_paths():

            for existing_route in self.get_routes():
                if existing_route.get_path() == new_route.get_path():

                    existing_route.responses = list(
                        set(existing_route.responses + new_route.responses))
                    existing_route.update_routes()
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

    def __str__(self):
        return 'Route => path: %s, responses%s' % (self.get_path(), self.get_responses())

    def __eq__(self, other):
        if not isinstance(other, Route):
            return False
        return self.path == other.path and self.current_response == other.current_response and self.status == other.status and self.delay == other.delay and self.responses == other.responses

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

    def to_tuple(self):
        return (self.get_current_response(), self.get_status(), self.get_delay())

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
