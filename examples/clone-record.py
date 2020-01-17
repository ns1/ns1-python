#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from ns1 import NS1

# NS1 will use config in ~/.nsone by default
api = NS1()

# to specify an apikey here instead, use:
# api = NS1(apiKey='qACMD09OJXBxT7XOuRs8')

# to load an alternate configuration file:
# api = NS1(configFile='/etc/ns1/api.json')

# load a zone
zone = api.loadZone("test.com")

# create a complex record
zone.add_A(
    "complex",
    [
        {"answer": ["1.1.1.1"], "meta": {"up": False, "country": ["US"]}},
        {"answer": ["9.9.9.9"], "meta": {"up": True, "country": ["FR"]}},
    ],
    use_csubnet=True,
    filters=[{"geotarget_country": {}}, {"select_first_n": {"N": 1}}],
)

# copy it to another record: old domain, new domain, record type
newrec = zone.cloneRecord("complex", "copy", "A")
print(newrec)

# you can also copy it to a different zone
newrec = zone.cloneRecord("complex", "complex", "A", zone="example.com")
print(newrec)
