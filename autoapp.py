# -*- coding: utf-8 -*-
""" Create an application instance. """

from sayan_service.app import create_app  # noqa
from sayan_service.settings import Config

app = create_app(config_object=Config)
