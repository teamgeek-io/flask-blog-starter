from flask import Flask

from .config import configure_app


def create_app(config=None):
    """Return a new Flask app."""
    import_name = __name__.split(".")[0]
    app = Flask(import_name)

    configure_app(app, import_name, config)

    from .database import db, migrate

    db.init_app(app)
    migrate.init_app(app, db)

    from .views import graphql, posts

    app.register_blueprint(posts)
    app.register_blueprint(graphql)

    return app
