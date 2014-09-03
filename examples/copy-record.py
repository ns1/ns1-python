#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from nsone import NSONE

# NSONE will use config in ~/.nsone by default
nsone = NSONE()

# to specify an apikey here instead, use:
# nsone = NSONE(apiKey='qACMD09OJXBxT7XOuRs8')

# to load an alternate configuration file:
# nsone = NSONE(configFile='/etc/nsone/api.json')

# load a zone
zone = nsone.loadZone('test.com')

# create a complex record
zone.add_A('complex',
           [{'answer': ['1.1.1.1'],
             'meta': {
                 'up': False,
                 'country': ['US']
                 }
             },
            {'answer': ['9.9.9.9'],
             'meta': {
                 'up': True,
                 'country': ['FR']
                 }
             }],
           use_csubnet=True,
           filters=[{'geotarget_country': {}},
                    {'select_first_n': {'N': 1}}])

# copy it to another record: old domain, new domain, record type
newrec = zone.copyRecord('complex', 'copy', 'A')
print newrec

