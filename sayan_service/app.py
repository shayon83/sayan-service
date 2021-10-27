# -*- coding: utf-8 -*-
""" The entry point for the application. """

import traceback

import connexion
import flask

from sayan_service import commands, errors
from sayan_service.extensions import bcrypt, cache, cors, db, marshmallow, migrate, structlog
from sayan_service.settings import Config
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics


def create_app(config_object=None):
    """ Creates an instance of the app. """
    cxn = connexion.FlaskApp(__name__.split('.')[0], specification_dir='api/')
    app = cxn.app

    # Register the logger as early as possible.
    register_logger(app)
    logger = app.logger

    logger.debug('Configuring the Flask app')
    app.config.from_object(config_object or Config)

    logger.debug('Loading Flask extensions')
    register_extensions(app)

    logger.debug('Registering Connexion API specs')
    register_specs(cxn)

    logger.debug('Registering a global error handler')
    register_error_handlers(cxn)

    logger.debug('Registering Flask shell context')
    register_shell_context(app)

    logger.debug('Registering CLI commands')
    register_commands(app)

    logger.debug('Registering Metrics handler')
    register_metrics(app)

    return app


def register_logger(app):
    """ Initializes structured logging for the flask app. """
    structlog.init_app(app)


def register_extensions(app):
    """ Registers Flask extensions. """
    bcrypt.init_app(app)
    cache.init_app(app)
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    marshmallow.init_app(app)


def register_specs(cxn):
    """ Register Connexion APIs.
    """
    api_options = {
        'swagger_ui': cxn.app.config.get('SWAGGER_UI_ENABLED')
    }

    cxn.add_api('v1/spec.yaml', strict_validation=True, options=api_options)


def register_error_handlers(cxn):
    """ Registers handlers for uncaught errors. """
    def render_error(error):
        cxn.app.logger.error(traceback.format_exc())
        content, code = errors.resolve_error(error)
        return flask.jsonify(content), code
    cxn.add_error_handler(Exception, render_error)


def register_shell_context(app):
    """ Registers the context that is available when working with the app in the Python shell. """
    def shell_context():
        return {'db': db}
    app.shell_context_processor(shell_context)


def register_commands(app):
    """ Registers click commands for the app. """
    app.cli.add_command(commands.seed)


def register_metrics(app):
    """ Registers prometheus metrics handler. """
    metrics = GunicornPrometheusMetrics(app)
