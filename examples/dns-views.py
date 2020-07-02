"""

DNS views allow for <blurb here>

This means an FQDN can now appear in more than one zone. We have implemented
views in a back-compatible way, so if you do not intend to use them, you can
largely continue to use the API as you've done before.

# How it works

Until now, API calls for a zone have have had the FQDN in the URL, and in the
'zone' field in the body. If the URL and body don't match, or if it's not a
valid FQDN, it is an error.

For views, the 'zone' field on the body still contains the zone's FQDN, but the
URL string no longer has to match, or be an FQDN. This field is now a "handle",
unique within your account, to identify the "view". This identifier is passed
and appears in the "name" field on zones, and the "zone_name" field on records.

The identifier may "happen" to be an FQDN, but is no longer required to be.

Lets say you have an existing "classic" zone:
/v1/zones/example.com {'zone': 'example.com', 'name': 'example.com'}

Now you can add a "named zone" with the same FQDN:
/v1/zones/example-two {'zone': 'example.com', 'name': 'example-two'}

And you can use the /views and /acl endpoints to configure how you want these
zones to serve.

# SDK considerations

Currently, not all SDK methods are "DNS views aware". For back-compatibily,
some can't be changed easily. When working with DNS views, care should be taken
if using SDK methods not shown here, such as the "high level" interfaces. Due
to compatibility, you may "successfully" end up doing the wrong thing!

Existing methods for create and update are a bit awkward when used with views,
due to compatibility, so create_named and update_named methods are provided

In general, when working with zones and records in the views paradigm, it's a
good idea to pass both the "zone" and "name/zone_name" parameters, even when
not strictly required, as it makes intent explicit.
"""

client = {}

zones = client.zones()
records = client.records()


# create zone ...
# ===============

# ... with existing method, "name" is required, FQDN still passed as argument
data = {'name': 'example-one', 'ttl': 900}
zone_one = zones.create('example.com', **data)

# ... with convenience function, name and FQDN are passed as aeguments. "name"
# is not required in data, but will validate against the passed name if present
data = {'ttl': 900}
zone_two = zones.create_named('example-two', 'example.com', **data)


# add a record ...
# ================

# ... with existing method
data = {'name': 'example-one', 'ttl': 888}
record_one = records.create('example.com', 'sub.example.com', 'A', **data)

# ... or convenience method
data = {'ttl': 888}
record_two = records.create_named('example-two', 'example.com', 'sub.example.com', 'A', **data)


# retrieve a record ...
# =====================

# ... ensure you are passing the "name" and not the FQDN
record_one = records.retrieve('example-one', 'sub.example.com', 'A')
record_two = records.retrieve('example-two', 'sub.example.com', 'A')


# update a record ...
# ===================

# ... with existing method
data = {'name': 'example-one', 'ttl': 888}
record_one = records.update('example.com', 'sub.example.com', 'A', **data)

# ... or convenience method
data = {'ttl': 888}
record_two = records.update_named('example-two', 'example.com', 'sub.example.com', 'A', **data)


# delete a record ...
# ===================

# .. ensure you are passing the "name" and not the FQDN
for name in ['example-one', 'example-two']:
    response = records.delete(name, 'sub.example.com', 'A')


# retrieve zone ....
# ==================

# ... ensure you are passing the "name" and not the FQDN
zone_one = zones.retrieve('example-one')
zone_two = zones.retrieve('example-two')

# search is by "name"
search_results = zones.search('example')


# update named zone ...
# =====================

# ... with existing method
data = {'name': 'example-one', 'ttl': 999}
zone_one = zones.update('example.com', **data)

# ... or convenience function
data = {'ttl': 900}
zone_two = zones.update_named('example-two', 'example.com', **data)


# delete named zone ...
# =====================

# ... ensure you are passing the "name" and not the FQDN
for name in ['example-one', 'example-two']:
    response = zones.delete(name)
