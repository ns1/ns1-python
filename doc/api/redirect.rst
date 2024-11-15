ns1.redirect
=========

Redirect is an object representing a single redirect; RedirectCertificate represents a redirect certificate
and the Redirect.retrieveCertificate() method can be used to retrieve it.

.. note::

   The mandatory fields are domain, path and target, which describe a redirect in the form ``domain/path -> target``.

   By default, unless *https_enabled* is set to False, HTTPS will be enabled on the source domain: once there is a
   certificate for the source domain, all redirects using it are automatically HTTPS enabled, regardless of the value
   of *https_enabled*.

   The possible values for *forwarding_mode* are (see https://www.ibm.com/docs/en/ns1-connect?topic=redirects-path-query-forwarding):

   * ``all``: the entire URL path included in incoming requests to the source URL is appended to the target URL.
   * ``none``: no part of the requested URL path should be appended to the target URL.
   * ``capture``: only the segment of the requested URL path matching the wildcard segment defined in the source URL should be appended to the target URL.

   The possible values for *forwarding_type* are (see https://www.ibm.com/docs/en/ns1-connect?topic=redirects-configuring-url-redirect):

   * ``permanent``: answer clients with HTTP 301 Moved Permanently.
   * ``temporary``: answer clients with HTTP 302 Found.
   * ``masking``: answer clients with HTTP 200 OK and include the target in a frame.


.. automodule:: ns1.redirect
    :members:
    :undoc-members:
    :show-inheritance:


