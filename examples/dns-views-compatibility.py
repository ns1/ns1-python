"""
DNS views is a means for NS1 to serve one set of data to one group of clients
(e.g. internal employees), and different sets of data to other groups of
clients (e.g. public internet). This has been largely exposed by allowing zones
in the NS1 system to share the same FQDN, and allowing propagation to be
controlled via ACLs and "views". For existing zones, and users that have no
need for the added complexity of views, the default behavior is unchanged.
However, it is important to understand that the requirement that an FQDN be
unique within the network is removed in v3.x, and the ramifications of that.

COMPATIBILITY

Since an FQDN can now appear in more than one "zone", it can no longer uniquely
identify a zone. Instead, a user-supplied "name", unique within an account,
is used to uniquely identify the zone.

The zone name can be the same as its FQDN, existing zones transfer to the new
schema this way. And if not using views, it does serve as a good identifier.
However, if a second zone is created pointing to same FQDN, it cannot reuse
the FQDN as an identifier, and queries for the zone FQDN (as an identfier)
will return the first zone. The following example should help illustrate:

In general, for API requests, the identifier for a zone will appear in the URL.
They can also be passed or received as fields on an object. In the following
request to a v2.x system, we use ZONE as an identifier in the URL, and may
pass the `zone` field as an indicator of the FQDN for the zone.

$ENDPOINT/v1/zones/example.com -d '{zone: example.com}'
                   ^                ^
                   L___ ZONE (id)   L____ ZONE (fqdn)

Note also that it has been an ERROR if the values in the URL and `zone` field
do not match, and the API would reject.

Going forward, the unique identifier and FQDN of the zone are decoupled. The
reference in the URL is user-assignable, and is passed and returned using the
`name` field for zones (and the `zone_name` field for records). In the new
paradigm, the previous call would look more like:

$ENDPOINT/v1/zones/example.com -d '{zone: example.com, name: example.com}'
                   ^                ^                  ^
                   L___ NAME        L____ ZONE         L____ NAME

For compatibility, if `name` isn't present, the API will use the FQDN, so the
2.x call above should continue to work, and have the same result.

However, in 3.x we are now allowed to make new zones with the same FQDN:

$ENDPOINT/v1/zones/example-internal -d '{zone: example.com, name: example-internal}'
                   ^                     ^                  ^
                   L___ NAME             L____ ZONE         L____ NAME

`example-internal` shares the FQDN with `example.com`. API calls using
`example.com` as the identifier will uniquely identify the first zone, to
address the second zone, `example-internal` must be used in the identifier

So, you can continue to use the FQDN as an identifier - in fact, if you
are not using "views", it is recommended that you do so, but other zones using
the same FQDN will have to choose different names.

Note also that both the example-internal and example.com "zones" can coexist.
How they are propagated relies on how they are organized with regard to views,
acls, and networks.

SUMMARY

* As noted, mismatches between the zone name in the URL and the `zone` field
  are no longer rejected, as it is no longer an invalid condition.
* Change to zone responses: new field `name`. Also a new `views` array.
* Change to record responses: new field `zone_name` This holds the identifier
  for the record's zone

Client code should be updated to prefer the `name/zone_name` fields to the
`zone` fields, if present, for use as an identifier. In general, this can be
done without great urgency, however, it is a requirement that you do so if
exercising views functionality.

SDK CHANGES

There are some new endpoints for views functionality, which are discussed in
the dns-views example. This note is concerned with existing methods.

"lower level" rest interface:

* the `zone/z` argument to CRUD methods is always considered the
  "name/zone_name"
* On create, when the "name" is not the FQDN, the FQDN must be passed in
  the `zone` field, as we still need to know the FQDN for assignment.

Similar conceptual changes apply to the "high level" interface as illustrated
below.
"""

from ns1 import NS1

client = NS1()


# rest interface

# the resources we will be using
zones = client.zones()
records = client.records()


# create a named zone
# ===================
# "zone" must be passed in args to provide the FQDN
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


# high level interface


# create a named zone
# ===================
zone = client.createZone("example-name", zone="example.com")

# add a record
# ============
record = zone.add_A("domain.example.com", ["1.2.3.4"])

# retrieve a record
# =================
record = zone.loadRecord("domain.example.com", "A")

# update a record
# ===============
record.update(answers=["1.2.3.5"])
record.addAnswers(["2.3.4.5"])

# delete a record
# ===============
record.delete()

# retrieve zone
# =============
zone = client.loadZone("example-name")

# update named zone
# =================
zone.update(ttl="99")

# delete named zone
# =================
zone.delete()
