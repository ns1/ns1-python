================
NSONE Python SDK
================

:Info: A Python SDK for accessing NSONE, the Data Driven DNS platform.

.. image:: https://travis-ci.org/ns1/nsone-python.svg?branch=master
        :target: https://travis-ci.org/ns1/nsone-python

.. image:: https://readthedocs.org/projects/nsone/badge/?version=latest

About
=====

This package provides a python SDK for accessing the NSONE DNS platform
and includes both a simple NSONE REST API wrapper as well as a higher level
interface for managing zones, records, data feeds, and more.
It supports synchronous and asynchronous transports.

Both python 2.7 and 3.3 are supported.

Installation
============

  $ pip install nsone

Dependencies
============

None, but supports different transport backends. Currently supported:

 * `requests <http://docs.python-requests.org/en/latest/>`_ (synchronous, the default if available)
 * urllib (synchronous, the default if requests isn't available)
 * `twisted <https://twistedmatrix.com/>`_ (asynchronous)

Other transports are easy to add, see `transport <https://github.com/nsone/nsone-python/tree/develop/nsone/rest/transport>`_

Examples
========

See the `examples directory <https://github.com/nsone/nsone-python/tree/develop/examples>`_

Documentation
=============

If you don't yet have an NSONE account, `signup here (free) <https://nsone.net/signup/>`_

You'll need an API Key. To create one, login to `the portal <https://my.nsone.net/>`_ and
click on the Account button in the top right. Select Settings & Users, then add a new
API Key at the bottom.

* `Documentation at ReadTheDocs <http://nsone.readthedocs.org/en/latest/index.html>`_
* `NSONE REST API Documentation <http://nsone.net/api/>`_

Contributions
=============

We welcome contributions! Please fork on GitHub and submit a Pull Request.

