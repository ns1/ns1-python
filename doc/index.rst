Python SDK for NS1 DNS Platform
===============================

.. image:: _static/ns1.png
    :target: https://ns1.com/


About
-----

This package provides an SDK for accessing the NS1 DNS platform
and includes both a simple NS1 REST API wrapper as well as a higher level
interface for managing zones, records, data feeds, and more.
It supports synchronous and asynchronous transports.

Python versions 3.8 to 3.12 are supported.

Install with::

  $ pip install ns1-python


Quick Start
-----------

First, you'll need an API Key. To create one, login to `the portal <https://my.nsone.net/>`_ and
click on the Account button in the top right. Select Settings & Users, then add a new
API Key at the bottom.


Simple example:

.. code-block:: python

    from ns1 import NS1

    api = NS1(apiKey='<<CLEARTEXT API KEY>>')
    zone = api.createZone('example.com', nx_ttl=3600)
    print(zone)
    record = zone.add_A('honey', ['1.2.3.4', '5.6.7.8'])
    print(record)

Note that all zone and record changes propagate in real time throughout the NS1 platform.

There are more examples in the `examples directory <https://github.com/ns1/ns1-python/tree/master/examples>`_.

Contributions
-------------

We welcome contributions! Please `fork on GitHub <https://github.com/ns1/ns1-python/>`_ and submit a Pull Request.

Contents
--------

.. toctree::
   :maxdepth: 1

   features
   configuration
   usage


Reference
---------

.. toctree::

   api/modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

