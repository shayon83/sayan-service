# -*- coding: utf-8 -*-
""" Common factory implementation. """

import factory  # noqa

from factory.alchemy import SQLAlchemyModelFactory

from sayan_service.database import db, SQLAlchemyError


class BaseFactory(SQLAlchemyModelFactory):
    """ The base factory. """

    class Meta:
        """ Global factory configuration. """

        abstract = True
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'flush'

    @classmethod
    def _create(cls, *args, **kwargs):
        """_create

        An override of the BaseFactory from factory_boy. This simply wraps the method from the
        parent and rolls back the current transaction if it fails. This is primarily to model
        the behavior of the top-level Model class.

        :param *args:
            Args to proxy to the parent method.
        :param **kwargs:
            Kwargs to proxy to the parent method.
        """
        try:
            return super()._create(*args, **kwargs)
        except SQLAlchemyError:
            cls._meta.sqlalchemy_session.rollback()
            raise
