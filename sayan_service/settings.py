# -*- coding: utf-8 -*-
""" Application configuration. """

import os
from pathlib import Path
from typing import List

from decouple import Csv, config


class Config(object):
    """Config

    The configuration for the application. Each configuration option is specified as a class
    constant with a value derived from the environment using the :meth:`decouple.config` function.

    Default values, when specified, should be production-safe. If a production-safe value is
    dependent on usage, a default is not specified and is instead expected to be configured by
    the environment.
    """

    ##
    #: The `APP_DIR` points to the location of the Flask app on the local
    #: filesystem.
    #:
    #: This value is not configurable as it derives itself from the path of this
    #: settings file, as it is assumed to be in the `APP_DIR`.
    #:
    APP_DIR: Path = Path(__file__).parent.absolute()

    ##
    #: The `PROJECT_ROOT` specifies the path to the project (the directory
    #: containing migrations, tests, configurations, etc).
    #:
    #: This value is not configurable as it derives itself from the parent
    #: directory of the `APP_DIR`.
    #:
    PROJECT_ROOT: Path = APP_DIR.parent

    ##
    #: The `ENV` specifies the environment context that the application is
    #: being run in (local, development, staging, production).
    #:
    #: In general it is considered bad practice to write code that depends on
    #: this value: the application should be unaware of its environment context.
    #:
    #: However, this value may be used to restrict or prevent certain actions
    #: based on context. For example, disabling dangerous or destructive
    #: administrative actions in a production environment.
    #:
    #: Default: `production`
    #:
    ENV: str = config('ENV', 'production')

    ##
    #: The `DEBUG` flag is a standard universal flag for increasing verbosity
    #: and enabling developer features.
    #:
    #: Default: `False`
    #:
    DEBUG: bool = config('DEBUG', False, cast=bool)

    ##
    #: The `LOG_LEVEL` is used to configure logging verbosity.
    #:
    #: Possible values are:
    #:
    #:   - `NOTSET`
    #:   - `DEBUG`
    #:   - `INFO`
    #:   - `WARNING`
    #:   - `ERROR`
    #:   - `CRITICAL`
    #:
    #: Default: `INFO` (or `DEBUG` if the `DEBUG` flag is set)
    #:
    LOG_LEVEL: str = config('LOG_LEVEL', ('DEBUG' if DEBUG else 'INFO'), cast=str.upper)

    ##
    #: The `LOG_PRETTY` flag is used to make log messaging more human-readable.
    #:
    #: Most often used in development contexts.
    #:
    #: Default: `False`
    #:
    LOG_PRETTY: bool = config('LOG_PRETTY', False, cast=bool)

    ##
    #: The `SECRET_KEY` is used for signing and encryption. It should be
    #: randomly generated and appropriately secured.
    #:
    SECRET_KEY: str = config('SECRET_KEY')

    ##
    #: The `BCRYPT_LOG_ROUNDS` value configures the `rounds` parameter of
    #: `bcrypt.gensalt()` which determines the complexity of the generated
    #: salt.
    #:
    #: Default: `13`
    #:
    BCRYPT_LOG_ROUNDS: int = config('BCRYPT_LOG_ROUNDS', 13, cast=int)

    ##
    #: The `SQLALCHEMY_DATABASE_URI` is an RFC-1738 URI used to create an
    #: SQLAlchemy connection to a database.
    #:
    #: More configuration information can be found at:
    #:   http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls
    #:
    #: Default:
    #:   `postgresql://postgres@postgres:5432/sayan_service`
    #:
    SQLALCHEMY_DATABASE_URI: str = config('DATABASE_URI', 'postgresql://postgres@postgres:5432/sayan_service')

    ##
    #: The `SQLALCHEMY_TRACK_MODIFICATIONS` flag determines whether the
    #: `Flask-SQLAlchemy` extension should track and emit signals for
    #: modifications to model objects. Setting this option to True has a
    #: significant impact on memory usage, and should be disabled if
    #: possible.
    #:
    #: More information can be found at:
    #:  http://flask-sqlalchemy.readthedocs.io/en/stable/config
    #:
    #: Default: `False`
    #:
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = config('SQLALCHEMY_TRACK_MODIFICATIONS', False)

    ##
    #: The `SQLALCHEMY_ECHO` flag specifies whether SQLAlchemy should log the
    #: statements that it receives. If enabled, all queries made via SQLAlchemy
    #: will be logged.
    #:
    #: Enabling this option has a significant impact on performance for any
    #: application with nontrivial database usage, and should only be enabled
    #: for debugging and development purposes.
    #:
    #: Default: `False` (or `True` if the `DEBUG` flag is set)
    #:
    SQLALCHEMY_ECHO: bool = config('SQLALCHEMY_ECHO', False, cast=bool)

    ##
    #: The `CACHE_TYPE` specifies the driver to use for the `Flask-Cache`
    #: extension.
    #:
    #: Supported drivers and more infomation available at:
    #:   https://pythonhosted.org/Flask-Cache/#configuring-flask-cache
    #:
    #: Default: `simple`
    #:
    CACHE_TYPE: str = config('CACHE_TYPE', 'simple')

    ##
    #: The `CACHE_KEY_PREFIX` is used to prevent collisions with other users of
    #: the configured cache. The value of `CACHE_KEY_PREFIX` will be prepended
    #: to all cache keys when interacting with the cache.
    #:
    #: Default: `sayan_service.`
    #:
    CACHE_KEY_PREFIX: str = config('CACHE_KEY_PREFIX', 'sayan_service.')

    ##
    #: The `CORS_ORIGINS` specifies the origins to allow CORS requests from
    #: when configuring the `Flask-CORS` extension.
    #:
    #: It is highly recommended to make this list restrictive in a production
    #: context for security reasons.
    #:
    #: More configuration information available at:
    #:   https://flask-cors.readthedocs.io/en/latest/api.html#flask_cors.CORS
    #:
    #: Default: `*`
    #:
    CORS_ORIGINS: List[str] = config('CORS_ORIGINS', '*', cast=Csv())

    ##
    #: The `CORS_METHODS` specify which HTTP methods are supported by
    #: `Flask-CORS` for the configured CORS_ORIGINS. This value must be
    #: specified as a comma-separated string of valid HTTP methods. The string
    #: will be converted into a list when parsed.
    #:
    #: It is highly recommended to make this list restrictive in a production
    #: context for security reasons.
    #:
    #: More configuration information available at:
    #:   https://flask-cors.readthedocs.io/en/latest/api.html#flask_cors.CORS
    #:
    #: Default: `['GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE']`
    #:
    CORS_METHODS: List[str] = config('CORS_METHODS', 'GET,HEAD,POST,OPTIONS,PUT,PATCH,DELETE', cast=Csv())

    ##
    #: The `CORS_ALLOW_HEADERS` specify which headers will be accepted when
    #: requests are made from the `CORS_ORIGINS`.
    #:
    #: It is highly recommended to make this list restrictive in a production
    #: context for security reasons.
    #:
    #: More configuration information available at:
    #:   https://flask-cors.readthedocs.io/en/latest/api.html#flask_cors.CORS
    #:
    #: Default: `*`
    #:
    CORS_ALLOW_HEADERS: List[str] = config('CORS_ALLOW_HEADERS', '*', cast=Csv())

    ##
    #: The `SWAGGER_UI_ENABLED` flag lets us enable or disable the swagger ui
    #:
    #: Default: `False`
    #:
    SWAGGER_UI_ENABLED: bool = config('SWAGGER_UI_ENABLED', False, cast=bool)
