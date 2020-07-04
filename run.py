from flask import Flask
from app import config, controller

app = Flask(__name__)

config.config_env(app)


@app.route('/<path:string_route>', methods=['GET'])
def get_route(string_route):
    return controller.get_response_for_route(string_route)


if __name__ == '__main__':
    app.run()
