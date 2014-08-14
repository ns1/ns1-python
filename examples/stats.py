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

rec = zone.loadRecord('foo', 'A')
rqps = rec.qps()
print("current QPS for foo.test.com: %s" % rqps['qps'])
