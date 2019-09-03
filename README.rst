==============
NS1 Python SDK
==============

:Info: A Python SDK for accessing NS1, the Data Driven DNS platform.

.. image:: https://travis-ci.org/ns1/ns1-python.svg?branch=master
        :target: https://travis-ci.org/ns1/ns1-python

.. image:: https://readthedocs.org/projects/ns1-python/badge/?version=latest
        :target: https://ns1-python.readthedocs.io/en/latest/

About
=====

This package provides a python SDK for accessing the NS1 DNS platform
and includes both a simple NS1 REST API wrapper as well as a higher level
interface for managing zones, records, data feeds, and more.
It supports synchronous and asynchronous transports.

Both python 2.7 and 3.3 are supported.

Installation
============

  $ pip install ns1-python

Dependencies
============

None, but supports different transport backends. Currently supported:

 * `requests <http://docs.python-requests.org/en/latest/>`_ (synchronous, the default if available)
 * urllib (synchronous, the default if requests isn't available)
 * `twisted <https://twistedmatrix.com/>`_ (asynchronous)

Other transports are easy to add, see `transport <https://github.com/ns1/ns1-python/tree/master/ns1/rest/transport>`_

Examples
========

See the `examples directory <https://github.com/ns1/ns1-python/tree/master/examples>`_

Documentation
=============

If you don't yet have an NS1 account, `signup here (free) <https://ns1.com/signup/>`_

You'll need an API Key. To create one, login to `the portal <https://my.nsone.net/>`_ and
click on the Account button in the top right. Select Settings & Users, then add a new
API Key at the bottom.

* `Documentation at ReadTheDocs <https://ns1-python.readthedocs.org/en/latest/>`_
* `NS1 REST API Documentation <https://ns1.com/api/>`_

Tests
=====

Unit tests use `pytest` (`pip install pytest`). 2.7 also requires `mock` to be
installed (`pip install mock`).

Tests should, of course, run and pass under 2.7 and 3.3.

Contributions
=============

We welcome contributions! Please fork on GitHub and submit a Pull Request.
