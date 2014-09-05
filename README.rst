================
NSONE Python SDK
================

:Info: A Python SDK for accessing NSONE, the Data Driven DNS platform.
:Author: Shannon Weyrick

.. image:: https://travis-ci.org/nsone/nsone-python.png
        :target: https://travis-ci.org/nsone/nsone-python

About
=====

This package provides a python SDK for accessing the NSONE DNS platform.
It provides both a simple NSONE REST API wrapper, as well as a higher level
interface. It supports both synchronous and asynchronous HTTP backends.

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

Examples
========

See the `examples directory <https://github.com/nsone/nsone-python/tree/develop/examples>`_

Documentation
=============

* `Documentation at ReadTheDocs <http://nsone.readthedocs.org/en/latest/index.html>`_
* `NSONE REST API Documentation <http://nsone.net/api/>`_
