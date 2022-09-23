#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from ns1 import NS1

# NS1 will use config in ~/.nsone by default
api = NS1()

# to specify an apikey here instead, use:
# api = NS1(apiKey='<<CLEARTEXT API KEY>>')

# to load an alternate configuration file:
# api = NS1(configFile='/etc/ns1/api.json')

zone = api.loadZone("test.com")
qps = zone.qps()
print("current QPS for test.com: %s" % qps["qps"])
usage = zone.usage()
print("test.com usage: %s" % usage)
usage = zone.usage(period="30d")
print("test.com 30 d usage: %s" % usage)

rec = zone.loadRecord("foo", "A")
rqps = rec.qps()
print("current QPS for foo.test.com: %s" % rqps["qps"])
usage = rec.usage()
print("foo.test.com usage: %s" % usage)
usage = rec.usage(period="30d")
print("foo.test.com 30 d usage: %s" % usage)
