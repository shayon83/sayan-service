# -*- coding: utf-8 -*-
""" A Flask plugin for structured logging. """

import logging
import structlog
import sys

from flask import Flask, helpers
from typing import Optional
from decouple import config


##
#: We attempt to import the structlog[dev] and colorama packages (for pretty logging)
#: and set a flag if either of them are not available.
#:
try:
    import colorama
    from structlog import dev
    _HAS_STRUCTLOG_DEV = True
except ImportError:
    _HAS_STRUCTLOG_DEV = False


##
#: The `_LOG_LEVEL` controls logging verbosity and is set by the environment.
#:
_LOG_LEVEL = config('LOG_LEVEL', 'INFO')


##
#: When `_LOG_PRETTY` is set to True, a more human-friendly log renderer will be
#: used to emit messages. Generally used in a development context.
#:
_LOG_PRETTY = config('LOG_PRETTY', False, cast=bool)


##
#: The `_STRUCTLOG_PROCESSORS` specify the logging middleware used to structure
#: and format log messages before they're emitted.
#:
#: More information on structlog processors can be found at:
#:   http://www.structlog.org/en/latest/processors.html
#:
_STRUCTLOG_PROCESSORS = [
    structlog.stdlib.filter_by_level,
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.processors.TimeStamper(fmt='iso'),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
    structlog.processors.UnicodeDecoder(),
]


class FlaskStructlog:
    """FlaskStructlog

    A flask extension for patching the builtin Flask logger with a structlogger.
    """

    def __init__(self, app: Optional[Flask]=None, *args, **kwargs) -> None:
        if app:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """init_app

        Patches the builtin Flask logger and replaces it with a structlog logger.

        :param app:
            The Flask app for which to patch the logger.
        """
        if not structlog.is_configured():
            self._initialize_structlog(app)

        self._patch_flask_logger(app)

    def _patch_flask_logger(self, app):
        """_patch_flask_logger

        Replaces the builtin flask logger with a structured logger.

        :param app:
            The Flask app for which to patch the logger
        """
        structured_logger = structlog.get_logger('flask.app')

        def structlogger(self):
            return structured_logger

        setattr(app.__class__, 'logger', helpers.locked_cached_property(structlogger))

        if app.logger is not structured_logger:
            app.logger.warning(
                'The FlaskStructlog extension was unable to patch the builtin Flask logger. This '
                'probably means that a message was logged before the extension was initialized.'
            )

    def _initialize_structlog(self, app):
        """initialize_structlog

        Initializes structlog. Configures pretty logging if enabled.

        :param app:
            The Flask app from which to pull configuration.
        """
        processors = _STRUCTLOG_PROCESSORS
        renderer = structlog.processors.JSONRenderer()

        if _LOG_PRETTY:
            if not _HAS_STRUCTLOG_DEV:
                raise ImportError('The structlog[dev] module is required when LOG_PRETTY=True.')
            renderer = structlog.dev.ConsoleRenderer()

        processors.append(renderer)

        # Configure the logging module to the most basic implementation possible.
        logging.basicConfig(
            level=_LOG_LEVEL,
            stream=sys.stdout,
            format='%(message)s'
        )

        if not structlog.is_configured():
            structlog.configure_once(
                processors=processors,
                context_class=structlog.threadlocal.wrap_dict(dict),
                logger_factory=structlog.stdlib.LoggerFactory(),
                wrapper_class=structlog.stdlib.BoundLogger,
                cache_logger_on_first_use=True,
            )
