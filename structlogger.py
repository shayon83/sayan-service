# -*- coding: utf-8 -*-
""" Utilities for infrastructure components. """

import logging
import sys

import structlog

from sayan_service.settings import Config

##
#: We attempt to import the structlog[dev] package (for pretty logging) and set
#: a flag if it's not available.
#:
try:
    from structlog import dev
    HAS_STRUCTLOG_DEV = True
except ImportError:
    HAS_STRUCTLOG_DEV = False


##
#: The `STRUCTLOG_PROCESSORS` specify the logging middleware used to structure
#: and format log messages before they're emitted.
#:
#: More information on structlog processors can be found at:
#:   http://www.structlog.org/en/latest/processors.html
#:
STRUCTLOG_PROCESSORS = [
    structlog.stdlib.filter_by_level,
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.processors.TimeStamper(fmt='iso'),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
    structlog.processors.UnicodeDecoder(),
]


def initialize_structlog():
    """initialize_structlog

    Initializes structlog. Configures pretty logging if enabled.

    :param log_pretty:
        A flag to control emission of messages as human-readable or machine-parseable.
    """
    processors = STRUCTLOG_PROCESSORS
    renderer = structlog.processors.JSONRenderer()

    if Config.LOG_PRETTY:
        if not HAS_STRUCTLOG_DEV:
            raise ImportError('The structlog[dev] module is required when LOG_PRETTY=True.')
        renderer = structlog.dev.ConsoleRenderer()

    processors.append(renderer)

    # Configure the logging module to the most basic implementation possible.
    logging.basicConfig(level=Config.LOG_LEVEL, stream=sys.stdout, format='%(message)s')

    structlog.configure_once(
        processors=processors,
        context_class=structlog.threadlocal.wrap_dict(dict),
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


class GunicornLogger:
    """
    A stripped down version of the Gunicorn logger to provide structured logging.

    Original implementation:
        https://github.com/benoitc/gunicorn/blob/master/gunicorn/glogging.py
    """

    def __init__(self, cfg):
        """__init__

        Initializes structlog.

        :param cfg:
            The gunicorn configuration.
        """
        initialize_structlog()

        self._logger = structlog.get_logger('gunicorn')
        self.cfg = cfg

    def access(self, resp, req, environ, request_time) -> None:
        """ A noop implementation of access logging. """

    def reopen_files(self) -> None:
        """ A noop implementation of file logging. """

    def close_on_exec(self) -> None:
        """ A noop implementation of log closing. """

    def __getattr__(self, name):
        """ Allows proxying methods to the structlogger. """
        return getattr(self._logger, name)
