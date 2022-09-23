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

# import a zone from the included example zone definition
zone = api.createZone("example2.com", zoneFile="./importzone.db")
print(zone)

# delete a whole zone, including all records, data feeds, etc. this is
# immediate and irreversible, so be careful!
zone.delete()
