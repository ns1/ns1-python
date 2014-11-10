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

# import a zone from the included example zone definition
zone = nsone.createZone('example2.com', zoneFile='./importzone.db')
print(zone)

# delete a whole zone, including all records, data feeds, etc. this is
# immediate and irreversible, so be careful!
zone.delete()
