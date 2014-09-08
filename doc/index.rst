Python SDK for NSONE DNS Platform
=======================================

.. image:: _static/NSONE-500x500.png
    :height: 250px
    :width: 250px
    :target: https://nsone.net/


About
-----

This package provides an SDK for accessing the NSONE DNS platform
and includes both a simple NSONE REST API wrapper as well as a higher level
interface for managing zones, records, data feeds, and more.
It supports synchronous and asynchronous transports.

Both python 2.7 and 3.3 are supported.

Install with::

  $ pip install nsone


Quick Start
-----------

You'll need an API Key. To create one, login to `the portal <https://my.nsone.net/>`_ and
click on the Account button in the top right. Select Settings & Users, then add a new
API Key at the bottom.


.. code-block:: python

    from nsone import NSONE

    nsone = NSONE(apiKey='qACMD09OJXBxT7XOuRs8')
    zone = nsone.createZone('example.com', nx_ttl=3600)
    print(zone)
    record = zone.add_A('honey', ['1.2.3.4', '5.6.7.8'])
    print(record)

Note that all zone and record changes propagate in real time throughout the NSONE platform.

There are more examples in the `examples directory <https://github.com/nsone/nsone-python/tree/develop/examples>`_.

Contents
--------

.. toctree::
   :maxdepth: 1

   features


Reference
---------

.. toctree::

   api/modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

