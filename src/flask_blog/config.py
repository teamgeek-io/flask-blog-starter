import ast
import logging
import os

from flask import cli, current_app


def load_envvars(app):
    if not app:
        app = current_app

    cli.load_dotenv()

    for key in app.config:
        if key in ["FLASK_ENV", "FLASK_DEBUG", "ENV", "DEBUG"]:
            continue
        if key in os.environ:
            value = os.environ[key]
            if not isinstance(app.config[key], str):
                value = ast.literal_eval(value)
            app.config[key] = value


def configure_app(app, import_name=None, config=None):
    app.config.from_object(import_name + ".default_settings")

    variable_name = import_name.upper() + "_SETTINGS"
    if variable_name in os.environ:
        app.config.from_envvar(variable_name)

    load_envvars(app)

    if config:
        app.config.from_mapping(config)

    logger_level = getattr(logging, app.config["LOGGER_LEVEL"].upper())
    app.logger.setLevel(logger_level)
