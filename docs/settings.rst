Application Settings
====================

In keeping with best practices outlined by `The Twelve-Factor App`_, the
application configuration is `managed by the environment`_: all configurable
options are managed by environment variables.

These environment variables are extracted, parsed, and provided by the
:class:`sayan_service.settings.Config` class, each setting
represented as an uppercase class member (to denote that its value should be
constant and immutable).

.. _`The Twelve-Factor App`:  http://12factor.net
.. _`managed by the environment`:  http://12factor.net/config

.. autoclass:: sayan_service.settings.Config
   :members:
