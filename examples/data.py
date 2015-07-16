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

# create a zone to play in
zone = nsone.createZone('testzone.com')

# create an NSONE API data source
sourceAPI = nsone.datasource()
s = sourceAPI.create('my api source', 'nsone_v1')
sourceID = s['id']

# create feeds which will drive the meta data for each answer
# we'll use the id of these feeds when we connect the feeds to the
# answer meta below
feedAPI = nsone.datafeed()
feed1 = feedAPI.create(sourceID,
                       'feed to server1',
                       config={'label': 'server1'})

feed2 = feedAPI.create(sourceID,
                       'feed to server2',
                       config={'label': 'server2'})

# create a record to connect to this source, with two answers
# specify the up filter so we can send traffic to only those nodes
# which are known to be up. we'll start with just the second answer up.
# each 'up' meta value is a feed pointer, pointing to the feeds we
# created above
record = zone.add_A('record',
                    [{'answer': ['1.1.1.1'],
                      'meta': {
                          'up': {'feed': feed1['id']}
                          }
                      },
                     {'answer': ['9.9.9.9'],
                      'meta': {
                          'up': {'feed': feed2['id']}
                          }
                      }],
                    filters=[{'up': {}}])

# now publish an update via feed to the records. here we push to both
# feeds at once, but you can push to one or the other individually as well
sourceAPI.publish(sourceID, {
    'server1': {
        'up': True
    },
    'server2': {
        'up': False
    }})

# NSONE will instantly notify DNS servers at the edges, causing traffic to be
# sent to server1, and ceasing traffic to server2
