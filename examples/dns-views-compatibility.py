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
field. The reference in the URL can now be an arbitrary string, unique within
your account. This identifier is passed and returned in the 'name' field for
zones, and the 'zone_name' field for records. You may of course continue to use
the FQDN as the identifier - in fact, if you are not using "views", it is
recommended that you do so. However:

* Mismatches between the zone name in the URL and the 'zone' field are no
  longer validated to match, as it is no longer an invalid condition.
* New field 'name' on zone responses. Also a new 'views' array
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

* the "zone/z" argument to CRUD methods is always considered the
  "name/zone_name"
* On create, when the "name" is not the FQDN, the FQDN must be passed in
  the 'zone' field, as we still need to know the FQDN for assignment.

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


# create a named zone
# ===================
# "zone" must be passed in args
data = {"zone": "example.com", "ttl": 900}
zone_object = zones.create("example-name", **data)


# add a record
# ============
data = {"zone": "example.com", "ttl": 888}
record_object = records.create("example-name", "sub.example.com", "A", **data)


# retrieve a record
# =================
record_object = records.retrieve("example-name", "sub.example.com", "A")


# update a record
# ===============
data = {"ttl": 888}
record_one = records.update("example-name", "sub.example.com", "A", **data)


# delete a record
# ===============
delete_response = records.delete("example-name", "sub.example.com", "A")


# retrieve zone
# =============
zone_object = zones.retrieve("example-name")
# search is by "name"
search_results = zones.search("example")


# update named zone
# =================
data = {"ttl": 999}
zone_one = zones.update("example-name", **data)


# delete named zone
# =================
delete_response = zones.delete("example-name")
