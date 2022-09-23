#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from ns1 import NS1, Config

# you can either build your own config, or let NS1 build a default one for
# you. the latter is easier and works like this:

# NS1 will use config in ~/.nsone by default
api = NS1()

# to specify an apikey here instead, use:
api = NS1(apiKey="<<CLEARTEXT API KEY>>")

# to load an alternate configuration file:
api = NS1(configFile="/etc/ns1/api.json")

# to load a specific keyID inside of your config file (see config format
# in docs), use this. this only makes sense for config file loads, not
# apiKey loads:
api = NS1(keyID="all-access")

# if you have special needs, build your own Config object and pass it to
# NS1:
config = Config()
config.createFromAPIKey("<<CLEARTEXT API KEY>>")
config["verbosity"] = 5
config["transport"] = "twisted"
api = NS1(config=config)

#  you can get the current config object NS1 is using via
config = api.config

# change config variables
config["verbosity"] = 5

# write out new config files
config.write("/tmp/newconfig.json")

# the config file format supports different apiKeys (see docs) using keyID

# get the current keyID
print(config.getCurrentKeyID())

# use a different keyID
config.useKeyID("read-access")
