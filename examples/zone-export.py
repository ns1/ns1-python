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

# Export a zone to BIND format
# The export() method will:
# 1. Initiate the export job
# 2. Poll the status until complete or failed
# 3. Download and return the zone file content
zone = api.loadZone("example.com")

print("Exporting zone example.com...")
zone_file = zone.export()
print("Export complete!")
print(zone_file)

# Save to a file
with open("example.com.txt", "w") as f:
    f.write(zone_file)
print("Zone file saved to example.com.txt")

# Made with Bob
