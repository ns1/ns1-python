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

Installation
============

  $ pip install nsone

Dependencies
============

None, but supports different transport backends. Currently supported:

 * requests (synchronous, the default if available)
 * urllib2 (synchronous, the default if requests isn't available)
 * twisted (asynchronous)

Examples
========

See the `examples directory <https://github.com/nsone/nsone-python/tree/develop/examples>`_

Documentation
=============

* `Documentation at ReadTheDocs <nsone.readthedocs.org/en/latest/index.html>`_
* `NSONE REST API Documentation <http://nsone.net/api/>`_
