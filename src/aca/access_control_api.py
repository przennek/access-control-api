# Enable Gevent monkey patching
from flask_cors import CORS
from gevent import monkey

from aca.api.controllers.api_controllers import api_bp

monkey.patch_all()

import logging.handlers
import os

from flask import Flask, jsonify, send_from_directory
from flask_injector import FlaskInjector

from aca.application_context import context

# logging
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "DEBUG"))

# app
app = Flask(__name__, static_folder="static", static_url_path="/static")

# blueprints
app.register_blueprint(api_bp)

# di
app.before_first_request_funcs = []

app.config["iocc"] = FlaskInjector(app=app, modules=[context])

CORS(app, resources={r'/*': {'origins': '*'}})


# Route to serve /static/aca-front
@app.route('/static/aca-front')
@app.route('/static/aca-front/')
def serve_index():
    return send_from_directory('static', 'index.html')


@app.route('/list-endpoints', methods=['GET'])
def list_endpoints():
    """
    List all registered endpoints in the Flask application.
    """
    endpoints = []
    for rule in app.url_map.iter_rules():
        endpoints.append({
            'endpoint': rule.endpoint,
            'methods': sorted(rule.methods),
            'path': str(rule),
        })

    return jsonify({'endpoints': endpoints})


if __name__ == '__main__':
    app.run(threaded=True)
