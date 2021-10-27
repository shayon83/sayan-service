# -*- coding: utf-8 -*-
""" Migration environment. """

from __future__ import with_statement

import logging
from logging.config import fileConfig

from alembic import context
from flask import current_app as app
from sqlalchemy import engine_from_config, pool

# Configuration
DATABASE_URI = app.config.get('SQLALCHEMY_DATABASE_URI')

# Alembic configuration (sourced from alembic.ini)
# Make sure to escape percent symbols in the password
config = context.config
db_uri_escaped = DATABASE_URI.replace('%', '%%')
config.set_main_option('sqlalchemy.url', db_uri_escaped)

# Set up logging
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# Specify the target metadata object for migrations
target_metadata = app.extensions['migrate'].db.metadata


def run_migrations_offline():
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option('sqlalchemy.url')
    context.configure(url=url)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    # Prevents an auto-migration from being generated when there are no changes to the schema:
    #   - See: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    engine = engine_from_config(config.get_section(config.config_ini_section),
                                prefix='sqlalchemy.',
                                poolclass=pool.NullPool)

    connection = engine.connect()
    context.configure(connection=connection,
                      target_metadata=target_metadata,
                      process_revision_directives=process_revision_directives,
                      **app.extensions['migrate'].configure_args)

    try:
        with context.begin_transaction():
            context.execute('SET search_path TO public, shared, extensions;')
            context.run_migrations()
    finally:
        connection.close()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
