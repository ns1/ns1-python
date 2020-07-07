"""
DNS views allow for <blurb here>

This means an FQDN can now appear in more than one zone. We have implemented
views in a back-compatible way, so if you do not intend to use them, you can
largely continue to use the API as you've done before.

COMPATIBILITY

Until now, the unique identifier of a zone in the API has been the FQDN. This
appears both in the URL for API requests and in the 'zone' field of zones and
records. The API throws an error if the URL and field in the body do not match.

Going forward, the unique identifier of the zone is "decoupled" from the 'zone'
field. The reference in the URL can now be an arbitratry string, unique within
your account. This identifier is passed and returned in the 'name' field for
zones, and the 'zone_name' field for records. You may of course continue to use
the FQDN as the identifier - in fact, if you are not using "views", it is
recommended that you do so. However:

* Mismatches between the zone name in the URL and the 'zone' field are no
  longer validated to match, as it is no longer an invalid condition.
* New field 'name' on zone responses
* New field 'zone_name' on record responses

Crucially, if you are NOT using "views", then the 'zone' and 'name' fields on
the zone will probably have the same value, but the unique identifier for the
zone is ALWAYS the value in the 'name' field. So in general, code should be
written or updated to prefer the 'name/zone_name' fields for identification,
and when using "views" functionality, calling code MUST be
"name/zone_name aware".

SDK CHANGES

There are some new endpoints for views functionality, which are discusses in
another example. This note is just about existing methods. Currently, only the
'rest interface' is ensured to be 'name/zone_name' aware:

* zone GET, zone DELETE, record GET, and record DELETE are unchanged. However,
  they should always be passed the zone 'name'.
* for compatibility reasons, the arguments to zone CREATE, zone UPDATE, record
  CREATE, and record UPDATE are unchanged. The argument remains the zone FQDN.
  However, a different 'name/zone_name' can be passed in kwargs.
* since that is somewhat awkward and error prone, 'create_named' and
  'update_named' methods are provided on zones and records. These explicitly
  require the name and fqdn arguments

As noted, not all SDK "interfaces" are "DNS views aware". When working with DNS
views, care should be taken if using SDK methods not shown here, such as the
"high level" interfaces. Due to compatibility, you may "successfully" end up
doing the wrong thing!
"""

from ns1 import NS1

client = NS1()

# the resources we will be using
zones = client.zones()
records = client.records()


# create a named zone ...
# =======================

# ... with existing method. "name" must be passed in kwargs, FQDN is still
# passed as argument
data = {"name": "example-one", "ttl": 900}
zone_one = zones.create("example.com", **data)

# ... with convenience function. name and FQDN are both required arguments.
# "name" is not required in kwargs, but will be validated against the passed
# name if present
data = {"ttl": 900}
zone_two = zones.create_named("example-two", "example.com", **data)


# add a record ...
# ================

# ... with existing method
data = {"name": "example-one", "ttl": 888}
record_one = records.create("example.com", "sub.example.com", "A", **data)

# ... or convenience method
data = {"ttl": 888}
record_two = records.create_named(
    "example-two", "example.com", "sub.example.com", "A", **data
)


# retrieve a record ...
# =====================

# ... ensure you are passing the "name" and not the FQDN
record_one = records.retrieve("example-one", "sub.example.com", "A")
record_two = records.retrieve("example-two", "sub.example.com", "A")


# update a record ...
# ===================

# ... with existing method
data = {"name": "example-one", "ttl": 888}
record_one = records.update("example.com", "sub.example.com", "A", **data)

# ... or convenience method
data = {"ttl": 888}
record_two = records.update_named(
    "example-two", "example.com", "sub.example.com", "A", **data
)


# delete a record ...
# ===================

# .. ensure you are passing the "name" and not the FQDN
for name in ["example-one", "example-two"]:
    response = records.delete(name, "sub.example.com", "A")


# retrieve zone ....
# ==================

# ... ensure you are passing the "name" and not the FQDN
zone_one = zones.retrieve("example-one")
zone_two = zones.retrieve("example-two")

# search is by "name"
search_results = zones.search("example")


# update named zone ...
# =====================

# ... with existing method
data = {"name": "example-one", "ttl": 999}
zone_one = zones.update("example.com", **data)

# ... or convenience function
data = {"ttl": 900}
zone_two = zones.update_named("example-two", "example.com", **data)


# delete named zone ...
# =====================

# ... ensure you are passing the "name" and not the FQDN
for name in ["example-one", "example-two"]:
    response = zones.delete(name)
