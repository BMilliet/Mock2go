from flask import Flask
from app import config, controller

app = Flask(__name__)

config.config_env(app)


@app.route('/<route_string>', methods=['GET'])
def get_route(route_string):
    return controller.get_response_for_route(route_string)


if __name__ == '__main__':
    app.run()
