# -*- coding: utf-8 -*-
""" Database seeding. """

import click

from flask.cli import with_appcontext


@click.command()
@with_appcontext
def seed():
    """seed

    Seeds the application with initial data.
    """
    click.echo('Seeding initial data...')

    ##
    # Put any application seeding logic here.
    #

    click.secho('Done!', fg='green')
