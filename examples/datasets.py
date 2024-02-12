#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

import time

from ns1 import NS1

# NS1 will use config in ~/.nsone by default
api = NS1()

# to specify an apikey here instead, use:

# from ns1 import Config
# config = Config()
# config.createFromAPIKey('<<CLEARTEXT API KEY>>')
# api = NS1(config=config)

config = api.config

#########################
# LOAD / CREATE DATASET #
#########################

# create a dataset
dt = api.datasets().create(
    name="my dataset",
    datatype={
        "type": "num_queries",
        "scope": "account",
    },
    repeat=None,
    timeframe={
        "aggregation": "monthly",
        "cycles": 1
    },
    export_type="csv",
    recipient_emails=None,
)
print(dt)

# to load an existing dataset, get a Dataset object back
dt = api.datasets().retrieve(dt.get("id"))
print(dt)

######################
# DOWNLOAD REPORTS   #
######################

while True:
    print("waiting for report to be generated...")
    time.sleep(5)

    dt = api.datasets().retrieve(dt.get("id"))
    reports = dt.get("reports")
    if reports is None:
        continue

    status = reports[0].get("status")
    if status == "available":
        print("report generation completed")
        break

    if status == "failed":
        print("failed to generate report")
        exit(1)

report = api.datasets().retrieveReport(dt.get("id"), reports[0].get("id"))
file_path = "%s.%s" % (dt.get("name"), dt.get("export_type"))

with open(file_path, "w") as file:
    file.write(report)

print("dataset report saved to", file_path)
