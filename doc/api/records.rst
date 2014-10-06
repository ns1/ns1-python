nsone.records
=============

Object representing a single DNS record in a zone of a specific type.

.. note::

   Answers to a record (the `answers` kwarg) should be passed as one of the following four structures, depending on how advanced the configuration for the answer needs to be:

     1. A single string that is coerced to a single answer with no other fields e.g. meta. For example: `"1.1.1.1"`
     2. A list of single strings that is coerced to several answers with no other fields e.g. meta. For example: `["1.1.1.1", "2.2.2.2"]`
     3. A list of lists. In this case there will be as many answers as are in the outer list, and the
        answers themselves are used verbatim from the inner list (e.g. may
        have MX style `[10, '1.1.1.1]`), but no other fields e.g. meta.
        You must use this form for MX records, and if there is only one
        answer it still must be wrapped in an outer list.
     4. A list of dicts. In this case it expects the full rest model and passes it along unchanged. You must use this
        form for any advanced record config like meta data or data feeds.

.. code-block:: python

        # Example of an advanced answer configuration (list of dicts)
        record = yield zone.add_A('record',
                                   [{'answer': ['1.1.1.1'],
                                     'meta': {
                                         'up': False
                                         }
                                     },
                                    {'answer': ['9.9.9.9'],
                                     'meta': {
                                         'up': True
                                         }
                                     }],
                                   filters=[{'up': {}}])

.. automodule:: nsone.records
    :members:
    :undoc-members:
    :show-inheritance:


