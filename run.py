from flask import Flask, request
from app import controller, fileHandler

app = Flask(__name__)

app.config['ENV'] = 'Development'
app.config['DEBUG'] = True

fileHandler.setup_if_needed()

@app.route('/<path:string_route>', methods=['GET', 'POST'])
def get_route(string_route):
    return controller.get_response_for_route(string_route, request)


if __name__ == '__main__':
    app.run()
