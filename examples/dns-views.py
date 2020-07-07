"""
DNS views example

Settiing up "internal" and "external" views of a zone
"""

from ns1 import NS1

client = NS1()

# The resources we will be using
zones = client.zones()
records = client.records()
acls = client.acls()
views = client.views()

# create our zones and records. explicitly setting empty networks keeps
# things from propagating. See dns-views-compatibility for more details on
# zone and record calls
zone_internal = zones.create_named(
    'zone-internal', 'example.com', networks=[]
)
record_internal = records.create_named(
    zone_internal['name'],
    zone_internal['zone'],
    'example.com',
    'A',
    answers=[{'answer': ['1.1.1.1']}]
)
zone_external = zones.create_named(
    'zone-external', 'example.com', networks=[]
)
record_external = records.create_named(
    zone_external['name'],
    zone_external['zone'],
    'example.com',
    'A',
    answers=[{'answer': ['2.2.2.2']}]
)

# create an acl for each view
acl_internal = acls.create(
    'acl-internal',
    src_prefixes=['10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16'],
)
acl_external = acls.create(
    'acl-external',
    src_prefixes=['0.0.0.0/0']
)

# create views. this associates zones, acls, and networks, and as the networks
# are set, triggers propagation
# Note: preference reordering is expensive, try to leave space for insertions
internal_view = views.create(
    'view-internal',
    acls=[acl_internal['name']],
    zones=[zone_internal['name']],
    networks=[1],
    preference=10
)
external_view = views.create(
    'view-external',
    acls=[acl_external['name']],
    zones=[zone_external['name']],
    networks=[1],
    preference=20
)
