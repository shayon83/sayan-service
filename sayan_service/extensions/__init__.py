# -*- coding: utf-8 -*-
""" Extensions module for registering Flask extensions. """

from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .flask_structlog import FlaskStructlog

bcrypt = Bcrypt()
cache = Cache()
cors = CORS()
db = SQLAlchemy()
marshmallow = Marshmallow()
migrate = Migrate()
structlog = FlaskStructlog()
