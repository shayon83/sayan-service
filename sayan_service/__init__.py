# -*- coding: utf-8 -*-

""" The top-level application module for sayan_service. """

# We import our top-level modules here so that they can be discovered by tools
# like Alembic and the ServiceProvider. Removing these imports (or failing to
# add them when you create a new module) may cause your models to go
# undiscovered.

from pkg_resources import get_distribution, DistributionNotFound

from . import *  # noqa

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = "0.1.0.dev0+missinggit"
