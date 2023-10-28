from flask_cors import CORS
from gevent import monkey

from aca.api.controllers.call_control_controllers import call_api_bp
from aca.api.controllers.enrollment_controllers import enrollment_api_bp
from aca.api.controllers.internal_controllers import api_bp
from aca.api.controllers.lock_control_controllers import lock_api_bp
from aca.api.controllers.status_controllers import status_api_bp

monkey.patch_all()

import logging.handlers
import os

from flask import Flask
from flask_injector import FlaskInjector

from aca.application_context import context

# logging
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "DEBUG"))

# app
app = Flask(__name__, static_folder="static", static_url_path="/static")

# blueprints
app.register_blueprint(api_bp)
app.register_blueprint(call_api_bp)
app.register_blueprint(lock_api_bp)
app.register_blueprint(enrollment_api_bp)
app.register_blueprint(status_api_bp)

# di
app.before_first_request_funcs = []

app.config["iocc"] = FlaskInjector(app=app, modules=[context])

CORS(app, resources={r'/*': {'origins': '*'}})

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    app.run(threaded=True)
