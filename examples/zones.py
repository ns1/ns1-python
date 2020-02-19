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

# turn on "follow pagination". This will handle paginated responses for
# zone list and the records for a zone retrieve. It's off by default to
# avoid a breaking change
config = api.config
config["follow_pagination"] = True

######################
# LOAD / CREATE ZONE #
######################

# to load an existing zone, get a Zone object back
test_zone = api.loadZone("test.com")

# or create a new zone, get a Zone object back
# you can specify options like retry, refresh, expiry, nx_ttl, etc
zone = api.createZone("example.com", nx_ttl=3600)
print(zone)

# once you have a Zone, you can access all the zone information via the
# data property
print(zone.data["dns_servers"])

###############
# ADD RECORDS #
###############

# in general, use add_XXXX to add a new record to a zone, where XXXX represents
# the record type. all of these take optional named parameters like
# ttl, use_csubnet, feed, networks, meta, regions, filters
# all of these return Record objects

# add an A record with a single static answer
rec = zone.add_A("orchid", "2.2.2.2")
print(rec)

# add an A record with two static answers
zone.add_A("honey", ["1.2.3.4", "5.6.7.8"])

# add a cname
zone.add_CNAME("pot", "honey.example.com")

# add an MX with two answers, priority 5 and 10
zone.add_MX(
    "example.com", [[5, "mail1.example.com"], [10, "mail2.example.com"]]
)

# add a AAAA, specify ttl of 300 seconds
zone.add_AAAA("honey6", "2607:f8b0:4006:806::1010", ttl=300)

# add an A record using full answer format to specify 2 answers with meta data.
# ensure edns-client-subnet is in use, and add two filters: geotarget_country,
# and select_first_n, which has a filter config option N set to 1
zone.add_A(
    "bumble",
    [
        {"answer": ["1.1.1.1"], "meta": {"up": False, "country": ["US"]}},
        {"answer": ["9.9.9.9"], "meta": {"up": True, "country": ["FR"]}},
    ],
    use_csubnet=True,
    filters=[{"geotarget_country": {}}, {"select_first_n": {"N": 1}}],
)

# zone usage
print(zone.qps())

###########################
# LOAD and UPDATE RECORDS #
###########################

# if you don't have a Record object yet, you can load it in one of two ways:
# 1) directly from the top level NS1 object by specifying name and type
rec = api.loadRecord("honey.example.com", "A")
print(rec)
# 2) if you have a Zone object already, you can load it from that
rec = zone.loadRecord("honey", "A")
print(rec)

# you can access all the record information via the data property
print(rec.data["answers"])

# add answer(s) to existing answer list
rec.addAnswers("4.4.4.4")
rec.addAnswers(["3.4.5.6", "4.5.6.8"])
print(rec.data["answers"])

# update the full answer list
rec.update(answers=["6.6.6.6", "7.7.7.7"])
print(rec.data["answers"])

# set filters, ttl
rec.update(
    filters=[{"geotarget_country": {}}, {"select_first_n": {"N": 1}}], ttl=10
)

# update record level (as opposed to zone or answer level) meta data
rec.update(meta={"up": False})

# update answer level meta data directly. note this is better done through
# a data feed (see examples/data.py), which allows changing the meta data
# values individually, without having to set the answer block
rec = zone.loadRecord("bumble", "A")
print(rec.data["answers"])
rec.update(
    answers=[
        {"answer": ["1.1.1.1"], "meta": {"up": True, "country": ["US"]}},
        {"answer": ["9.9.9.9"], "meta": {"up": False, "country": ["FR"]}},
    ]
)
print(rec.data["answers"])

# record usage
print(rec.qps())


##########
# DELETE #
##########

# delete a single record
rec.delete()

# delete a whole zone, including all records, data feeds, etc. this is
# immediate and irreversible, so be careful!
zone.delete()
