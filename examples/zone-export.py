#
# Copyright (c) 2025 NSONE, Inc.
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

# export a zone to BIND format
zone = api.loadZone("example.com")
zone_file = zone.export()
print(zone_file)

# save to a file
with open("example.com.zone", "w") as f:
    f.write(zone_file)
