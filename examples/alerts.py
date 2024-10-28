#
# Copyright (c) 2024 NSONE, Inc.
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

# turn on "follow pagination". This will handle paginated responses for
# zone list and the records for a zone retrieve. It's off by default to
# avoid a breaking change
config = api.config
config["follow_pagination"] = True

# create a new zone, get a Zone object back
# to use in a new alert
zone = api.createZone("example-secondary.com", secondary={
    "enabled": True,
    "primary_ip": "198.51.100.12",
    "primary_port": 53,
    "tsig": {
        "enabled": False,
    }
})
print("Created zone: %s" % zone['name'])

# Create a notifier list.
nl = api.notifylists().create(body={
    "name": "example",
    "notify_list": [{
            "type": "email",
            "config": {
                "email": "user@example.com"
            }
        }
    ]
})
print("Created notifier list with id: %s" % nl['id'])
nl_id = nl['id']

# Create an alert
newAlert = api.alerts().create(name="example_alert", type="zone", subtype="transfer_failed", zone_names=["example-secondary.com"], notifier_list_ids=[nl_id])
alert_id = newAlert['id']
print("Created alert with id: %s" % alert_id)

# List alerts.
alertList = api.alerts().list()
print(alertList)
for alert in alertList:
    print(alert["name"])

# Clean up.
api.alerts().delete(alert_id)
api.notifylists().delete(nl_id)
zone.delete()
