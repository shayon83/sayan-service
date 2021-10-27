# -*- coding: utf-8 -*-
""" Test configuration and fixtures. """

import pytest
import sqlalchemy

from alembic import command
from alembic.config import Config as AlembicConfig
from decouple import config
from flask_migrate import Migrate

from sayan_service.app import create_app
from sayan_service.extensions import db as _db
from sayan_service.settings import Config


class TestConfig(Config):
    """TestConfig

    A configuration object specific to the testing context.
    """

    # Database connection parameters
    SQLALCHEMY_DATABASE_URI = config('TEST_DATABASE_URI', 'postgresql://postgres@postgres:5432/test_sayan_service')  # noqa

    # When the FLASK_DEBUG flag is on, preserving context causes
    # "Popped wrong request context" assertion errors when running tests.
    PRESERVE_CONTEXT_ON_EXCEPTION = False


@pytest.fixture(scope="session")
def app(request):
    """app

    Returns session-wide application.
    """
    app = create_app(config_object=TestConfig)
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture(scope='session')
def db(app, request):
    """db

    Returns session-wide initialized database.
    """

    database_uri = sqlalchemy.engine.url.make_url(TestConfig.SQLALCHEMY_DATABASE_URI)
    host_uri = sqlalchemy.engine.url.URL(
        database_uri.drivername,
        username=database_uri.username,
        password=database_uri.password,
        host=database_uri.host,
        port=database_uri.port)
    database_name = database_uri.database
    template_engine = sqlalchemy.create_engine(host_uri, echo=False)
    conn = template_engine.connect()
    conn = conn.execution_options(
        autocommit=True, isolation_level='AUTOCOMMIT')

    try:
        conn.execute(f'DROP DATABASE IF EXISTS {database_name};')
        conn.execute(f'CREATE DATABASE {database_name};')
    except:
        pass
    finally:
        conn.close()
        template_engine.dispose()

    Migrate(_db.app, _db)
    alembic_config = AlembicConfig('/srv/migrations/alembic.ini')
    alembic_config.set_main_option('script_location', 'migrations')
    command.upgrade(alembic_config, 'head')

    yield _db


@pytest.fixture(scope='function')
def session(app, db, request):
    """session

    Returns function-scoped session, ensuring that tests run in an isolated context.

    This includes database cleaning and any other operations that clean the application state
    so that the tests run consistently.
    """
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(f'TRUNCATE TABLE {table} CASCADE;')

    db.session.commit()

    yield db.session

    db.session.close()
