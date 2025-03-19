#
# Copyright (c) 2025 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from ns1 import NS1

# NS1 will use config in ~/.nsone by default
api = NS1()

# to specify an apikey here instead, use:

# from ns1 import Config
# config = Config()
# config.createFromAPIKey('<<CLEARTEXT API KEY>>')
# api = NS1(config=config)

config = api.config

############################
# GET BILLING USAGE LIMITS #
############################

limits = api.billing_usage().getLimits(fromUnix=1738368000, toUnix=1740614400)
print("### USAGE LIMITS ###")
print(limits)
print("####################")

###################################
# GET BILLING USAGE FOR QUERIES   #
###################################

usg = api.billing_usage().getQueriesUsage(fromUnix=1738368000, toUnix=1740614400)
print("### QUERIES USAGE ###")
print(usg)
print("####################")

###################################
# GET BILLING USAGE FOR DECISIONS #
###################################

usg = api.billing_usage().getDecisionsUsage(fromUnix=1738368000, toUnix=1740614400)
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
