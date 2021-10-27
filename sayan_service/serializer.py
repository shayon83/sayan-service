# -*- coding: utf-8 -*-
""" Serializer module for marshalling API responses. """

from marshmallow_enum import EnumField  # noqa

from .extensions import marshmallow as ma


class Serializer(ma.Schema):
    """ A base serializer for non-model entities. """
    class Meta:
        strict = True


class ModelSerializer(ma.ModelSchema):
    """ A base serializer for model entities. """
    class Meta:
        strict = True

    uuid = ma.String()
    created_at = ma.DateTime()
    updated_at = ma.DateTime()
