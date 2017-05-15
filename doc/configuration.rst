Configuration
=============

Configuring the SDK can be done programmatically and/or via loading (and saving) simple
JSON text configuration files. At a minimum, the NS1 API key to access the REST API must
be specified.


Loading From a File
-------------------

By default, configuration is loaded from the file ``~/.nsone``; that is, a file called
``.nsone`` in the home directory of the user calling the script.

.. code-block:: python

    # to load an explicit configuration file:
    api = NS1(configFile='/etc/ns1/api.json')

From an API Key
---------------

.. code-block:: python

    # to generate a configuration based on an api key
    api = NS1(apiKey='qACMD09OJXBxT7XOuRs8')

JSON File Format
----------------

This example shows two different API keys. Which to use can be selected at runtime, see :mod:`ns1.config`

.. code-block:: json

    {
       "default_key": "account2",
       "verbosity": 5,
       "keys": {
            "account1": {
                "key": "qACMD09OJXBxT7XOuRs8",
                "desc": "account number 1",
                "writeLock": true
            },
            "account2": {
                "key": "qACMD09OJXBxT7XOwv9v",
                "desc": "account number 2",
                "writeLock": false
            },
       },
       "cli": {
           "output_format": "text"
       }
    }

More
----

There are more examples in the `config.py example <https://github.com/ns1/ns1-python/tree/master/examples/config.py>`_.
For the full Config object reference API, see :mod:`ns1.config`

