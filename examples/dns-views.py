"""
DNS views example

Settiing up "internal" and "external" views of a zone

https://help.ns1.com/hc/en-us/articles/360054071374
"""

from base64 import b64encode

from ns1 import NS1

client = NS1()

# The resources we will be using
zones = client.zones()
records = client.records()
acls = client.acls()
tsig = client.tsig()
views = client.views()


def run():
    # create our zones and records. explicitly setting empty networks keeps
    # things from propagating. See dns-views-compatibility for more details on
    # zone and record calls
    zone_internal = zones.create(
        "zone-internal", zone="example.com", networks=[]
    )
    record_internal = records.create(
        zone_internal["name"],
        "example.com",
        "A",
        answers=[{"answer": ["1.1.1.1"]}],
    )
    zone_external = zones.create(
        "zone-external", zone="example.com", networks=[]
    )
    record_external = records.create(
        zone_external["name"],
        "example.com",
        "A",
        answers=[{"answer": ["2.2.2.2"]}],
    )

    # we'll use tsig on one of our acls
    tsig_internal = tsig.create(
        "example-tsig",
        algorithm="hmac-sha512",
        secret=b64encode(b"example-secret").decode(),
    )

    # create an acl for each view
    acl_internal = acls.create(
        "acl-internal",
        src_prefixes=["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"],
        tsig_keys=[tsig_internal["name"]],
    )
    acl_external = acls.create("acl-external", src_prefixes=["0.0.0.0/0"])

    # create views. this associates zones, acls, and networks, and as the networks
    # are set, triggers propagation
    # Note: preference reordering is expensive, try to leave space for insertions
    view_internal = views.create(
        "view-internal",
        read_acls=[acl_internal["name"]],
        zones=[zone_internal["name"]],
        networks=[1],
        preference=10,
    )
    view_external = views.create(
        "view-external",
        read_acls=[acl_external["name"]],
        zones=[zone_external["name"]],
        networks=[1],
        preference=20,
    )
    return (
        zone_internal,
        zone_external,
        record_internal,
        record_external,
        acl_external,
        acl_internal,
        view_internal,
        view_external,
        tsig_internal,
    )


def verify():
    print(acls.list())
    print(tsig.list())
    print(views.list())
    print(zones.list())


def cleanup():
    # delete all the things we created
    zones.delete("zone-internal")
    zones.delete("zone-external")
    views.delete("view-internal")
    views.delete("view-external")
    acls.delete("acl-internal")
    acls.delete("acl-external")
    tsig.delete("example-tsig")


# Note: this will do real things to your real account, and you may want to
# config your client differently before running things

# run()
# verify()
# cleanup()
