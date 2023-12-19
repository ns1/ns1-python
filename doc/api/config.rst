ns1.config
==========

This object is used to configure the SDK and REST client. It handles multiple
API keys via a simple selection mechanism (keyID).

Sample:

.. code-block:: json

    {
       "default_key": "account2",
       "verbosity": 5,
       "keys": {
            "account1": {
                "key": "<<CLEARTEXT API KEY>>",
                "desc": "account number 1",
            },
            "account2": {
                "key": "<<ANOTHER CLEARTEXT API KEY>>",
                "desc": "account number 2",
            }
       },
       "cli": {
           "output_format": "text"
       }
    }

.. automodule:: ns1.config
    :members:
    :undoc-members:
    :show-inheritance:



