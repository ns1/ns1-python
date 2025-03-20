#
# Copyright (c) 2025 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from ns1 import NS1
import datetime

# NS1 will use config in ~/.nsone by default
api = NS1()

# to specify an apikey here instead, use:

# from ns1 import Config
# config = Config()
# config.createFromAPIKey('<<CLEARTEXT API KEY>>')
# api = NS1(config=config)

config = api.config

from_unix = int(
    datetime.datetime.fromisoformat("2025-02-01 00:00:00").strftime("%s")
)
to_unix = int(
    datetime.datetime.fromisoformat("2025-02-28 23:59:59").strftime("%s")
)

############################
# GET BILLING USAGE LIMITS #
############################

limits = api.billing_usage().getLimits(from_unix, to_unix)
print("### USAGE LIMITS ###")
print(limits)
print("####################")

###################################
# GET BILLING USAGE FOR QUERIES   #
###################################

usg = api.billing_usage().getQueriesUsage(from_unix, to_unix)
print("### QUERIES USAGE ###")
print(usg)
print("####################")

###################################
# GET BILLING USAGE FOR DECISIONS #
###################################

usg = api.billing_usage().getDecisionsUsage(from_unix, to_unix)
print("### DECISIONS USAGE ###")
print(usg)
print("####################")

###################################
# GET BILLING USAGE FOR MONITORS #
###################################

usg = api.billing_usage().getMonitorsUsage()
print("### MONITORS USAGE ###")
print(usg)
print("####################")

###################################
# GET BILLING USAGE FOR FILER CHAINS #
###################################

usg = api.billing_usage().getMonitorsUsage()
print("### FILTER CHAINS USAGE ###")
print(usg)
print("####################")

###################################
# GET BILLING USAGE FOR RECORDS #
###################################

usg = api.billing_usage().getRecordsUsage()
print("### RECORDS USAGE ###")
print(usg)
print("####################")
