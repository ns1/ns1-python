#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from nsone import NSONE

# NSONE will use config in ~/.nsone by default
nsone = NSONE()

# to specify an apikey here instead, use:

# from nsone import Config
# config = Config()
# config.createFromAPIKey('qACMD09OJXBxT7XOuRs8')
# nsone = NSONE(config=config)

zone = nsone.loadZone('test.com')
qps = zone.qps()
print("current QPS for test.com: %s" % qps['qps'])
usage = zone.usage()
print("test.com usage: %s" % usage)
usage = zone.usage(period='30d')
print("test.com 30 d usage: %s" % usage)

rec = zone.loadRecord('foo', 'A')
rqps = rec.qps()
print("current QPS for foo.test.com: %s" % rqps['qps'])
usage = rec.usage()
print("foo.test.com usage: %s" % usage)
usage = rec.usage(period='30d')
print("foo.test.com 30 d usage: %s" % usage)
