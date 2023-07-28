import logging.handlers
import os

from flask import Flask
from flask_injector import FlaskInjector

from aca.api.controllers import controller_bp
from aca.application_context import context

# logging
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "DEBUG"))

# app
app = Flask(__name__)

# blueprints
app.register_blueprint(controller_bp)

# di
app.before_first_request_funcs = []

app.config["iocc"] = FlaskInjector(app=app, modules=[context])

if __name__ == '__main__':
    app.run()
