from flask import Flask

from .config import configure_app


def create_app(config=None):
    import_name = __name__.split(".")[0]
    app = Flask(import_name)

    configure_app(app, import_name, config)

    from .views import graphql, pages

    app.register_blueprint(pages)
    app.register_blueprint(graphql)

    return app
