from flask import current_app


def iocc(dependency):
    container = current_app.config["iocc"]
    return container.injector.get(dependency)