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

# create a record to connect to this source, with two answers
# specify the up filter so we can send traffic to only those nodes
# which are known to be up. we'll start with just the second answer up.
record = zone.add_A('record',
                    [{'answer': ['1.1.1.1'],
                      'meta': {
                          'up': False
                          }
                      },
                     {'answer': ['9.9.9.9'],
                      'meta': {
                          'up': True
                          }
                      }],
                    filters=[{'up': {}}])

# create feeds from this source for each answer
feedAPI = nsone.datafeed()
feedAPI.create(sourceID,
               'feed to server1',
               config={'label': 'server1'},
               destinations=[{'desttype': 'answer',
                              'record': record.data['id'],
                              'destid': record.data['answers'][0]['id']
                              }])

feedAPI.create(sourceID,
               'feed to server2',
               config={'label': 'server2'},
               destinations=[{'desttype': 'answer',
                              'record': record.data['id'],
                              'destid': record.data['answers'][1]['id']
                              }])

# now publish an update via feed to the records
sourceAPI.publish(sourceID, {
    'server1': {
        'up': True
    },
    'server2': {
        'up': False
    }})

# NSONE will instantly notify DNS servers at the edges, causing traffic to be
# sent to server1, and ceasing traffic to server2
